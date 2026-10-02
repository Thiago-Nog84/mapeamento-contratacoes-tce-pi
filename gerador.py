import os

with open('mapear_pncp_tce.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Trocar o CNPJ do TCE pelo do MPPI (05805924000189)
code = code.replace("PNCPClient.CNPJ_TCE", "'05805924000189'")
code = code.replace("tce_pncp", "mppi_pncp")

with open('mapear_pncp_mppi.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("mapear_pncp_mppi.py gerado!")
