"""
validar_corpus.py
=================
Etapa 4 do Roadmap: Validacao de Integridade do Corpus para Treinamento de IA
Executa 5 modulos de analise e gera relatorio completo em corpus_ia/relatorio_qualidade.md

Modulos:
  1. Cobertura de texto      -- quais PDFs extrairam texto suficiente
  2. Encoding / corrompidos  -- deteccao de caracteres invalidos
  3. Classificacao           -- amostra de cada categoria para auditoria
  4. Metricas do corpus      -- estatisticas completas por ano/modalidade/categoria
  5. Teste RAG               -- busca semantica simples com TF-IDF (sem GPU)

Uso:
  python validar_corpus.py              # Executa todos os modulos
  python validar_corpus.py --modulo 1   # Executa apenas modulo especifico
"""

import os, re, json, argparse, unicodedata, warnings
from pathlib import Path
from datetime import datetime
from collections import defaultdict

warnings.filterwarnings("ignore")

CORPUS = Path("corpus_ia")
INDICE = CORPUS / "indice.jsonl"
RELATORIO = CORPUS / "relatorio_qualidade.md"

CATEGORIAS_LABEL = {
    "etp": "Estudo Tecnico Preliminar",
    "tr": "Termo de Referencia",
    "dfd": "Documento de Formalizacao de Demanda",
    "pesquisa_precos": "Pesquisa de Precos",
    "mapa_riscos": "Mapa de Riscos",
    "edital": "Edital",
    "parecer": "Parecer Juridico",
    "contrato": "Contrato / Minuta",
    "ratificacao": "Ratificacao / Autorizacao",
    "outros": "Outros",
}

def carregar_indice():
    with open(INDICE, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def ler_md(r):
    p = r.get("arquivo_md", "")
    if p and os.path.exists(p):
        return Path(p).read_text(encoding="utf-8", errors="replace")
    return ""

# ─────────────────────────────────────────────────
# MODULO 1 — COBERTURA DE TEXTO
# ─────────────────────────────────────────────────
def modulo_cobertura(registros):
    print("\n[1/5] Analisando cobertura de texto...")
    sem_texto, pouco, ok = [], [], []
    for r in registros:
        chars = r.get("chars", 0) or 0
        if chars < 100:
            sem_texto.append(r)
        elif chars < 500:
            pouco.append(r)
        else:
            ok.append(r)

    total = len(registros)
    resultado = {
        "total": total,
        "sem_texto": sem_texto,
        "pouco_texto": pouco,
        "texto_ok": ok,
        "pct_sem": round(len(sem_texto)*100/total, 1),
        "pct_pouco": round(len(pouco)*100/total, 1),
        "pct_ok": round(len(ok)*100/total, 1),
    }

    print(f"  OK (>=500 chars):   {len(ok)} ({resultado['pct_ok']}%)")
    print(f"  Pouco (100-499):    {len(pouco)} ({resultado['pct_pouco']}%)")
    print(f"  Sem texto (<100):   {len(sem_texto)} ({resultado['pct_sem']}%)")

    if sem_texto:
        print(f"\n  Candidatos a OCR ({len(sem_texto)} arquivos):")
        for r in sem_texto[:8]:
            print(f"    [{r.get('categoria','?')}] {r.get('arquivo_original','?')[:55]}")

    return resultado

# ─────────────────────────────────────────────────
# MODULO 2 — ENCODING / CARACTERES CORROMPIDOS
# ─────────────────────────────────────────────────
def modulo_encoding(registros):
    print("\n[2/5] Verificando encoding e caracteres corrompidos...")

    PADRAO_CORR = re.compile(r"[^\x09\x0A\x0D\x20-\x7E\u00C0-\u024F\u0300-\u036F\u2013\u2014\u2019\u201C\u201D\n\r\t ]")
    docs_corrompidos = []
    total_chars = 0
    total_corrompidos = 0

    for r in registros:
        txt = ler_md(r)
        if not txt:
            continue
        corrupto = len(PADRAO_CORR.findall(txt))
        total_chars += len(txt)
        total_corrompidos += corrupto
        if corrupto > 10:
            docs_corrompidos.append({
                "id": r["id"],
                "categoria": r.get("categoria"),
                "arquivo": r.get("arquivo_original","")[:50],
                "chars_corrompidos": corrupto,
                "pct": round(corrupto*100/max(len(txt),1), 2),
            })

    docs_corrompidos.sort(key=lambda x: -x["chars_corrompidos"])
    pct_global = round(total_corrompidos*100/max(total_chars,1), 3)

    print(f"  Total de caracteres analisados: {total_chars:,}")
    print(f"  Caracteres suspeitos:           {total_corrompidos:,} ({pct_global}%)")
    print(f"  Docs com encoding ruim (>10):   {len(docs_corrompidos)}")

    if docs_corrompidos:
        print(f"\n  Top 5 com mais corrompidos:")
        for d in docs_corrompidos[:5]:
            print(f"    [{d['categoria']}] {d['arquivo']} -> {d['chars_corrompidos']} chars ({d['pct']}%)")

    return {
        "total_chars": total_chars,
        "total_corrompidos": total_corrompidos,
        "pct_global": pct_global,
        "docs_corrompidos": docs_corrompidos,
    }

# ─────────────────────────────────────────────────
# MODULO 3 — AUDITORIA DA CLASSIFICACAO
# ─────────────────────────────────────────────────
def modulo_classificacao(registros):
    print("\n[3/5] Auditando qualidade da classificacao automatica...")
    import random
    random.seed(42)

    por_cat = defaultdict(list)
    for r in registros:
        por_cat[r.get("categoria","outros")].append(r)

    amostra = []
    suspeitos = []

    for cat, docs in sorted(por_cat.items()):
        n_amostra = max(1, min(3, len(docs)))
        sample = random.sample(docs, n_amostra)
        for r in sample:
            txt = ler_md(r)
            resumo = txt[txt.find("## Resumo"):txt.find("## Resumo")+300] if "## Resumo" in txt else txt[:200]
            resumo_limpo = re.sub(r"\s+", " ", resumo).strip()[:150]
            amostra.append({
                "cat": cat,
                "arquivo": r.get("arquivo_original","")[:45],
                "resumo": resumo_limpo,
                "chars": r.get("chars",0),
            })

        # Detectar possiveis erros: "outros" com muito texto (provavelmente classificavel)
        for r in docs:
            if cat == "outros" and r.get("chars",0) > 1000:
                suspeitos.append(r)

    print(f"  Categorias encontradas: {len(por_cat)}")
    for cat, docs in sorted(por_cat.items(), key=lambda x: -len(x[1])):
        label = CATEGORIAS_LABEL.get(cat, cat)
        print(f"    {label:35s} {len(docs):4d} docs")

    if suspeitos:
        print(f"\n  ATENCAO: {len(suspeitos)} docs em 'outros' com texto substancial (possivelmente mal classificados)")
        for r in suspeitos[:5]:
            resumo = ler_md(r)[:100].replace("\n"," ")
            print(f"    {r.get('arquivo_original','')[:50]} | {resumo[:80]}")

    return {"por_categoria": {k: len(v) for k,v in por_cat.items()}, "suspeitos_outros": len(suspeitos), "amostra": amostra}

# ─────────────────────────────────────────────────
# MODULO 4 — METRICAS COMPLETAS DO CORPUS
# ─────────────────────────────────────────────────
def modulo_metricas(registros):
    print("\n[4/5] Calculando metricas completas do corpus...")

    total = len(registros)
    total_chars = sum(r.get("chars",0) or 0 for r in registros)
    total_paginas = sum(int(r.get("paginas",0) or 0) for r in registros)
    media_chars = total_chars // total if total else 0
    media_pags = round(total_paginas / total, 1) if total else 0

    por_ano = defaultdict(int)
    por_mod = defaultdict(int)
    por_cat = defaultdict(int)
    chars_por_cat = defaultdict(int)
    pags_por_cat = defaultdict(int)

    for r in registros:
        por_ano[r.get("ano","?")] += 1
        por_mod[r.get("modalidade","?")] += 1
        por_cat[r.get("categoria","?")] += 1
        chars_por_cat[r.get("categoria","?")] += r.get("chars",0) or 0
        pags_por_cat[r.get("categoria","?")] += int(r.get("paginas",0) or 0)

    print(f"  Total de documentos:    {total}")
    print(f"  Total de paginas:       {total_paginas:,}")
    print(f"  Total de caracteres:    {total_chars:,}")
    print(f"  Media chars/doc:        {media_chars:,}")
    print(f"  Media paginas/doc:      {media_pags}")

    print(f"\n  Por ano:")
    for a, n in sorted(por_ano.items()):
        print(f"    {a}: {n} docs")

    print(f"\n  Por modalidade:")
    for m, n in sorted(por_mod.items(), key=lambda x: -x[1]):
        print(f"    {n:4d}  {m}")

    return {
        "total": total,
        "total_chars": total_chars,
        "total_paginas": total_paginas,
        "media_chars": media_chars,
        "media_pags": media_pags,
        "por_ano": dict(por_ano),
        "por_modalidade": dict(por_mod),
        "por_categoria": dict(por_cat),
        "chars_por_cat": dict(chars_por_cat),
        "pags_por_cat": dict(pags_por_cat),
    }

# ─────────────────────────────────────────────────
# MODULO 5 — TESTE RAG COM TF-IDF
# ─────────────────────────────────────────────────
def modulo_rag(registros):
    print("\n[5/5] Executando teste RAG (TF-IDF sem GPU)...")
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
    except ImportError:
        print("  scikit-learn nao disponivel. Pulando teste RAG.")
        return {"status": "sklearn_ausente"}

    # Carregar textos (resumos do indice)
    textos = []
    meta_docs = []
    for r in registros:
        resumo = r.get("texto_resumo","") or ""
        if len(resumo) > 50:
            textos.append(resumo)
            meta_docs.append(r)

    if not textos:
        print("  Nenhum resumo disponivel.")
        return {"status": "sem_resumos"}

    print(f"  Indexando {len(textos)} documentos com TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2), min_df=2)
    matriz = vectorizer.fit_transform(textos)
    print(f"  Indice criado: {matriz.shape[0]} docs x {matriz.shape[1]} termos")

    # Queries de teste
    queries = [
        "estudo tecnico preliminar servicos de tecnologia da informacao",
        "pesquisa de precos fornecedores cotacao mercado",
        "termo de referencia objeto contratacao quantitativo",
        "mapa de riscos probabilidade impacto mitigacao",
        "pregao eletronico edital habilitacao julgamento",
        "dispensa de licitacao autorizacao empenho",
    ]

    resultados_rag = []
    print(f"\n  Resultados da busca semantica TF-IDF:")
    print(f"  {'Query':<45} {'Top resultado':<45} {'Score'}")
    print(f"  {'-'*45} {'-'*45} {'-'*5}")

    for q in queries:
        q_vec = vectorizer.transform([q])
        sims = cosine_similarity(q_vec, matriz).flatten()
        top_idx = np.argsort(sims)[::-1][:3]
        top = meta_docs[top_idx[0]]
        score = round(float(sims[top_idx[0]]), 3)
        nome = (top.get("arquivo_original","") or "")[:42]
        cat = top.get("categoria","?")
        print(f"  {q[:43]:<45} [{cat}] {nome:<40} {score}")
        resultados_rag.append({
            "query": q,
            "resultado_top": nome,
            "categoria": cat,
            "score": score,
        })

    scores = [r["score"] for r in resultados_rag]
    media_score = round(sum(scores)/len(scores), 3)
    print(f"\n  Score medio de relevancia: {media_score}")
    return {"status": "ok", "n_docs_indexados": len(textos), "media_score": media_score, "resultados": resultados_rag}

# ─────────────────────────────────────────────────
# GERADOR DO RELATORIO .md
# ─────────────────────────────────────────────────
def gerar_relatorio(m1, m2, m3, m4, m5):
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    total = m4["total"]

    pct_ok = m1["pct_ok"]
    pct_ocr = m1["pct_sem"]
    enc_pct = m2["pct_global"]
    rag_score = m5.get("media_score","N/A") if m5.get("status") == "ok" else "N/A"

    if pct_ok >= 85 and enc_pct < 1.0 and (m5.get("status") == "ok" and rag_score > 0.1):
        nota_geral = "BOM"
        nota_emoji = "APROVADO"
    elif pct_ok >= 70:
        nota_geral = "REGULAR"
        nota_emoji = "APROVADO COM RESSALVAS"
    else:
        nota_geral = "INSATISFATORIO"
        nota_emoji = "REQUER CORRECOES"

    linhas = [
        f"# Relatorio de Qualidade do Corpus — TCE-PI",
        f"## Gerado em: {ts}",
        "",
        f"> **Avaliacao geral:** {nota_geral} — {nota_emoji}",
        f"> **Total de documentos auditados:** {total}",
        "",
        "---", "",
        "## 1. Cobertura de Texto",
        "",
        "| Nivel | Quantidade | % |",
        "| :--- | :--- | :--- |",
        f"| Texto suficiente (>=500 chars) | {m1['texto_ok'].__len__()} | {m1['pct_ok']}% |",
        f"| Pouco texto (100-499 chars) | {m1['pouco_texto'].__len__()} | {m1['pct_pouco']}% |",
        f"| Sem texto (<100 chars) — candidatos a OCR | {m1['sem_texto'].__len__()} | {m1['pct_sem']}% |",
        "",
    ]
    if m1["sem_texto"]:
        linhas += ["### Candidatos a OCR (PDFs digitalizados/escaneados)", ""]
        linhas += ["| Categoria | Arquivo |", "| :--- | :--- |"]
        for r in m1["sem_texto"][:20]:
            linhas.append(f"| {r.get('categoria','?')} | {r.get('arquivo_original','?')[:60]} |")

    linhas += [
        "", "---", "",
        "## 2. Encoding e Caracteres Corrompidos",
        "",
        f"- **Total de caracteres analisados:** {m2['total_chars']:,}",
        f"- **Caracteres suspeitos:** {m2['total_corrompidos']:,} ({m2['pct_global']}%)",
        f"- **Documentos com encoding ruim (>10 chars suspeitos):** {len(m2['docs_corrompidos'])}",
        "",
    ]
    if m2["docs_corrompidos"]:
        linhas += ["| Categoria | Arquivo | Chars corrompidos | % |", "| :--- | :--- | :--- | :--- |"]
        for d in m2["docs_corrompidos"][:15]:
            linhas.append(f"| {d['categoria']} | {d['arquivo']} | {d['chars_corrompidos']} | {d['pct']}% |")

    linhas += [
        "", "---", "",
        "## 3. Auditoria da Classificacao Automatica",
        "",
        "| Categoria | Documentos |",
        "| :--- | :--- |",
    ]
    for cat, n in sorted(m3["por_categoria"].items(), key=lambda x: -x[1]):
        label = CATEGORIAS_LABEL.get(cat, cat)
        linhas.append(f"| {label} | {n} |")

    if m3["suspeitos_outros"] > 0:
        linhas += [
            "",
            f"> **Atencao:** {m3['suspeitos_outros']} documentos classificados como 'outros' possuem texto substancial e podem estar mal classificados. Revisar manualmente.",
        ]

    linhas += ["", "### Amostra de Documentos por Categoria (auditoria manual)", ""]
    cat_atual = ""
    for a in m3["amostra"]:
        if a["cat"] != cat_atual:
            cat_atual = a["cat"]
            label = CATEGORIAS_LABEL.get(cat_atual, cat_atual)
            linhas += [f"\n#### {label}", ""]
        linhas.append(f"- **{a['arquivo']}** ({a['chars']} chars)")
        linhas.append(f"  > {a['resumo'][:120]}")

    linhas += [
        "", "---", "",
        "## 4. Metricas Completas do Corpus",
        "",
        f"| Metrica | Valor |",
        "| :--- | :--- |",
        f"| Total de documentos | {m4['total']} |",
        f"| Total de paginas | {m4['total_paginas']:,} |",
        f"| Total de caracteres | {m4['total_chars']:,} |",
        f"| Media de chars por documento | {m4['media_chars']:,} |",
        f"| Media de paginas por documento | {m4['media_pags']} |",
        "",
        "| Ano | Documentos |", "| :--- | :--- |",
    ]
    for a, n in sorted(m4["por_ano"].items()):
        linhas.append(f"| {a} | {n} |")

    linhas += ["", "| Modalidade | Documentos |", "| :--- | :--- |"]
    for m, n in sorted(m4["por_modalidade"].items(), key=lambda x: -x[1]):
        linhas.append(f"| {m} | {n} |")

    linhas += ["", "| Categoria | Docs | Total chars | Media chars/doc | Media pags |", "| :--- | :--- | :--- | :--- | :--- |"]
    for cat, n in sorted(m4["por_categoria"].items(), key=lambda x: -x[1]):
        label = CATEGORIAS_LABEL.get(cat, cat)
        tchars = m4["chars_por_cat"].get(cat, 0)
        tpags = m4["pags_por_cat"].get(cat, 0)
        mchars = tchars // n if n else 0
        mpags = round(tpags / n, 1) if n else 0
        linhas.append(f"| {label} | {n} | {tchars:,} | {mchars:,} | {mpags} |")

    linhas += [
        "", "---", "",
        "## 5. Teste RAG (Busca Semantica TF-IDF)",
        "",
    ]
    if m5.get("status") == "ok":
        linhas += [
            f"- **Documentos indexados:** {m5['n_docs_indexados']}",
            f"- **Score medio de relevancia:** {m5['media_score']} (escala 0-1)",
            "",
            "| Query de Teste | Resultado Top | Categoria | Score |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for r in m5["resultados"]:
            linhas.append(f"| {r['query'][:45]} | {r['resultado_top'][:40]} | {r['categoria']} | {r['score']} |")

        if m5["media_score"] >= 0.15:
            linhas += ["", "> **Avaliacao RAG:** Score acima de 0.15 — corpus adequado para recuperacao semantica com TF-IDF. Para uso com LLMs, recomenda-se embeddings densos (sentence-transformers)."]
        else:
            linhas += ["", "> **Avaliacao RAG:** Score baixo — considerar melhorar a extração de texto e a limpeza dos documentos antes do uso em RAG com LLMs."]
    else:
        linhas += [f"> sklearn nao disponivel — teste RAG nao executado. Instale com: pip install scikit-learn"]

    linhas += [
        "", "---", "",
        "## Conclusao e Recomendacoes",
        "",
        f"**Avaliacao geral: {nota_geral} — {nota_emoji}**", "",
        "| # | Recomendacao | Prioridade |",
        "| :--- | :--- | :--- |",
    ]
    if m1["pct_sem"] > 5:
        linhas.append(f"| 1 | Aplicar OCR nos {m1['sem_texto'].__len__()} PDFs sem texto (instalar Tesseract + pytesseract) | Alta |")
    if m2["pct_global"] > 0.5:
        linhas.append(f"| 2 | Corrigir encoding: {len(m2['docs_corrompidos'])} docs com chars suspeitos | Media |")
    if m3["suspeitos_outros"] > 0:
        linhas.append(f"| 3 | Revisar {m3['suspeitos_outros']} docs em 'outros' com texto substancial | Media |")
    linhas.append("| 4 | Substituir TF-IDF por sentence-transformers para RAG com LLMs | Baixa |")
    linhas.append("| 5 | Testar corpus em LLM real (ex: Gemini, GPT) com perguntas sobre contratacoes | Baixa |")

    linhas += ["", "---", "*Relatorio gerado automaticamente pelo validar_corpus.py*"]

    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"\nRelatorio salvo em: {RELATORIO}")


# ─────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modulo", type=int, default=0, help="Executar apenas modulo N (1-5)")
    args = parser.parse_args()

    print("="*65)
    print("  VALIDACAO DE INTEGRIDADE DO CORPUS — TCE-PI")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*65)

    registros = carregar_indice()
    print(f"  {len(registros)} documentos carregados do indice")

    if args.modulo == 0 or args.modulo == 1:
        m1 = modulo_cobertura(registros)
    else:
        m1 = {"sem_texto":[], "pouco_texto":[], "texto_ok":[], "pct_sem":0, "pct_pouco":0, "pct_ok":0}

    if args.modulo == 0 or args.modulo == 2:
        m2 = modulo_encoding(registros)
    else:
        m2 = {"total_chars":0,"total_corrompidos":0,"pct_global":0,"docs_corrompidos":[]}

    if args.modulo == 0 or args.modulo == 3:
        m3 = modulo_classificacao(registros)
    else:
        m3 = {"por_categoria":{},"suspeitos_outros":0,"amostra":[]}

    if args.modulo == 0 or args.modulo == 4:
        m4 = modulo_metricas(registros)
    else:
        m4 = {"total":0,"total_chars":0,"total_paginas":0,"media_chars":0,"media_pags":0,"por_ano":{},"por_modalidade":{},"por_categoria":{},"chars_por_cat":{},"pags_por_cat":{}}

    if args.modulo == 0 or args.modulo == 5:
        m5 = modulo_rag(registros)
    else:
        m5 = {"status":"pulado"}

    if args.modulo == 0:
        gerar_relatorio(m1, m2, m3, m4, m5)

    print("\n" + "="*65)
    print("  VALIDACAO CONCLUIDA!")
    print("="*65)

if __name__ == "__main__":
    main()
