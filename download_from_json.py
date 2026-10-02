import json
import os
import sys
from src.pncp_client import PNCPClient

ano = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
with open(f'contratacoes_tce_pncp_{ano}.json', 'r', encoding='utf-8') as f:
    contratacoes = json.load(f)

client = PNCPClient()
count = 0
for c in contratacoes:
    seq_compra = c['sequencial_pncp']
    num_compra = c['numero_compra']
    
    arquivos = c.get('arquivos', [])
    for a in arquivos:
        seq_doc = a['sequencial_documento']
        tipo_doc = a.get('tipo', 'Documento')
        titulo = a.get('titulo', f"doc_{seq_doc}")
        
        caminho_local = f"downloads/tce_pncp_{ano}/{num_compra.replace('/','_')}_{seq_compra}/{tipo_doc}_{titulo}.pdf"
        
        # Limpar nome do arquivo para Windows
        for char in [':', '?', '"', '<', '>', '|', '*']:
            caminho_local = caminho_local.replace(char, '')
        
        if os.path.exists(caminho_local):
            continue
            
        print(f"Baixando: {caminho_local}")
        try:
            client.baixar_arquivo(PNCPClient.CNPJ_TCE, ano, seq_compra, seq_doc, caminho_local)
            count += 1
        except Exception as e:
            print(f"Erro definitivo ao baixar {titulo}: {e}")

print(f"Download {ano} concluido! {count} novos arquivos baixados.")
