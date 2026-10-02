import os
import sys
import json
import time
import re
from pathlib import Path
import pdfplumber
from src.pncp_client import PNCPClient

sys.stdout.reconfigure(encoding="utf-8")

client = PNCPClient()
CNPJ_MPPI = "05805924000189"

modalidades = [
    (6, "Pregão Eletrônico", "pregao"),
    (8, "Dispensa de Licitação", "dispensa"),
    (9, "Inexigibilidade de Licitação", "inexigibilidade")
]

def categorizar_arquivo(titulo: str, tipo_nome: str) -> tuple:
    txt = (titulo + " " + tipo_nome).lower()
    if any(k in txt for k in ["termo de refer", " tr ", "tr_", "projeto basico"]):
        return "tr", "Termo de Referência"
    if any(k in txt for k in ["estudo t", "etp"]):
        return "etp", "Estudo Técnico Preliminar"
    if any(k in txt for k in ["edital", "aviso de licit", "aviso de dispensa"]):
        return "edital", "Edital / Aviso Convocatório"
    if any(k in txt for k in ["contrato", "minuta", "termo aditivo", "rescisao"]):
        return "contrato", "Contrato / Minuta"
    if any(k in txt for k in ["dfd", "dod", "formalizacao da demanda", "oficializacao"]):
        return "dfd", "Documento de Formalização da Demanda"
    if any(k in txt for k in ["risco", "matriz"]):
        return "mapa_riscos", "Mapa / Matriz de Riscos"
    if any(k in txt for k in ["parecer", "despacho", "nota tecnica"]):
        return "parecer", "Parecer / Despacho Jurídico"
    if any(k in txt for k in ["pesquisa", "preco", "cotacao", "mapa comparativo"]):
        return "pesquisa_precos", "Pesquisa de Preços"
    if any(k in txt for k in ["ratificacao", "homologacao", "adjudicacao", "autorizacao"]):
        return "ratificacao", "Autorização / Ratificação"
    return "outros", "Outros Documentos"

def sanitizar(nome: str) -> str:
    for c in [":", "?", '"', "<", ">", "|", "*", "/", "\\"]:
        nome = nome.replace(c, "_")
    return nome[:80].strip()

def converter_pdf_para_md(pdf_path: str, meta: dict, saida_base: Path) -> dict:
    try:
        texto_paginas = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pags = len(pdf.pages)
            for i, p in enumerate(pdf.pages):
                txt = p.extract_text() or ""
                if txt.strip():
                    texto_paginas.append(f"<!-- Pagina {i+1} -->\n{txt.strip()}")
        
        if not texto_paginas:
            return None
            
        conteudo_completo = "\n\n".join(texto_paginas)
        resumo = texto_paginas[0][:500].replace("\n", " ").strip()
        
        cat_slug = meta["categoria"]
        cat_dir = saida_base / cat_slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        md_nome = f"mppi_{meta['ano']}_{meta['num_compra']}_{meta['seq_compra']}_{meta['seq_doc']}_{cat_slug}.md"
        md_path = cat_dir / md_nome
        
        frontmatter = f"""---
id: {meta['id']}
tipo: {meta['label']}
categoria: {cat_slug}
modalidade: {meta['modalidade']}
ano: {meta['ano']}
sequencial_compra: {meta['seq_compra']}
sequencial_doc: {meta['seq_doc']}
arquivo_original: {os.path.basename(pdf_path)}
paginas: {total_pags}
orgao: MPPI
fonte: PNCP
objeto: {meta.get('objeto', '')}
valor_estimado: {meta.get('valor', 0)}
---

# {meta['label']} - MPPI ({meta['num_compra']}/{meta['ano']})

**Órgão:** Ministério Público do Estado do Piauí (MPPI)
**Modalidade:** {meta['modalidade']}
**Objeto:** {meta.get('objeto', '')}
**Valor Estimado:** R$ {meta.get('valor', 0):,.2f}
**Arquivo:** {os.path.basename(pdf_path)}

## Resumo Inicial
{resumo}

## Conteúdo Integral
{conteudo_completo}
"""
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(frontmatter)
            
        return {
            "id": meta["id"],
            "sigla": meta["label"],
            "categoria": cat_slug,
            "label": meta["label"],
            "modalidade": meta["modalidade"],
            "ano": str(meta["ano"]),
            "orgao": "MPPI",
            "sequencial_compra": str(meta["seq_compra"]),
            "sequencial_doc": str(meta["seq_doc"]),
            "arquivo_original": os.path.basename(pdf_path),
            "paginas": str(total_pags),
            "chars": len(conteudo_completo),
            "arquivo_md": str(md_path),
            "texto_resumo": resumo
        }
    except Exception as e:
        print(f"    [!] Erro ao converter PDF {pdf_path}: {e}")
        return None

def executar_extracao():
    saida_base = Path("corpus_ia")
    indice_path = saida_base / "indice.jsonl"
    
    # Obter proximo id
    ultimo_id = 2000
    if indice_path.exists():
        with open(indice_path, "r", encoding="utf-8") as f:
            for l in f:
                try:
                    d = json.loads(l)
                    doc_id = d.get("id", "")
                    if doc_id.startswith("doc_"):
                        num = int(doc_id.replace("doc_", ""))
                        if num > ultimo_id:
                            ultimo_id = num
                except Exception:
                    pass
                    
    novo_id_counter = ultimo_id + 1
    total_novos_docs = 0

    for ano in [2025, 2026]:
        print(f"\n{'='*70}\n>>> INICIANDO PROCESSAMENTO MPPI PARA O ANO {ano} <<<\n{'='*70}")
        compras_ano = []
        
        for mod_cod, mod_nome, mod_slug in modalidades:
            print(f"\n[*] Consultando {mod_nome} (ano {ano})...")
            pagina = 1
            tot_reg = 1
            coletados = 0
            
            while coletados < tot_reg:
                try:
                    res = client.consultar_contratacoes(CNPJ_MPPI, ano, mod_cod, pagina=pagina, tamanho_pagina=50)
                except Exception as e:
                    print(f"  [!] Erro ao consultar pagina {pagina}: {e}. Aguardando 10s...")
                    time.sleep(10)
                    continue
                    
                if pagina == 1:
                    tot_reg = res.get("totalRegistros", 0)
                    print(f"  -> Total de certames no PNCP: {tot_reg}")
                    if tot_reg == 0:
                        break
                        
                items = res.get("data", [])
                if not items:
                    break
                    
                for it in items:
                    coletados += 1
                    seq = it.get("sequencialCompra")
                    num = it.get("numeroCompra")
                    obj = it.get("objetoCompra", "")
                    val = it.get("valorTotalEstimado", 0.0)
                    
                    time.sleep(0.8) # rate-limiting
                    try:
                        arquivos = client.listar_arquivos_contratacao(CNPJ_MPPI, ano, seq)
                    except Exception:
                        arquivos = []
                        
                    registro = {
                        "modalidade": mod_nome,
                        "codigo_modalidade": mod_cod,
                        "numero_compra": num,
                        "ano": ano,
                        "sequencial_pncp": seq,
                        "numero_controle_pncp": it.get("numeroControlePNCP"),
                        "objeto": obj,
                        "valor_estimado": val,
                        "total_arquivos": len(arquivos),
                        "arquivos": []
                    }
                    
                    pasta_compra = Path(f"downloads/mppi_pncp_{ano}/{sanitizar(str(num))}_{seq}")
                    pasta_compra.mkdir(parents=True, exist_ok=True)
                    
                    for a in arquivos:
                        seq_doc = a.get("sequencialDocumento")
                        tipo_doc = a.get("tipoDocumentoNome") or a.get("tipoDocumentoId") or "Documento"
                        titulo = sanitizar(a.get("titulo") or f"doc_{seq_doc}")
                        url_download = f"{client.BASE_PNCP}/orgaos/{CNPJ_MPPI}/compras/{ano}/{seq}/arquivos/{seq_doc}"
                        
                        nome_pdf = f"{sanitizar(str(tipo_doc))}_{titulo}.pdf"
                        pdf_path = pasta_compra / nome_pdf
                        
                        registro["arquivos"].append({
                            "sequencial_documento": seq_doc,
                            "tipo": tipo_doc,
                            "titulo": titulo,
                            "url_download": url_download,
                            "arquivo_local": str(pdf_path)
                        })
                        
                        # Download do PDF se nao existir
                        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
                            print(f"    [+] Baixando: [{num}/{ano}] {tipo_doc}: {titulo[:35]}")
                            try:
                                client.baixar_arquivo(CNPJ_MPPI, ano, seq, seq_doc, str(pdf_path))
                                time.sleep(0.7)
                            except Exception as err:
                                print(f"        [!] Erro no download: {err}")
                                
                        # Converter para Markdown e indexar no RAG
                        if pdf_path.exists() and pdf_path.stat().st_size > 0:
                            cat_slug, cat_label = categorizar_arquivo(titulo, str(tipo_doc))
                            doc_meta = {
                                "id": f"doc_{novo_id_counter:04d}",
                                "label": cat_label,
                                "categoria": cat_slug,
                                "modalidade": mod_nome,
                                "ano": ano,
                                "num_compra": num,
                                "seq_compra": seq,
                                "seq_doc": seq_doc,
                                "objeto": obj,
                                "valor": val
                            }
                            idx_item = converter_pdf_para_md(str(pdf_path), doc_meta, saida_base)
                            if idx_item:
                                novo_id_counter += 1
                                total_novos_docs += 1
                                with open(indice_path, "a", encoding="utf-8") as f_idx:
                                    f_idx.write(json.dumps(idx_item, ensure_ascii=False) + "\n")
                                    
                    compras_ano.append(registro)
                    print(f"  [{coletados}/{tot_reg}] Compra {num}/{ano} processada ({len(arquivos)} arquivos)")
                    
                pagina += 1
                
        # Salva o JSON consolidado do ano
        with open(f"contratacoes_mppi_pncp_{ano}.json", "w", encoding="utf-8") as f_json:
            json.dump(compras_ano, f_json, ensure_ascii=False, indent=2)
        print(f"\n[OK] Salvo contratacoes_mppi_pncp_{ano}.json com {len(compras_ano)} compras.")

    print(f"\n{'='*70}\n[CONCLUÍDO COM SUCESSO!]")
    print(f"Total de novos documentos adicionados ao acervo RAG: {total_novos_docs}")
    print(f"{'='*70}")

if __name__ == "__main__":
    executar_extracao()
