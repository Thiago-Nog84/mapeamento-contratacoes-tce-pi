import pandas as pd
import json
import re

df = pd.read_excel('licitações.xlsx')

col_controle = df.columns[2]
col_procedimento = df.columns[3]
col_url = df.columns[19] # Caminho detalhamento licitao

def normalize_num(x):
    if pd.isna(x): return None
    m = re.search(r'(\d+)/(\d{4}|\d{2})', str(x))
    if m:
        num = m.group(1).zfill(5)
        ano = m.group(2)
        if len(ano) == 2: ano = "20" + ano
        return f"{num}/{ano}"
    return None

df['num_normalizado'] = df[col_procedimento].apply(normalize_num)
df['controle_tce_norm'] = df[col_controle].apply(lambda x: str(x).strip() if pd.notna(x) else None)

base_extraida = set()

# PNCP
for ano in [2023, 2024, 2025, 2026]:
    fpath = f'contratacoes_tce_pncp_{ano}.json'
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                num = item.get('numero_compra')
                if num:
                    nstr = str(num)
                    if '/' in nstr:
                        p = nstr.split('/')
                        norm = f"{p[0].zfill(5)}/{p[1]}"
                    else:
                        norm = f"{nstr.zfill(5)}/{ano}"
                    base_extraida.add(norm)
    except: pass

# Muralic
try:
    with open('licitacoes_export.json', 'r', encoding='utf-8') as f:
        for item in json.load(f):
            ctrl = str(item.get('controle_tce')).strip()
            num_proc = normalize_num(item.get('numero_procedimento'))
            if ctrl and ctrl != 'None': base_extraida.add(ctrl)
            if num_proc: base_extraida.add(num_proc)
except: pass

missing = []

for _, row in df.iterrows():
    n_norm = row['num_normalizado']
    c_norm = row['controle_tce_norm']
    
    if (n_norm and n_norm in base_extraida) or (c_norm and c_norm in base_extraida):
        continue
    
    url = str(row[col_url])
    m = re.search(r'id=(\d+)', url)
    if m:
        id_web = int(m.group(1))
        missing.append({
            'id_web': id_web,
            'num_proc': n_norm if n_norm else (c_norm if c_norm else "desc"),
            'ano': n_norm.split('/')[1] if isinstance(n_norm, str) else "2026"
        })

with open('missing_muralic.json', 'w') as f:
    json.dump(missing, f, indent=2)

print(f"Salvos {len(missing)} processos ausentes em missing_muralic.json")
