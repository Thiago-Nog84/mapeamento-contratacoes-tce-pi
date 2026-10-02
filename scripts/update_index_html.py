path = r'E:\Thiago\Dev\Mapeamento TCE\dashboard\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('lang="en"', 'lang="pt-BR"')
html = html.replace('<title>dashboard</title>', '<title>PROJETO ANNONA • Observatório de Governança & Compras Públicas | MPPI</title>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html title!')
