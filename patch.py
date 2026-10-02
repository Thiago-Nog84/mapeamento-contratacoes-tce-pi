import re
import os

# Patch pncp_client.py
with open('src/pncp_client.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_get = """
    def _get(self, url: str) -> Any:
        import time
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        for t in range(5):
            try:
                with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code == 403:
                    print(f"      [!] API PNCP bloqueou ({e.code}). Aguardando 10s...")
                    time.sleep(10)
                else:
                    raise e
            except Exception as e:
                print(f"      [!] Erro PNCP: {e}. Aguardando 5s...")
                time.sleep(5)
        return {}
"""

code = re.sub(
    r'    def _get.*?return json\.loads\(resp\.read\(\)\.decode\(\'utf-8\'\)\)',
    new_get.strip('\n'),
    code,
    flags=re.DOTALL
)

with open('src/pncp_client.py', 'w', encoding='utf-8') as f:
    f.write(code)

# Patch mapear_pncp_tce.py
with open('mapear_pncp_tce.py', 'r', encoding='utf-8') as f:
    code_map = f.read()

old_loop = """
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

new_loop = """
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
# Replace matching without exact character match for "contratações"
code_map = re.sub(
    r'        resultado = client\.consultar_contratacoes\(.*?for it in items:',
    new_loop.strip('\n'),
    code_map,
    flags=re.DOTALL
)

# And inject pagina += 1 at the end of the while loop (which ends before the next modality loop or out_file)
code_map = re.sub(
    r'            total_coletado\.append\(registro\)',
    '            total_coletado.append(registro)\n            \n        pagina += 1',
    code_map
)

with open('mapear_pncp_tce.py', 'w', encoding='utf-8') as f:
    f.write(code_map)

print("Patch aplicado com sucesso.")
