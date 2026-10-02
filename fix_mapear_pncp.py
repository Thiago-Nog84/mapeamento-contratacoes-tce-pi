import os

with open('mapear_pncp_tce.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Substituir bloco de consulta para ter loop de paginação
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

code = code.replace(old_block.strip(), new_block.strip())

with open('mapear_pncp_tce.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("mapear_pncp_tce.py atualizado com paginacao")
