# -*- coding: utf-8 -*-
with open(r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Remove the duplicate stat-cards and extra </div>
snippet_to_remove = """                <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
                  <div className="stat-label">Total Final Homologado</div>
                  <div className="stat-val">R$ 272,4 Mi</div>
                  <div className="stat-sub">Valor adjudicado aos fornecedores</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #10b981' }}>
                  <div className="stat-label">Economia aos Cofres Públicos</div>
                  <div className="stat-val" style={{ color: '#34d399' }}>R$ 68,8 Mi</div>
                  <div className="stat-sub">Diferença economizada no certame</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #c5a059' }}>
                  <div className="stat-label">Deságio Médio Global</div>
                  <div className="stat-val" style={{ color: '#a60225' }}>20,18%</div>
                  <div className="stat-sub">Faixa saudável de competitividade</div>
                </div>
              </div>"""

if snippet_to_remove in text:
    text = text.replace(snippet_to_remove, "")
    print("Snippet removido com sucesso!")
else:
    # Try with raw lines replacement
    lines = text.splitlines(keepends=True)
    # Check lines 426 to 441
    new_lines = []
    skip = False
    for i, l in enumerate(lines):
        if 'borderLeft: \'4px solid #3b82f6\'' in l and i > 410 and i < 445:
            skip = True
        if skip and '{/* SIMULADOR INTERATIVO' in l:
            skip = False
        if not skip:
            new_lines.append(l)
    text = "".join(new_lines)
    print("Substituição por linhas executada!")

with open(r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx", "w", encoding="utf-8") as f:
    f.write(text)
