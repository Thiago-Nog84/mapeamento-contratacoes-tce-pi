import os, sys, fitz, docx, zipfile, xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

pasta = r"E:\Thiago\Dev\Mapeamento TCE\Manual de Projetos"

def ler_pdf(caminho, max_paginas=20):
    try:
        doc = fitz.open(caminho)
        texto = []
        for i in range(min(len(doc), max_paginas)):
            texto.append(f"--- PÁGINA {i+1} ---")
            texto.append(doc[i].get_text())
        return "\n".join(texto)
    except Exception as e:
        return f"Erro ao ler PDF: {e}"

def ler_odt(caminho):
    try:
        with zipfile.ZipFile(caminho, 'r') as z:
            content = z.read('content.xml')
            root = ET.fromstring(content)
            # Extrair texto de tags
            textos = []
            for elem in root.iter():
                if elem.text:
                    textos.append(elem.text)
            return " ".join(textos)
    except Exception as e:
        return f"Erro ao ler ODT: {e}"

print("="*80)
print("1. REGULAMENTO DO PRÊMIO CNMP")
print("="*80)
cnmp_pdf = os.path.join(pasta, "Regulamento_Premio_CNMP_2021.pdf")
if os.path.exists(cnmp_pdf):
    txt = ler_pdf(cnmp_pdf, 10)
    print(txt[:2500])

print("\n" + "="*80)
print("2. ATO PGJ PI 1.0255/2020 (NORMATIVO DE GESTÃO DE PROJETOS MPPI)")
print("="*80)
ato_pdf = os.path.join(pasta, "ATO_PGJ_PI_NA___1.0255_2020___consolidado.pdf")
if os.path.exists(ato_pdf):
    txt_ato = ler_pdf(ato_pdf, 10)
    print(txt_ato[:2500])

print("\n" + "="*80)
print("3. MANUAL DE PROJETOS DO MPPI")
print("="*80)
manual_pdf = os.path.join(pasta, "Manual_de_Projetos.pdf")
if os.path.exists(manual_pdf):
    doc_m = fitz.open(manual_pdf)
    print(f"Total de páginas no Manual de Projetos: {len(doc_m)}")
    # Ler sumário e primeiras páginas
    txt_m = ler_pdf(manual_pdf, 12)
    print(txt_m[:3000])

print("\n" + "="*80)
print("4. MODELO DE TAP INICIAL (ODT)")
print("="*80)
tap_odt = os.path.join(pasta, "modelo-de-Termo-de-Abertura-de-Projeto-TAP-inicial.odt")
if os.path.exists(tap_odt):
    txt_tap = ler_odt(tap_odt)
    print(txt_tap[:2000])

