"""
download_anos.py
Executa o download de multiplos anos em sequencia.
Uso: python download_anos.py 2023 2024
"""
import subprocess, sys, time

anos = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [2023, 2024]

for ano in anos:
    print(f"\n{'='*60}")
    print(f"  Iniciando: ano {ano}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "mapear_pncp_tce.py", "--ano", str(ano), "--download"],
        capture_output=False
    )
    elapsed = round(time.time() - t0, 1)
    print(f"\n  Ano {ano} concluido em {elapsed}s (codigo: {result.returncode})")

print("\nTodos os anos processados!")
