import os, re, json, argparse, unicodedata, logging, warnings
from datetime import datetime
from pathlib import Path

# Suprimir warnings de fontes do pdfplumber
logging.getLogger("pdfminer").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

try:
    import pdfplumber
    PDF_ENGINE = "pdfplumber"
except ImportError:
    raise ImportError("Instale pdfplumber: pip install pdfplumber")

CATEGORIAS = {
    "etp": {
        "label": "Estudo Tecnico Preliminar (ETP)", "sigla": "ETP",
        "keywords": [
            "estudo tecnico preliminar","etp","estudo preliminar",
            "analise de viabilidade","analise de alternativas",
            "solucao de ti","necessidade da contratacao",
            "relevancia da contratacao","estudo de viabilidade"
        ]
    },
    "tr": {
        "label": "Termo de Referencia (TR)", "sigla": "TR",
        "keywords": [
            "termo de referencia","objeto da contratacao",
            "especificacao tecnica","criterio de aceitacao",
            "obrigacoes da contratada","obrigacoes da contratante",
            "modelo de execucao","forma de execucao","gestao do contrato",
            "prazo de execucao","quantitativo estimado"
        ]
    },
    "dfd": {
        "label": "Documento de Formalizacao de Demanda (DFD)", "sigla": "DFD",
        "keywords": [
            "documento de formalizacao de demanda","dfd",
            "formalizacao de demanda","setor requisitante",
            "justificativa da necessidade","necessidade do setor"
        ]
    },
    "pesquisa_precos": {
        "label": "Pesquisa de Precos", "sigla": "Pesquisa de Precos",
        "keywords": [
            "pesquisa de preco","pesquisa de mercado","mapa de precos",
            "cotacao de preco","levantamento de preco","painel de precos",
            "preco de referencia","mediana","fornecedor consultado",
            "menor preco","media de precos"
        ]
    },
    "mapa_riscos": {
        "label": "Mapa e Analise de Riscos", "sigla": "Mapa de Riscos",
        "keywords": [
            "mapa de risco","analise de risco","gerenciamento de risco",
            "matriz de risco","probabilidade","impacto","risco identificado",
            "mitigacao","contingencia","gestao de riscos"
        ]
    },
    "edital": {
        "label": "Edital de Licitacao", "sigla": "Edital",
        "keywords": [
            "edital","aviso de licitacao","aviso de pregao",
            "pregao eletronico","objeto do certame",
            "condicoes de participacao","criterio de julgamento",
            "habilitacao","impugnacao"
        ]
    },
    "parecer": {
        "label": "Parecer Juridico e Nota Tecnica", "sigla": "Parecer",
        "keywords": [
            "parecer juridico","nota juridica","analise juridica",
            "nota tecnica","despacho","manifestacao juridica",
            "pronunciamento","somos pelo deferimento","pelo indeferimento"
        ]
    },
    "contrato": {
        "label": "Contrato e Minuta de Contrato", "sigla": "Contrato",
        "keywords": [
            "minuta de contrato","instrumento contratual",
            "contratante","contratada","clausula","vigencia",
            "valor do contrato","nota de empenho","rescisao","penalidades"
        ]
    },
    "ata": {
        "label": "Ata de Registro de Precos e Sessao", "sigla": "Ata",
        "keywords": [
            "ata de registro de precos","ata de sessao",
            "sistema de registro de precos","item registrado","ata vigente"
        ]
    },
    "ratificacao": {
        "label": "Ato de Ratificacao e Autorizacao", "sigla": "Ratificacao",
        "keywords": [
            "ratifico","ratificacao","autorizacao de empenho",
            "autorizo","dispensa de licitacao","inexigibilidade",
            "homologo","homologacao","adjudico","adjudicacao"
        ]
    },
}

def normalizar(texto):
    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def classificar_documento(nome_arquivo, texto_inicio):
    nome_norm = normalizar(nome_arquivo)
    texto_norm = normalizar(texto_inicio[:1500] if texto_inicio else "")
    pontos = {cat: 0 for cat in CATEGORIAS}
    for cat, cfg in CATEGORIAS.items():
        for kw in cfg["keywords"]:
            kw_norm = normalizar(kw)
            if kw_norm in nome_norm:
                pontos[cat] += 3
            if kw_norm in texto_norm:
                pontos[cat] += 1
    melhor = max(pontos, key=pontos.get)
    return melhor if pontos[melhor] > 0 else "outros"

def extrair_metadados_caminho(caminho):
    meta = {"ano": None, "modalidade": None, "sequencial_compra": None, "sequencial_doc": None, "nome_original": caminho.name}
    for parte in caminho.parts:
        if re.match(r"^\d{4}_", parte):
            sp = parte.split("_", 1)
            meta["ano"] = sp[0]
            meta["modalidade"] = sp[1] if len(sp) > 1 else parte
        elif parte.isdigit() and meta["modalidade"]:
            meta["sequencial_compra"] = parte
    m = re.match(r"^(\d+)_", caminho.name)
    if m:
        meta["sequencial_doc"] = m.group(1)
    return meta

def extrair_texto(caminho):
    texto_total = []
    n_paginas = 0
    try:
        with pdfplumber.open(str(caminho)) as pdf:
            n_paginas = len(pdf.pages)
            for pg in pdf.pages:
                t = pg.extract_text()
                if t and t.strip():
                    texto_total.append(t.strip())
    except Exception as e:
        raise e
    return "\n\n".join(texto_total), n_paginas

def limpar_texto(texto):
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", texto)
    return texto.strip()

def gerar_markdown(caminho_pdf, categoria, texto, n_paginas, meta, idx_global):
    cfg = CATEGORIAS.get(categoria, {"label": "Outros", "sigla": "Outros"})
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    resumo = texto[:500].replace("\n", " ").strip() if texto else "Sem texto extraivel."
    if len(texto) > 500:
        resumo += "..."
    md = f"""---
id: doc_{idx_global:04d}
tipo: {cfg['sigla']}
categoria: {categoria}
modalidade: {meta.get('modalidade', 'N/A')}
ano: {meta.get('ano', 'N/A')}
sequencial_compra: {meta.get('sequencial_compra', 'N/A')}
sequencial_doc: {meta.get('sequencial_doc', 'N/A')}
arquivo_original: {meta.get('nome_original', caminho_pdf.name)}
paginas: {n_paginas}
orgao: TCE-PI
fonte: PNCP
extraido_em: {timestamp}
---

# {cfg['label']}

**Orgao:** Tribunal de Contas do Estado do Piaui (TCE-PI)
**Modalidade:** {meta.get('modalidade', 'N/A')}
**Ano:** {meta.get('ano', 'N/A')}
**Sequencial da Compra:** {meta.get('sequencial_compra', 'N/A')}
**Documento:** {meta.get('nome_original', caminho_pdf.name)}
**Paginas:** {n_paginas}
**Fonte:** Portal Nacional de Contratacoes Publicas (PNCP)

## Resumo

{resumo}

## Conteudo Completo

{texto if texto else '_Documento sem texto extraivel (PDF de imagem/escaneado)._'}

---
*Documento extraido do PNCP. Orgao: TCE-PI. Base legal: Lei 14.133/2021 e IN TCE-PI 02/2026.*
"""
    return md

def gerar_indice_jsonl(registros, saida):
    with open(saida, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def gerar_dataset_md(registros, saida):
    total = len(registros)
    cats, mods, anos = {}, {}, {}
    for r in registros:
        cats[r["categoria"]] = cats.get(r["categoria"], 0) + 1
        mods[r.get("modalidade","N/A")] = mods.get(r.get("modalidade","N/A"), 0) + 1
        anos[r.get("ano","N/A")] = anos.get(r.get("ano","N/A"), 0) + 1

    lines = [
        f"# Corpus de Artefatos de Contratacoes Publicas - TCE-PI",
        f"## Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        f"> **Fonte:** PNCP | **Orgao:** TCE-PI | **Total:** {total} documentos",
        f"> **Anos cobertos:** {', '.join(sorted([str(k) for k in anos.keys() if k is not None]))}",
        f"> **Finalidade:** Corpus de referencia para estudo e treinamento de IA em contratacoes publicas",
        f"> **Base legal:** Lei 14.133/2021 | IN TCE-PI 02/2026 | CNMP Portaria 151/2023",
        "",
        "---", "",
        "## Por Tipo de Artefato",
        "| Tipo | Sigla | Quantidade |",
        "| :--- | :--- | :--- |",
    ]
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        cfg = CATEGORIAS.get(cat, {"label": cat.upper(), "sigla": cat.upper()})
        lines.append(f"| {cfg['label']} | {cfg['sigla']} | {n} |")

    lines += ["", "## Por Modalidade", "| Modalidade | Quantidade |", "| :--- | :--- |"]
    for mod, n in sorted(mods.items(), key=lambda x: -x[1]):
        lines.append(f"| {mod} | {n} |")

    lines += ["", "## Por Ano", "| Ano | Quantidade |", "| :--- | :--- |"]
    for ano, n in sorted(anos.items()):
        lines.append(f"| {ano} | {n} |")

    lines += [
        "", "---", "",
        "## Indice Completo de Documentos",
        "| ID | Tipo | Modalidade | Ano | Seq | Arquivo |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in registros:
        nome = (r.get("arquivo_original") or "")[:45]
        lines.append(f"| `{r['id']}` | {r['sigla']} | {r.get('modalidade','?')} | {r.get('ano','?')} | {r.get('sequencial_compra','?')} | {nome} |")

    lines += ["", "---", "*Corpus para uso interno do MPPI - Mapeamento TCE-PI.*"]
    with open(saida, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def processar(pasta_pdfs, limite, verbose, incremental):
    import sys
    pasta = Path(pasta_pdfs)
    saida_base = Path("corpus_ia")
    saida_base.mkdir(exist_ok=True)
    for cat in list(CATEGORIAS.keys()) + ["outros"]:
        (saida_base / cat).mkdir(exist_ok=True)

    # Carregar indice existente se incremental
    indice_path = saida_base / "indice.jsonl"
    registros_existentes = set()
    registros = []
    if incremental and indice_path.exists():
        with open(indice_path, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                registros_existentes.add(r.get("arquivo_original",""))
                registros.append(r)
        print(f"  Modo incremental: {len(registros)} docs ja processados")

    pdfs = sorted(pasta.rglob("*.pdf"))
    if incremental:
        pdfs = [p for p in pdfs if p.name not in registros_existentes]
        print(f"  Novos PDFs a processar: {len(pdfs)}")
    if limite:
        pdfs = pdfs[:limite]
    total_novos = len(pdfs)
    idx_start = len(registros) + 1

    print(f"\n{'='*65}")
    print(f"  EXTRATOR DE ARTEFATOS - TCE-PI | Motor: {PDF_ENGINE}")
    print(f"  Pasta: {pasta_pdfs}")
    print(f"  PDFs novos: {total_novos} | Saida: corpus_ia/")
    print(f"{'='*65}\n")

    erros, contadores = [], {}

    for i, pdf_path in enumerate(pdfs, idx_start):
        idx_display = i - idx_start + 1
        if verbose or (idx_display % 25 == 0) or idx_display == 1 or idx_display == total_novos:
            pct = idx_display * 100 // total_novos if total_novos else 100
            print(f"  [{idx_display:3d}/{total_novos}] ({pct:3d}%) {pdf_path.name[:55]}")
        try:
            texto_bruto, n_paginas = extrair_texto(pdf_path)
            texto = limpar_texto(texto_bruto)
            categoria = classificar_documento(pdf_path.name, texto) if len(texto) > 20 else "outros"
            meta = extrair_metadados_caminho(pdf_path)
            cfg = CATEGORIAS.get(categoria, {"label": "Outros", "sigla": "Outros"})
            contadores[categoria] = contadores.get(categoria, 0) + 1
            seq = meta.get("sequencial_compra") or "000"
            seq_doc = meta.get("sequencial_doc") or str(i)
            ano = meta.get("ano") or "0000"
            nome_saida = f"{ano}_{seq}_{seq_doc}_{categoria}_{contadores[categoria]:03d}.md"
            md_content = gerar_markdown(pdf_path, categoria, texto, n_paginas, meta, i)
            saida_md = saida_base / categoria / nome_saida
            saida_md.write_text(md_content, encoding="utf-8")
            registros.append({
                "id": f"doc_{i:04d}",
                "sigla": cfg["sigla"],
                "categoria": categoria,
                "label": cfg["label"],
                "modalidade": meta.get("modalidade","N/A"),
                "ano": meta.get("ano","N/A"),
                "sequencial_compra": meta.get("sequencial_compra"),
                "sequencial_doc": meta.get("sequencial_doc"),
                "arquivo_original": meta.get("nome_original"),
                "paginas": n_paginas,
                "chars": len(texto),
                "arquivo_md": str(saida_md),
                "texto_resumo": texto[:300].replace("\n"," ") if texto else "",
            })
            if verbose:
                print(f"         OK [{cfg['sigla']}] {n_paginas}p -> {nome_saida}")
        except Exception as e:
            erros.append({"arquivo": str(pdf_path), "erro": str(e)})
            if verbose:
                print(f"         ERRO: {e}")

    # Re-contar contadores totais para o relatorio final
    cont_total = {}
    for r in registros:
        cont_total[r["categoria"]] = cont_total.get(r["categoria"], 0) + 1

    gerar_indice_jsonl(registros, indice_path)
    gerar_dataset_md(registros, saida_base / "dataset.md")

    print(f"\n{'='*65}")
    print(f"  EXTRACAO CONCLUIDA!")
    print(f"{'='*65}")
    print(f"  Total no corpus:  {len(registros)} docs")
    print(f"  Novos processados:{total_novos} | Erros: {len(erros)}")
    print(f"\n  Distribuicao total por categoria:")
    for cat, n in sorted(cont_total.items(), key=lambda x: -x[1]):
        cfg = CATEGORIAS.get(cat, {"label": cat.upper(), "sigla": cat})
        bar = "#" * min(n, 45)
        print(f"    {cfg['sigla']:30s} {n:4d}  {bar}")
    print(f"\n  corpus_ia/ pronto para uso em RAG/fine-tuning!")
    if erros:
        ep = saida_base / "erros_extracao.json"
        with open(ep, "w", encoding="utf-8") as f:
            json.dump(erros, f, indent=2, ensure_ascii=False)
        print(f"  Erros registrados em: {ep}")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai artefatos de contratacao dos PDFs PNCP-TCE-PI")
    parser.add_argument("--pasta", default="downloads/PNCP", help="Pasta raiz com PDFs (ex: downloads/PNCP)")
    parser.add_argument("--limite", type=int, default=None, help="Limitar a N documentos")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detalha cada arquivo")
    parser.add_argument("--incremental", "-i", action="store_true", help="Ignora arquivos ja processados")
    args = parser.parse_args()
    processar(args.pasta, args.limite, args.verbose, args.incremental)
