import pandas as pd
import json
from pathlib import Path

# Carregar planilha
df = pd.read_excel('licitações.xlsx')

def extract_num_ano(x):
    if pd.isna(x): return None
    import re
    m = re.search(r'(\d+)/(\d{4})', str(x))
    if m:
        return f"{m.group(1).zfill(5)}/{m.group(2)}"
    return None

df['num_normalizado'] = df['Nº Procedimento'].apply(extract_num_ano)

pncp_records = []

# Todos os JSONs na pasta raiz
for fpath in Path('.').glob('*.json'):
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data] # dicts
            for item in data:
                # pode ser numero_compra ou numero_licitacao ou id_licitacao etc
                num = item.get('numero_compra') or item.get('numero_licitacao') or item.get('numero')
                ano = item.get('ano') or item.get('ano_licitacao')
                if num and ano:
                    num_str = str(num)
                    if '/' in num_str:
                        p = num_str.split('/')
                        norm = f"{p[0].zfill(5)}/{p[1]}"
                    else:
                        norm = f"{num_str.zfill(5)}/{ano}"
                    pncp_records.append({
                        'num': norm,
                        'fonte': fpath.name,
                        'valor': item.get('valor_estimado') or item.get('valor_total') or 0
                    })
        except:
            pass

base_extraida = {}
for r in pncp_records:
    norm = r['num']
    if norm not in base_extraida:
        base_extraida[norm] = []
    base_extraida[norm].append(r)

encontrados = 0
nao_encontrados = []

for _, row in df.iterrows():
    norm = row['num_normalizado']
    if not norm: continue
    
    if norm in base_extraida:
        encontrados += 1
    else:
        nao_encontrados.append(norm)

with open('conciliacao_relatorio.md', 'w', encoding='utf-8') as f:
    f.write("# Relatório de Conciliação (Todas as Fontes JSON)\n\n")
    f.write(f"- **Total na planilha:** 404\n")
    f.write(f"- **Encontrados nas extrações (PNCP + Muralic):** {encontrados}\n")
    f.write(f"- **Não encontrados:** {len(nao_encontrados)}\n")

print("Relatorio atualizado")
