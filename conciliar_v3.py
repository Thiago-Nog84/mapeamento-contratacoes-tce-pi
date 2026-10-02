import pandas as pd
import json
from pathlib import Path
import re

df = pd.read_excel('licitações.xlsx')

col_controle = df.columns[2]
col_procedimento = df.columns[3]
col_valor = df.columns[11]

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

base_extraida = {}

for ano in [2023, 2024, 2025, 2026]:
    fpath = f'contratacoes_tce_pncp_{ano}.json'
    if Path(fpath).exists():
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
                    
                    if norm not in base_extraida: base_extraida[norm] = []
                    base_extraida[norm].append({'fonte': f'PNCP_{ano}', 'valor': item.get('valor_estimado', 0)})

if Path('licitacoes_export.json').exists():
    with open('licitacoes_export.json', 'r', encoding='utf-8') as f:
        for item in json.load(f):
            ctrl = str(item.get('controle_tce')).strip()
            num_proc = normalize_num(item.get('numero_procedimento'))
            val = item.get('valor_previsto', 0)
            
            if ctrl and ctrl != 'None':
                if ctrl not in base_extraida: base_extraida[ctrl] = []
                base_extraida[ctrl].append({'fonte': 'MURALIC', 'valor': val})
            if num_proc:
                if num_proc not in base_extraida: base_extraida[num_proc] = []
                base_extraida[num_proc].append({'fonte': 'MURALIC', 'valor': val})

encontrados = 0
nao_encontrados = []
divergencia_valor = []

for _, row in df.iterrows():
    n_norm = row['num_normalizado']
    c_norm = row['controle_tce_norm']
    
    match = []
    if n_norm and n_norm in base_extraida:
        match = base_extraida[n_norm]
    elif c_norm and c_norm in base_extraida:
        match = base_extraida[c_norm]
        
    if match:
        encontrados += 1
        valor_planilha = row[col_valor]
        try:
            if isinstance(valor_planilha, str):
                v_plan = float(valor_planilha.replace('R$','').replace('.','').replace(',','.').strip())
            else:
                v_plan = float(valor_planilha)
        except:
            v_plan = 0
            
        v_base = max([r['valor'] for r in match])
        if v_plan and v_base and abs(v_plan - v_base) > 100:
            divergencia_valor.append({
                'num': n_norm or c_norm,
                'planilha': v_plan,
                'base': v_base,
                'fontes': list(set(r['fonte'] for r in match))
            })
    else:
        nao_encontrados.append(n_norm or c_norm)

with open('conciliacao_relatorio.md', 'w', encoding='utf-8') as f:
    f.write("# Relatório de Conciliação (Planilha Oficial vs Corpus Extraído)\n\n")
    f.write(f"- **Total de licitações na planilha oficial:** {len(df)}\n")
    f.write(f"- **Encontrados no corpus (PNCP + Muralic):** {encontrados} ({(encontrados/len(df))*100:.1f}%)\n")
    f.write(f"- **Não encontrados no corpus:** {len(nao_encontrados)}\n")
    f.write(f"- **Divergências de Valor (>R):** {len(divergencia_valor)}\n\n")
    
    if nao_encontrados:
        f.write("## Amostra de Não Encontrados\n")
        for n in nao_encontrados[:15]:
            f.write(f"- {n}\n")
            
    if divergencia_valor:
        f.write("\n## Divergências de Valor\n")
        f.write("| Processo | Valor Planilha | Valor Extraído | Fonte |\n")
        f.write("|---|---|---|---|\n")
        for d in divergencia_valor[:15]:
            f.write(f"| {d['num']} | R$ {d['planilha']:,.2f} | R$ {d['base']:,.2f} | {', '.join(d['fontes'])} |\n")

print(f"Relatorio gerado. Encontrados: {encontrados}/{len(df)}")
