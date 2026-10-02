import os

with open('mapear_pncp_mppi.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"11536694000100"', '"10551559000163"')
code = code.replace('TCE-PI', 'MPPI')

with open('mapear_pncp_mppi.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("CNPJ do Fundo MPPI atualizado!")
