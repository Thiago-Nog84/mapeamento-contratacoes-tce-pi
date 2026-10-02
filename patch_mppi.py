with open('mapear_pncp_mppi.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("PNCPClient.CNPJ_FMTC", "'10551559000163'")

with open('mapear_pncp_mppi.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("mapear_pncp_mppi.py corrigido!")
