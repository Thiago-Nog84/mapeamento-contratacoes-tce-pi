import json
import os
import sys
import time
from src.pncp_client import PNCPClient

client = PNCPClient()
count = 0

for orgao, cnpj in [('mppi', '05805924000189'), ('fpdc', '24291901000148')]:
    fpath = f'contratacoes_{orgao}_pncp_2024.json'
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, 'r', encoding='utf-8') as f:
        contratacoes = json.load(f)

    for c in contratacoes:
        seq_compra = c['sequencial_pncp']
        num_compra = c['numero_compra']
        ano_compra = c['ano']
        
        # Como o MPPI tem os fundos todos atrelados nos proprios JSONs gerados
        # vamos garantir qual o CNPJ usado pela chamada. O orgao pode ter fundos.
        # No nosso JSON nao gravamos o CNPJ emissor... vamos assumir o cnpj principal
        # Se der erro, usamos o CNPJ do fundo: 10551559000163 para o MPPI.
        # (Idealmente deve tentar os dois, ja que ambos estao no JSON)
        
        arquivos = c.get('arquivos', [])
        for a in arquivos:
            seq_doc = a['sequencial_documento']
            tipo_doc = a.get('tipo', 'Documento')
            titulo = a.get('titulo', f"doc_{seq_doc}")
            url_download = a.get('url_download', '')
            
            caminho_local = f"downloads/{orgao}_pncp_2024/{num_compra.replace('/','_')}_{seq_compra}/{tipo_doc}_{titulo}.pdf"
            for char in [':', '?', '"', '<', '>', '|', '*']:
                caminho_local = caminho_local.replace(char, '')
            
            if os.path.exists(caminho_local):
                continue
                
            print(f"Baixando: {caminho_local}")
            os.makedirs(os.path.dirname(caminho_local), exist_ok=True)
            try:
                # O PNCPClient.baixar_arquivo exige o CNPJ. Vamos extrair da url_download!
                # url_download ex: https://pncp.gov.br/api/pncp/v1/orgaos/05805924000189/compras/...
                import re
                m = re.search(r'/orgaos/(\d+)/', url_download)
                cnpj_real = m.group(1) if m else cnpj
                
                client.baixar_arquivo(cnpj_real, ano_compra, seq_compra, seq_doc, caminho_local)
                count += 1
                time.sleep(1)
            except Exception as e:
                print(f"Erro definitivo ao baixar {titulo}: {e}")

print(f"Download concluido! {count} novos arquivos baixados.")
