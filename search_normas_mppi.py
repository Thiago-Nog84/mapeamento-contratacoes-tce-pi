import re

def search_in_file(filepath, keywords):
    print(f"=== {filepath} ===")
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if any(k.lower() in line.lower() for k in keywords):
                snippet = "".join(lines[max(0, idx-2):min(len(lines), idx+8)])
                print(f"--- Linha {idx+1} ---")
                print(snippet)
                print("="*40)
    except Exception as e:
        print(f"Erro: {e}")

path_mppi_1382 = r"C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago\01_Normativos_Vigentes\03_MPPI\Atos\Ato PGJ 1382.2024 - Regulamenta a Implementação da 14133 no MPPI.md"
search_in_file(path_mppi_1382, ["dispensa", "inexigibilidade", "adesão", "carona", "não participante", "registro de preços"])
