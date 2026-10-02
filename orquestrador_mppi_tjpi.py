import time
import subprocess
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=== ORQUESTRADOR: TRANSIÇÃO AUTOMÁTICA MPPI -> TJ-PI ===")

# Verifica se o script extrair_mppi_2025_2026.py ainda esta rodando
while True:
    try:
        out = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /FO CSV', shell=True).decode('utf-8', errors='ignore')
        # Se extrair_mppi_2025_2026.py acabou (verificamos se contratacoes_mppi_pncp_2026.json ja existe e tem conteudo)
        f26 = "contratacoes_mppi_pncp_2026.json"
        if os.path.exists(f26) and os.path.getsize(f26) > 500:
            print("\n[OK] Extração bruta do MPPI (2024, 2025 e 2026) FINALIZADA com sucesso!")
            break
    except Exception as e:
        pass
    print("Aguardando finalização do MPPI 2026...")
    time.sleep(10)

print("\n--- ETAPA INTERMEDIÁRIA: Descompactando e indexando editais/TRs ZIP do MPPI ---")
subprocess.run([sys.executable, "descompactar_mppi.py"], check=False)

print("\n" + "="*75)
print(">>> INICIANDO IMEDIATAMENTE A EXTRAÇÃO DO TJ-PI E CGJ <<<")
print("="*75)
subprocess.run([sys.executable, "-u", "extrair_tjpi.py"], check=False)

print("\n[PIPELINE COMPLETO CONCLUÍDO!]")
