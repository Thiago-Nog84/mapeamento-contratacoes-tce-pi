import os

with open('mapear_pncp_mppi.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Trocar os CNPJs do MPPI pelo CNPJ do FPDC
code = code.replace("05805924000189", "24291901000148")
code = code.replace("10551559000163", "24291901000148") # Usamos o mesmo para o segundo loop para nao quebrar, ou deixamos.
code = code.replace("MPPI", "FPDC")
code = code.replace("mppi", "fpdc")

with open('mapear_pncp_fpdc.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("mapear_pncp_fpdc.py gerado!")
