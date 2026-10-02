import shutil

scratch_app = r'c:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\Mapeamento TCE\scratch\portal_app.jsx'
target_app = r'E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx'

with open(scratch_app, 'r', encoding='utf-8') as f:
    code = f.read()

# Substituir ocorrências pelo PROJETO ANNONA
code = code.replace("BASE RAG ATIVA: 10.504 DOCUMENTOS INDEXADOS", "PROJETO ANNONA ATIVO: 10.504 DOCUMENTOS INDEXADOS")
code = code.replace("OBSERVATÓRIO CLC", "PROJETO ANNONA")
code = code.replace("MPPI • Governança & Compras", "Governança & Compras Públicas • MPPI")
code = code.replace("Ecossistema Regional de Inteligência em Compras Públicas do Nordeste", "PROJETO ANNONA — Inteligência e Governança em Compras do Nordeste")
code = code.replace(
    "Iniciativa Pioneira Nacional",
    "Inspirado na Cura Annonae • Magistratura de Compras"
)
code = code.replace(
    "Simulador Interativo de Deságio e Risco de Inexequibilidade (CLC/MPPI)",
    "Simulador Interativo de Deságio e Risco ANNONA (CLC/MPPI)"
)
code = code.replace(
    "Coordenação de Licitações e Contratos (CLC/MPPI) • Inovação, Dados Abertos e Gestão Preventiva",
    "Coordenação de Licitações e Contratos (CLC/MPPI) • PROJETO ANNONA: Da Tradição Romana à Inteligência de Dados"
)

with open(scratch_app, 'w', encoding='utf-8') as f:
    f.write(code)

shutil.copyfile(scratch_app, target_app)
print("portal_app.jsx atualizado e copiado para App.jsx com a marca PROJETO ANNONA!")
