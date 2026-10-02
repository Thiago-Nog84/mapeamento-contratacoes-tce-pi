import os

with open('analisar_pdfs.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the NoneType comparison in sorted(anos.keys())
# replace sorted(anos.keys()) with sorted([str(k) for k in anos.keys() if k is not None])
code = code.replace("sorted(anos.keys())", "sorted([str(k) for k in anos.keys() if k is not None])")

with open('analisar_pdfs.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('gen_dataset.py', 'r', encoding='utf-8') as f:
    code2 = f.read()

code2 = code2.replace("sorted(anos.items())", "sorted([(str(k), v) for k, v in anos.items() if k is not None])")

with open('gen_dataset.py', 'w', encoding='utf-8') as f:
    f.write(code2)

print("Corrigido problemas com ano == None")
