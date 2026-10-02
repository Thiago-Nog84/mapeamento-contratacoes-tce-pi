import json
import os
import time
from src.muralic_scraper import MuralicScraper

with open('missing_muralic.json', 'r') as f:
    missing = json.load(f)

scraper = MuralicScraper()
count = 0

for item in missing:
    id_web = item['id_web']
    num_proc = str(item['num_proc']).replace('/', '_').replace(':', '')
    ano = item['ano']
    
    dir_destino = f"downloads/muralic_tce/{ano}/{num_proc}_{id_web}"
    
    # Se ja existe a pasta com arquivos, pula
    if os.path.exists(dir_destino) and len(os.listdir(dir_destino)) > 0:
        continue
        
    print(f"[{count+1}/{len(missing)}] Processando ID {id_web} ({num_proc})...")
    try:
        proc = scraper.obter_detalhes_e_artefatos(id_web)
        if not proc or not proc.artefatos:
            print("  -> Nenhum artefato encontrado.")
            continue
            
        os.makedirs(dir_destino, exist_ok=True)
        for art in proc.artefatos:
            # Baixar so os relevantes (Edital, TR, ETP)
            tipo_low = art.tipo.lower() if art.tipo else ""
            if "edital" in tipo_low or "termo de refer" in tipo_low or "estudo t" in tipo_low or "projeto" in tipo_low:
                print(f"  -> Baixando {art.tipo}: {art.nome_arquivo}")
                scraper.baixar_artefato(id_web, art, dir_destino)
                
        count += 1
        time.sleep(1)
    except Exception as e:
        print(f"  [!] Erro no ID {id_web}: {e}")

print(f"Concluido! {count} novos procedimentos processados no Muralic.")
