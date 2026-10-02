import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("contratacoes_mppi_pncp_2024.json", "r", encoding="utf-8") as f:
    mppi_contratos = json.load(f)

print(f"=== Mapeamento de Processos MPPI (Total {len(mppi_contratos)}) ===")
for c in mppi_contratos:
    mod = c.get("modalidade")
    num = c.get("numero_compra")
    seq = c.get("sequencial_pncp")
    obj = c.get("objeto", "")
    val = c.get("valor_estimado", 0)
    folder = f"downloads/mppi_pncp_2024/{num.replace('/', '_')}_{seq}"
    arqs_baixados = len(os.listdir(folder)) if os.path.exists(folder) else 0
    print(f"[{mod}] Num: {num} (Seq {seq}) | R$ {val:,.2f} | Arqs baixados: {arqs_baixados}")
    print(f"   Objeto: {obj[:110]}...")
