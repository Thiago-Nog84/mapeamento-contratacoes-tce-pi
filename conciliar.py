import pandas as pd
import json
from pathlib import Path

# Carregar planilha
df = pd.read_excel('licitações.xlsx')

# Limpar e normalizar os numeros
def extract_num_ano(x):
    if pd.isna(x): return None
    import re
    m = re.search(r'(\d+)/(\d{4})', str(x))
    if m:
        return f"{m.group(1).zfill(5)}/{m.group(2)}"
    return None

df['num_normalizado'] = df['Nº Procedimento'].apply(extract_num_ano)

# Carregar JSONs
pncp_records = []
for ano in [2023, 2024, 2025, 2026]:
    fpath = f'contratacoes_tce_pncp_{ano}.json'
    if Path(fpath).exists():
        with open(fpath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                num = item.get('numero_compra')
                if num:
                    # No JSON do PNCP o ano esta separado na maioria das vezes,
                    # mas as vezes tem barra. Vamos testar.
                    num_str = str(num)
                    if '/' in num_str:
                        p = num_str.split('/')
                        norm = f"{p[0].zfill(5)}/{p[1]}"
                    else:
                        norm = f"{num_str.zfill(5)}/{ano}"
                        
                    pncp_records.append({
                        'num': norm,
                        'ano': ano,
                        'fonte': f'PNCP_{ano}',
                        'valor': item.get('valor_estimado', 0)
                    })

base_extraida = {}
for r in pncp_records:
    norm = r['num']
    if norm not in base_extraida:
        base_extraida[norm] = []
    base_extraida[norm].append(r)

# Conciliacao
encontrados = 0
nao_encontrados = []
divergencia_valor = []
planilha_validos = 0

for _, row in df.iterrows():
    norm = row['num_normalizado']
    if not norm:
        continue
    planilha_validos += 1
    
    if norm in base_extraida:
        encontrados += 1
        # Verificar valor
        valor_planilha = row['Valor']
        if isinstance(valor_planilha, str):
            try:
                v_plan = float(valor_planilha.replace('R$','').replace('.','').replace(',','.').strip())
            except:
                v_plan = 0
        else:
            v_plan = valor_planilha
            
        v_base = max([r['valor'] for r in base_extraida[norm]])
        
        # se diferenca maior que 100 reais
        if pd.notna(v_plan) and v_base and abs(v_plan - v_base) > 100:
            divergencia_valor.append({
                'num': norm,
                'planilha': v_plan,
                'base': v_base
            })
    else:
        nao_encontrados.append(norm)

with open('conciliacao_relatorio.md', 'w', encoding='utf-8') as f:
    f.write("# Relatório de Conciliação\n\n")
    f.write(f"- **Total na planilha com número válido:** {planilha_validos}\n")
    f.write(f"- **Encontrados no corpus PNCP extraído:** {encontrados}\n")
    f.write(f"- **Não encontrados:** {len(nao_encontrados)}\n")
    f.write(f"- **Divergências de valor (>R):** {len(divergencia_valor)}\n\n")
    
    if nao_encontrados:
        f.write("## Amostra de Não Encontrados\n")
        for n in nao_encontrados[:20]:
            f.write(f"- {n}\n")
            
    if divergencia_valor:
        f.write("\n## Amostra de Divergências de Valor\n")
        f.write("| Número | Valor Planilha | Valor Extraído |\n")
        f.write("|---|---|---|\n")
        for d in divergencia_valor[:20]:
            f.write(f"| {d['num']} | R$ {d['planilha']:.2f} | R$ {d['base']:.2f} |\n")

print("Relatorio gerado em conciliacao_relatorio.md")
