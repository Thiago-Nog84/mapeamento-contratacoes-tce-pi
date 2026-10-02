import os

# 1. Checkout original mapear_pncp_tce.py
os.system("git checkout mapear_pncp_tce.py")

# 2. Read and rewrite correctly
with open('mapear_pncp_tce.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_block = """
        resultado = client.consultar_contratacoes(
            cnpj=PNCPClient.CNPJ_TCE,
            ano=ano,
            codigo_modalidade=mod_cod,
            pagina=1,
            tamanho_pagina=50
        )
        total_reg = resultado.get('totalRegistros', 0)
        items = resultado.get('data', [])
        print(f"    -> {total_reg} contrataes encontradas.")

        for it in items:
"""

new_block = """
        import time
        pagina = 1
        total_reg = 1
        itens_coletados = 0
        
        while itens_coletados < total_reg:
            resultado = client.consultar_contratacoes(
                cnpj=PNCPClient.CNPJ_TCE,
                ano=ano,
                codigo_modalidade=mod_cod,
                pagina=pagina,
                tamanho_pagina=50
            )
            if pagina == 1:
                total_reg = resultado.get('totalRegistros', 0)
                print(f"    -> {total_reg} contratações encontradas.")
            
            items = resultado.get('data', [])
            if not items:
                break
                
            for it in items:
                itens_coletados += 1
"""

# Regex replacement
import re
code = re.sub(
    r'        resultado = client\.consultar_contratacoes\(.*?for it in items:',
    new_block.strip('\n'),
    code,
    flags=re.DOTALL
)

# Fix indentation of the inner loop body
lines = code.split('\n')
new_lines = []
in_for_loop = False
for i, line in enumerate(lines):
    if 'itens_coletados += 1' in line:
        new_lines.append(line)
        in_for_loop = True
        continue
        
    if in_for_loop:
        if line.startswith('            seq ='):
            # The body starts here, we need to indent everything by 4 spaces
            pass
        
        if line.startswith('            total_coletado.append(registro)'):
            # This is the last line of the inner loop body
            new_lines.append('    ' + line)
            new_lines.append('            ')
            new_lines.append('        pagina += 1')
            in_for_loop = False
            continue
            
        if line.strip() != '' and not line.startswith('    for '):
            new_lines.append('    ' + line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('mapear_pncp_tce.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("mapear_pncp_tce.py atualizado corretamente!")
