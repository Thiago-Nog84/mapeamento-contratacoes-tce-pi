import json
import os

mppi_files = set()
for root, dirs, files in os.walk("downloads/mppi_pncp_2024"):
    for f in files:
        mppi_files.add(f)

updated_docs = []
mppi_tagged = 0

with open("corpus_ia/indice.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        orig = doc.get("arquivo_original", "")
        if orig in mppi_files or "mppi" in doc.get("arquivo_md", "").lower():
            doc["orgao"] = "MPPI"
            doc["ano"] = "2024"
            mppi_tagged += 1
        elif doc.get("orgao") is None or doc.get("orgao") == "desconhecido":
            doc["orgao"] = "TCE-PI"
        updated_docs.append(doc)

with open("corpus_ia/indice.jsonl", "w", encoding="utf-8") as f:
    for doc in updated_docs:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"Sucesso! Total docs: {len(updated_docs)} | Tagged MPPI: {mppi_tagged} | TCE-PI: {len(updated_docs) - mppi_tagged}")
