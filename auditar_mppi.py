import os
import json
import glob
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("="*75)
print("AUDITORIA CONCILIADA: DADOS DO MPPI MAPEADOS vs ARMAZENADOS EM DISCO")
print("="*75)

anos = [2024, 2025, 2026]

resumo = {}

for ano in anos:
    json_path = f"contratacoes_mppi_pncp_{ano}.json"
    pasta_download = f"downloads/mppi_pncp_{ano}"
    
    if not os.path.exists(json_path):
        print(f"[!] JSON {json_path} não encontrado!")
        continue
        
    with open(json_path, "r", encoding="utf-8") as f:
        compras = json.load(f)
        
    total_compras_json = len(compras)
    total_arquivos_json = sum(len(c.get("arquivos", [])) for c in compras)
    
    # Checagem em disco
    pastas_disco = glob.glob(f"{pasta_download}/*")
    total_pastas_disco = len(pastas_disco)
    
    arquivos_disco = []
    arquivos_zerados = []
    arquivos_zip = []
    arquivos_pdf = []
    
    for root, dirs, files in os.walk(pasta_download):
        for file in files:
            fp = os.path.join(root, file)
            sz = os.path.getsize(fp)
            arquivos_disco.append(fp)
            if sz == 0:
                arquivos_zerados.append(fp)
            else:
                try:
                    with open(fp, "rb") as check_f:
                        magic = check_f.read(4)
                    if magic.startswith(b"PK"):
                        arquivos_zip.append(fp)
                    elif magic.startswith(b"%PDF"):
                        arquivos_pdf.append(fp)
                except Exception:
                    pass
                    
    resumo[ano] = {
        "compras_json": total_compras_json,
        "pastas_disco": total_pastas_disco,
        "arqs_previstos_json": total_arquivos_json,
        "arqs_totais_disco": len(arquivos_disco),
        "arqs_zerados": len(arquivos_zerados),
        "arqs_zip_pacotes": len(arquivos_zip),
        "arqs_pdf_reais": len(arquivos_pdf)
    }

print("\n--- RESUMO COMPARATIVO POR EXERCÍCIO ---")
for ano, d in resumo.items():
    print(f"\nAno {ano}:")
    print(f"  • Certames no JSON: {d['compras_json']} | Pastas em disco: {d['pastas_disco']}")
    print(f"  • Arquivos previstos na API: {d['arqs_previstos_json']} | Arquivos gravados em disco: {d['arqs_totais_disco']}")
    print(f"  • Arquivos válidos: {d['arqs_totais_disco'] - d['arqs_zerados']} (PDFs diretos: {d['arqs_pdf_reais']}, Pacotes ZIP: {d['arqs_zip_pacotes']})")
    print(f"  • Arquivos zerados (0 bytes / falhas): {d['arqs_zerados']}")

# Checagem no Corpus RAG
print("\n" + "="*75)
print("AUDITORIA NO ÍNDICE RAG (corpus_ia/indice.jsonl)")
print("="*75)

with open("corpus_ia/indice.jsonl", "r", encoding="utf-8") as f:
    docs_rag = [json.loads(line) for line in f]

docs_mppi_ano = {}
for d in docs_rag:
    if d.get("orgao") == "MPPI":
        ano = d.get("ano", "N/A")
        docs_mppi_ano[ano] = docs_mppi_ano.get(ano, 0) + 1

print(f"Total de documentos indexados no RAG do MPPI: {sum(docs_mppi_ano.values())}")
for ano, count in sorted(docs_mppi_ano.items()):
    print(f"  • Ano {ano}: {count} documentos indexados")

