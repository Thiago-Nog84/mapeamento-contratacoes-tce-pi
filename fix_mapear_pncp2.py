import re

with open('mapear_pncp_tce.py', 'r', encoding='utf-8') as f:
    code = f.read()

import textwrap

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

# We'll use regex to replace everything between "resultado = client.consultar_contratacoes(" and "seq = it.get('sequencialCompra')"
pattern = re.compile(r"resultado = client\.consultar_contratacoes\(.*?for it in items:", re.DOTALL)
match = pattern.search(code)
if match:
    # keep the indentation
    code = code[:match.start()] + new_block.strip() + "\n" + code[match.end():]
    
    # also add pagina += 1 at the end of the while loop
    # actually, where does the while loop end? We need to indent everything inside the for loop!
    # Ah, the indentation will be messed up.
