import re
import json

with open("E:/Thiago/Dev/Mapeamento TCE/tce_bundle.js", "r", encoding="utf-8") as f:
    text = f.read()

# Try finding JSON block containing "name" and "version" and "api"
start_idx = text.find('api:[{')
if start_idx != -1:
    print("Encontrou api:[{ em", start_idx)

# Find all occurrences of endpoints
pattern = re.compile(r'\"type\":\"([^\"]+)\",\"url\":\"([^\"]+)\",\"title\":\"([^\"]+)\"')
matches = pattern.findall(text)
print(f"Total matches por regex: {len(matches)}")

# Also look for any words related to processo, decisao, acordao, julgamento, licitacao
keywords = ['processo', 'decisao', 'julgad', 'acordao', 'jurisprudencia', 'licitac', 'contrat', 'despesa', 'folha', 'empenho']
for kw in keywords:
    kw_matches = [m for m in matches if kw in m[1].lower() or kw in m[2].lower()]
    print(f"Palavra '{kw}': {len(kw_matches)} endpoints")
    for m in kw_matches[:5]:
        print(f"   [{m[0].upper()}] {m[1]} -> {m[2]}")

print("\n--- TODOS OS ENDPOINTS MAPEADOS ---")
for m in matches:
    print(f"[{m[0].upper()}] {m[1]} - {m[2]}")
