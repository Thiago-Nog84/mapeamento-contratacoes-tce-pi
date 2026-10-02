import json
import os
import glob

print("=== 1. Arquivos baixados no disco ===")
mppi_folders = glob.glob("downloads/mppi_pncp_2024/*")
total_pdfs = 0
for f in mppi_folders:
    pdfs = [p for p in os.listdir(f) if p.endswith(".pdf")]
    total_pdfs += len(pdfs)
print(f"Total de processos MPPI com pastas: {len(mppi_folders)}")
print(f"Total de PDFs baixados no disco para MPPI: {total_pdfs}")

print("\n=== 2. Mapeamento no JSON de 2024 ===")
with open("contratacoes_mppi_pncp_2024.json", "r", encoding="utf-8") as f:
    mppi_2024 = json.load(f)
total_arquivos_previstos = sum(len(c.get("arquivos", [])) for c in mppi_2024)
print(f"Total de compras mapeadas no PNCP (2024): {len(mppi_2024)}")
print(f"Total de arquivos listados na API do PNCP: {total_arquivos_previstos}")

print("\n=== 3. Corpus RAG (corpus_ia) ===")
with open("corpus_ia/indice.jsonl", "r", encoding="utf-8") as f:
    docs = [json.loads(line) for line in f]
print(f"Total de documentos no índice RAG: {len(docs)}")

# Verificar quantos vieram dos PDFs do MPPI
mppi_in_rag = []
for d in docs:
    txt = d.get("arquivo_original", "") + " " + d.get("arquivo_md", "") + " " + d.get("texto_resumo", "")
    if any(k in txt.lower() for k in ["mppi", "procuradoria-geral de justiça", "ministério público do estado do piauí", "fll. 0"]):
        mppi_in_rag.append(d)

print(f"Documentos do MPPI identificados no RAG: {len(mppi_in_rag)}")
