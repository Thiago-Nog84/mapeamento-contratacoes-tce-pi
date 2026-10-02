import os
import json
import sqlite3
import pandas as pd

print("=== 1. Buscando em licitações.xlsx ===")
try:
    df = pd.read_excel("licitações.xlsx")
    carona_rows = df[df.astype(str).apply(lambda row: row.str.contains("ades|carona|registro de pre|arp", case=False).any(), axis=1)]
    print(f"Total registros em licitações.xlsx com menção a adesão/carona/registro de preços: {len(carona_rows)}")
    for idx, r in carona_rows.head(5).iterrows():
        print(f"  Colunas relevantes: {r.to_dict()}")
except Exception as e:
    print(f"Erro ao ler excel: {e}")

print("\n=== 2. Buscando em corpus_ia (.md) por 'carona' ou 'órgão não participante' ou 'adesão a ata' ===")
matches = []
corpus_dir = "corpus_ia"
for root, dirs, files in os.walk(corpus_dir):
    for f in files:
        if f.endswith('.md'):
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    if any(term in content.lower() for term in ['adesão à ata', 'adesao a ata', 'órgão não participante', 'orgao nao participante', 'carona']):
                        matches.append((fpath, len(content)))
            except Exception:
                pass

print(f"Total de documentos no Corpus IA mencionando Adesão a Ata / Não Participante / Carona: {len(matches)}")
for m, size in matches[:10]:
    print(f"  {m} ({size} chars)")
