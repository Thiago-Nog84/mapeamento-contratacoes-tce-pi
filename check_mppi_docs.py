import os
import json
import glob

print("=== Arquivos MPPI em downloads/mppi_pncp_2024 ===")
mppi_dirs = glob.glob("downloads/mppi_pncp_2024/*")
print(f"Total de processos MPPI baixados: {len(mppi_dirs)}")
proc_summary = []
for d in mppi_dirs[:15]:
    files = os.listdir(d)
    proc_summary.append((os.path.basename(d), len(files), [f[:40] for f in files[:4]]))

for p, n, sample in proc_summary:
    print(f"  {p} ({n} arquivos): {sample}")

print("\n=== Documentos MPPI em corpus_ia/indice.jsonl ===")
with open("corpus_ia/indice.jsonl", "r", encoding="utf-8") as f:
    mppi_indexed = []
    for line in f:
        doc = json.loads(line)
        # se orgao for MPPI ou caminho tiver mppi
        if doc.get("orgao") == "MPPI" or "mppi" in doc.get("arquivo_md", "").lower() or "mppi" in doc.get("arquivo_original", "").lower():
            mppi_indexed.append(doc)

print(f"Total indexados com marcação direta MPPI: {len(mppi_indexed)}")
if mppi_indexed:
    for doc in mppi_indexed[:5]:
        print(f"  [{doc.get('categoria')}] {doc.get('arquivo_original')} | {doc.get('arquivo_md')}")
