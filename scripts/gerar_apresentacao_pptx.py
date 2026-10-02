import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Paleta Institucional MPPI / ANNONA
COLOR_BG = RGBColor(11, 15, 25)        # Dark Slate #0B0F19
COLOR_CARD = RGBColor(20, 27, 44)      # Card Slate #141B2C
COLOR_VINHO = RGBColor(155, 17, 30)    # MPPI Vinho #9B111E
COLOR_GOLD = RGBColor(197, 160, 89)    # Dourado #C5A059
COLOR_EMERALD = RGBColor(16, 185, 129) # Verde #10B981
COLOR_BLUE = RGBColor(59, 130, 246)    # Azul #3B82F6
COLOR_WHITE = RGBColor(255, 255, 255)  # Branco
COLOR_MUTED = RGBColor(148, 163, 184)  # Cinza #94A3B8
COLOR_BORDER = RGBColor(51, 65, 85)    # Borda #334155

blank_slide_layout = prs.slide_layouts[6]

def set_slide_background(slide, color=COLOR_BG):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="PROJETO ANNONA • GOVERNANÇA & COMPRAS PÚBLICAS (MPPI)"):
    # Header box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_GOLD
    p_cat.space_after = Pt(4)
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

# ==============================================================================
# SLIDE 1: CAPA
# ==============================================================================
s1 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s1)

# Badge superior
b_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.7), Inches(0.4))
b_p = b_box.text_frame.paragraphs[0]
b_p.text = "MINISTÉRIO PÚBLICO DO ESTADO DO PIAUÍ  •  COORDENAÇÃO DE LICITAÇÕES E CONTRATOS (CLC)"
b_p.font.size = Pt(11)
b_p.font.bold = True
b_p.font.color.rgb = COLOR_GOLD

# Título Principal
t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.2))
tf1 = t_box.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "PROJETO ANNONA"
p1.font.size = Pt(46)
p1.font.bold = True
p1.font.color.rgb = COLOR_WHITE
p1.space_after = Pt(8)

p2 = tf1.add_paragraph()
p2.text = "Observatório de Governança, Preços e Inteligência em Contratações Públicas"
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = COLOR_GOLD

p3 = tf1.add_paragraph()
p3.text = "Da Tradição da Governança à Inteligência Artificial: Dados Abertos, Eficiência do Gasto e Blindagem sob a Lei nº 14.133/2021"
p3.font.size = Pt(13)
p3.font.color.rgb = COLOR_MUTED
p3.space_before = Pt(6)

# 3 Cards de Destaque na Capa
c1 = add_card(s1, Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.3))
c1_tb = s1.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(3.2), Inches(1.9))
c1_tf = c1_tb.text_frame
c1_tf.word_wrap = True
c1_tf.paragraphs[0].text = "10.504 DOCUMENTOS"
c1_tf.paragraphs[0].font.size = Pt(12)
c1_tf.paragraphs[0].font.bold = True
c1_tf.paragraphs[0].font.color.rgb = COLOR_BLUE
c1_p = c1_tf.add_paragraph()
c1_p.text = "100% dos 9 Ministérios Públicos do Nordeste integrados em RAG inédito."
c1_p.font.size = Pt(11)
c1_p.font.color.rgb = COLOR_WHITE

c2 = add_card(s1, Inches(4.8), Inches(4.3), Inches(3.6), Inches(2.3))
c2_tb = s1.shapes.add_textbox(Inches(5.0), Inches(4.5), Inches(3.2), Inches(1.9))
c2_tf = c2_tb.text_frame
c2_tf.word_wrap = True
c2_tf.paragraphs[0].text = "R$ 68,8 MI ECONOMIZADOS"
c2_tf.paragraphs[0].font.size = Pt(12)
c2_tf.paragraphs[0].font.bold = True
c2_tf.paragraphs[0].font.color.rgb = COLOR_EMERALD
c2_p = c2_tf.add_paragraph()
c2_p.text = "Curva empírica real de 20,18% de deságio médio em 219 certames concluídos."
c2_p.font.size = Pt(11)
c2_p.font.color.rgb = COLOR_WHITE

c3 = add_card(s1, Inches(8.8), Inches(4.3), Inches(3.6), Inches(2.3))
c3_tb = s1.shapes.add_textbox(Inches(9.0), Inches(4.5), Inches(3.2), Inches(1.9))
c3_tf = c3_tb.text_frame
c3_tf.word_wrap = True
c3_tf.paragraphs[0].text = "CUSTO ZERO & PRÊMIO CNMP"
c3_tf.paragraphs[0].font.size = Pt(12)
c3_tf.paragraphs[0].font.bold = True
c3_tf.paragraphs[0].font.color.rgb = COLOR_GOLD
c3_p = c3_tf.add_paragraph()
c3_p.text = "Inovação própria da CLC pré-qualificada na Categoria Governança e Gestão."
c3_p.font.size = Pt(11)
c3_p.font.color.rgb = COLOR_WHITE

s1.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 1):\n"
    "Senhor Procurador-Geral de Justiça, Senhores Subprocuradores, Colegas da Administração Superior:\n"
    "Apresento hoje à Administração Superior o PROJETO ANNONA, uma iniciativa concebida e desenvolvida com a força de trabalho interna da Coordenação de Licitações e Contratos (CLC) que coloca o Ministério Público do Estado do Piauí na liderança tecnológica e de governança das compras públicas em todo o Nordeste.\n"
    "O nome 'Annona' resgata a mais nobre raiz histórica da administração pública: a histórica 'Cura Annonae', criada em Roma no ano 7 d.C. para garantir preços justos, fiscalizar contratos e assegurar que o Estado nunca pare por desabastecimento. Nós pegamos essa tradição de zelo pelo dinheiro público e a projetamos no século XXI com Inteligência Artificial, RAG e dados abertos a custo zero."
)

# ==============================================================================
# SLIDE 2: O CENÁRIO REAL DAS CONTRATAÇÕES NO MPPI
# ==============================================================================
s2 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s2)
add_header(s2, "O Cenário Real das Contratações e os Limites dos Modelos Estáticos", "DIAGNÓSTICO E JUSTIFICATIVA")

# 3 Colunas de Diagnóstico
col_w = Inches(3.6)
h_val = Inches(4.8)

# Coluna 1
add_card(s2, Inches(0.8), Inches(1.8), col_w, h_val, border_color=COLOR_VINHO)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "1. DESAFIOS DA LEI 14.133/21"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_VINHO
p = tf.add_paragraph()
p.text = "\n• Exigência rigorosa de Estudos Técnicos Preliminares (ETP) e Matrizes de Risco.\n\n• Setores demandantes frequentemente começavam do zero a cada contratação.\n\n• Insegurança jurídica e receio de responsabilização de servidores (Art. 28 LINDB)."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

# Coluna 2
add_card(s2, Inches(4.8), Inches(1.8), col_w, h_val, border_color=COLOR_GOLD)
tb = s2.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "2. LIMITES DOS MODELOS EM PDF"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD
p = tf.add_paragraph()
p.text = "\n• O MPPI já possuía excelentes diretrizes (MJRs da Assessoria Jurídica), mas em PDFs estáticos de até 160 páginas.\n\n• Consulta manual lenta: servidores com dúvidas sobre como aplicar o rito simplificado.\n\n• Pesquisa de preços muitas vezes refém de cotações locais frágeis."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

# Coluna 3
add_card(s2, Inches(8.8), Inches(1.8), col_w, h_val, border_color=COLOR_BLUE)
tb = s2.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "3. PRESSÃO DO CONTROLE EXTERNO"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_BLUE
p = tf.add_paragraph()
p.text = "\n• Decisões recentes e duras de Tribunais de Contas sobre adesão a atas de registro de preços ('carona').\n\n• Destaque: Acórdão nº 300/2025 do Plenário do TCE-PI, exigindo justificativa contemporânea rigorosa.\n\n• Necessidade de blindagem preventiva de 2ª Linha de Defesa."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s2.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 2):\n"
    "A transição para a Nova Lei de Licitações trouxe grandes desafios para toda a administração pública brasileira. No MPPI, nós já avançamos ao publicar diretrizes normativas e excelentes manifestações referenciais pela Assessoria Jurídica. No entanto, tínhamos um problema prático: essas diretrizes estavam dispersas em documentos estáticos de texto e PDFs de dezenas de páginas. Os servidores dos setores demandantes continuavam 'começando do zero' a cada compra, e a nossa pesquisa de preços ainda operava isolada do resto do país. Precisávamos de um salto de inteligência."
)

# ==============================================================================
# SLIDE 3: O SALTO INOVADOR SOBRE AS MJRS
# ==============================================================================
s3 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s3)
add_header(s3, "O Salto Inovador: Como o ANNONA Potencializa as MJRs Existentes", "INOVAÇÃO E VALORIZAÇÃO INSTITUCIONAL")

# Caixa Antes vs Depois
add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=COLOR_MUTED)
tb = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "O CENÁRIO ANTERIOR (DOCUMENTAL / ESTÁTICO)"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_MUTED
p = tf.add_paragraph()
p.text = "\n• Manifestações Jurídico-Referenciais fundamentais (MJR 92 de dispensa, MJR 86 de adesão a ARP), mas arquivadas em pastas.\n\n• O servidor demandante precisava ler até 160 páginas para confirmar enquadramento.\n\n• Dúvidas recorrentes sobre instrução geravam devoluções processuais.\n\n• Operação isolada: sem comparação paramétrica com outros Ministérios Públicos."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=COLOR_GOLD)
tb = s3.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.0), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "A VERDADEIRA INOVAÇÃO DO PROJETO ANNONA (IA ATIVA)"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD
p = tf.add_paragraph()
p.text = "\n• Inteligência Artificial e RAG que leem o processo e dizem a aderência à MJR em segundos.\n\n• Atualização Preditiva: Adequação dinâmica das adesões a ata às exigências do Acórdão 300/2025 do TCE-PI.\n\n• Curva Empírica Real de Preços: R$ 341M analisados para balizar se a proposta é vantajosa.\n\n• Master Checklist Digital Interativo da CLC com 15 barreiras preventivas de 2ª Linha."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s3.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 3):\n"
    "Quero deixar muito claro perante esta Administração Superior: o PROJETO ANNONA não concorre com a nossa valorosa Assessoria Jurídica nem reinventa a roda. Pelo contrário: ele pega as louváveis manifestações jurídico-referenciais que o MPPI já possui — como a MJR 92 e a MJR 86 — e lhes dá asas tecnológicas. Em vez de exigir que um servidor leia um PDF de 160 páginas para saber se pode ou não dispensar a licitação, o ANNONA faz essa triagem automatizada com Inteligência Artificial, apontando de imediato o que falta e garantindo que o processo chegue blindado à PGJ."
)

# ==============================================================================
# SLIDE 4: PIONEIRISMO REGIONAL (100% DO NORDESTE)
# ==============================================================================
s4 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s4)
add_header(s4, "Pioneirismo Regional: 100% dos Ministérios Públicos do Nordeste Integrados", "ACERVO DE DADOS & BENCHMARKING")

# 4 Caixas de Indicadores do Acervo
kpi_w = Inches(2.7)
kpi_h = Inches(1.5)
add_card(s4, Inches(0.8), Inches(1.8), kpi_w, kpi_h, border_color=COLOR_GOLD)
tb = s4.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(2.5), Inches(1.3))
tb.text_frame.paragraphs[0].text = "10.504 DOCUMENTOS"
tb.text_frame.paragraphs[0].font.size = Pt(15)
tb.text_frame.paragraphs[0].font.bold = True
tb.text_frame.paragraphs[0].font.color.rgb = COLOR_GOLD
p = tb.text_frame.add_paragraph()
p.text = "100% estruturados em Markdown e JSONL."
p.font.size = Pt(9)
p.font.color.rgb = COLOR_WHITE

add_card(s4, Inches(3.8), Inches(1.8), kpi_w, kpi_h, border_color=COLOR_BLUE)
tb = s4.shapes.add_textbox(Inches(3.9), Inches(1.9), Inches(2.5), Inches(1.3))
tb.text_frame.paragraphs[0].text = "12 INSTITUIÇÕES"
tb.text_frame.paragraphs[0].font.size = Pt(15)
tb.text_frame.paragraphs[0].font.bold = True
tb.text_frame.paragraphs[0].font.color.rgb = COLOR_BLUE
p = tb.text_frame.add_paragraph()
p.text = "9 MPs do NE + TJ-PI, TCE-PI e MPDFT."
p.font.size = Pt(9)
p.font.color.rgb = COLOR_WHITE

add_card(s4, Inches(6.8), Inches(1.8), kpi_w, kpi_h, border_color=COLOR_VINHO)
tb = s4.shapes.add_textbox(Inches(6.9), Inches(1.9), Inches(2.5), Inches(1.3))
tb.text_frame.paragraphs[0].text = "662 PARECERES"
tb.text_frame.paragraphs[0].font.size = Pt(15)
tb.text_frame.paragraphs[0].font.bold = True
tb.text_frame.paragraphs[0].font.color.rgb = COLOR_VINHO
p = tb.text_frame.add_paragraph()
p.text = "Mapeamento das causas reais de ressalvas."
p.font.size = Pt(9)
p.font.color.rgb = COLOR_WHITE

add_card(s4, Inches(9.8), Inches(1.8), kpi_w, kpi_h, border_color=COLOR_EMERALD)
tb = s4.shapes.add_textbox(Inches(9.9), Inches(1.9), Inches(2.5), Inches(1.3))
tb.text_frame.paragraphs[0].text = "146 MATRIZES"
tb.text_frame.paragraphs[0].font.size = Pt(15)
tb.text_frame.paragraphs[0].font.bold = True
tb.text_frame.paragraphs[0].font.color.rgb = COLOR_EMERALD
p = tb.text_frame.add_paragraph()
p.text = "Mapas de risco em TIC, obras e serviços."
p.font.size = Pt(9)
p.font.color.rgb = COLOR_WHITE

# Caixa Descritiva dos 9 Estados
add_card(s4, Inches(0.8), Inches(3.6), Inches(11.7), Inches(3.0))
tb = s4.shapes.add_textbox(Inches(1.1), Inches(3.8), Inches(11.1), Inches(2.6))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "A ABRANGÊNCIA HISTÓRICA DO OBSERVATÓRIO DO MPPI:"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD

p = tf.add_paragraph()
p.text = (
    "• MPRN (2.743 docs) — Referência em Termos de Referência e atas integradas;\n"
    "• TJ-PI (2.178 docs) — Provimento nº 13/2025 e contratações do Judiciário estadual;\n"
    "• MPSE (1.144 docs) & TCE-PI (1.120 docs) — Decisões vinculantes e rito sumário de valor;\n"
    "• MPPI (561 docs) — Processos SEI da PGJ e Fundo Especial (FPDC);\n"
    "• MPAL (538 docs), MPBA (472 docs), MPDFT (435 docs), MPMA (431 docs), MPCE (322 docs), MPPB (293 docs), MPPE (267 docs).\n\n"
    "Conexão automatizada às APIs oficiais do Portal Nacional de Contratações Públicas (PNCP) com auditabilidade total."
)
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s4.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 4):\n"
    "O MPPI é hoje o primeiro Ministério Público de todo o Brasil a ter uma base unificada com 100% das contratações de uma região geográfica inteira. Quando o MPPI precisa contratar uma solução de nuvem, uma reforma de promotoria ou um software pericial, nós não precisamos adivinhar o mercado: nós acessamos o que os 8 MPs vizinhos contrataram, quanto pagaram e quais falhas os tribunais de contas apontaram neles. O Piauí deixou de ser consumidor passivo de modelos para ser o polo agregador do Nordeste."
)

# ==============================================================================
# SLIDE 5: IMPACTO FINANCEIRO REAL (R$ 68,8M DE ECONOMIA)
# ==============================================================================
s5 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s5)
add_header(s5, "Impacto Financeiro Comprovado: R$ 68,8 Milhões em Economia e o Simulador", "ESTUDO DE ECONOMICIDADE & DESÁGIO")

# 2 Colunas: Dados + Simulador
add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=COLOR_EMERALD)
tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "A CURVA REAL DE DESÁGIO DOS MINISTÉRIOS PÚBLICOS"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_EMERALD

p = tf.add_paragraph()
p.text = (
    "\n• Total Orçado Analisado: R$ 341.262.169,56\n"
    "• Total Final Homologado: R$ 272.403.233,78\n"
    "• Economia Efetiva aos Cofres: R$ 68.858.935,79\n"
    "• Deságio Médio Global: 20,18% (em 219 certames concluídos)\n\n"
    "DESÁGIO PARAMÉTRICO POR CATEGORIA:\n"
    "  - TIC e Licenças em Nuvem: 25,32%\n"
    "  - Mobiliário e Equipamentos: 28,05%\n"
    "  - Terceirização / Mão de Obra: 13,14%\n"
    "  - Obras e Engenharia Predial: 10,58%"
)
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=COLOR_GOLD)
tb = s5.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.0), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "O SIMULADOR INTERATIVO ANNONA"
tf.paragraphs[0].font.size = Pt(13)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD

p = tf.add_paragraph()
p.text = (
    "\n• Ferramenta online integrada ao portal da CLC/MPPI.\n\n"
    "• O pregoeiro ou pesquisador digita o valor estimado e escolhe a categoria do objeto.\n\n"
    "• O sistema calcula:\n"
    "  1. A economia esperada com base na média regional;\n"
    "  2. O valor provável de homologação;\n"
    "  3. ALERTA DE RISCO DE INEXEQUIBILIDADE: avisa se o desconto passar do limite prudente (ex: >22% em terceirização), exigindo diligência do Art. 59, § 2º."
)
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s5.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 5):\n"
    "Aqui está a prova material da resolutividade do projeto: nós não lidamos com suposições, mas com dados matemáticos. Mapeamos R$ 341 milhões em licitações e descobrimos a curva real de desconto praticada pelo mercado perante os Ministérios Públicos. Essa inteligência permite que os nossos pregoeiros negociem com muito mais firmeza e que os nossos pesquisadores de preço não aceitem cotações infladas. Desenvolvemos inclusive um Simulador no portal que avisa quando um desconto é perigoso e pode gerar abandono de contrato por inexequibilidade."
)

# ==============================================================================
# SLIDE 6: BLINDAGEM CONTRA O TCE-PI E CONTROLE PREVENTIVO
# ==============================================================================
s6 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s6)
add_header(s6, "Blindagem Preventiva contra o TCE-PI e Resposta ao Acórdão nº 300/2025", "2ª LINHA DE DEFESA (ART. 169)")

add_card(s6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), border_color=COLOR_BLUE)
tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "COMO O ANNONA PROTEGE O PROCURADOR-GERAL E OS GESTORES:"
tf.paragraphs[0].font.size = Pt(14)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_BLUE

p = tf.add_paragraph()
p.text = (
    "\n1. RESPOSTA IMEDIATA AO ACÓRDÃO Nº 300/2025 DO TCE-PI (ADESÃO A ATAS / CARONA):\n"
    "   • O Plenário do TCE-PI fixou exigências duras: vigência máxima de 1 ano, pesquisa contemporânea de mercado e justificativa expressa de vantajosidade.\n"
    "   • A CLC antecipou-se e elaborou a Minuta de Instrução Normativa que fecha todas as brechas de nulidade.\n\n"
    "2. MINERAÇÃO DE 662 PARECERES JURÍDICOS:\n"
    "   • Catalogou os 6 temas responsáveis por 88% das devoluções de processos (Pesquisa de Preços, LRF, Qualificação Técnica, Não Fracionamento, Riscos e IMR/SLA).\n"
    "   • O ANNONA entrega a redação preventiva padrão antes do processo tramitar.\n\n"
    "3. MASTER CHECKLIST DIGITAL DE 15 ETAPAS:\n"
    "   • Barreira de controle interno da CLC que impede que qualquer processo com vício atinja a mesa de homologação do Procurador-Geral de Justiça."
)
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s6.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 6):\n"
    "Senhor Procurador-Geral, o ANNONA é um escudo protetor para a sua caneta e para a dos nossos gestores. O Tribunal de Contas do Piauí editou recentemente o Acórdão 300/2025, fixando regras duríssimas para adesões a atas de registro de preços. Em vez de esperar uma notificação ou auditoria, a CLC se antecipou: já estruturou a Instrução Normativa e o checklist de conformidade que blindam qualquer processo de carona no MPPI. Além disso, mineramos 662 pareceres jurídicos para eliminar previamente as causas de devolução de processos."
)

# ==============================================================================
# SLIDE 7: VELOCIDADE E BENEFÍCIO DIRETO À ATIVIDADE-FIM
# ==============================================================================
s7 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s7)
add_header(s7, "Celeridade de 70% nas Compras e Promotorias do Interior Equipadas", "BENEFÍCIOS NA PONTA E ATIVIDADE-FIM")

# 3 Blocos de Impacto
add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), border_color=COLOR_GOLD)
tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "COMPRAS DIRETAS EM ATÉ 7 DIAS ÚTEIS"
tf.paragraphs[0].font.size = Pt(12)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD
p = tf.add_paragraph()
p.text = "\n• Processos de pequeno valor demoravam 35 a 45 dias por passarem pela fila da Assessoria Jurídica.\n\n• Com a aplicação automatizada do Parecer Referencial (Art. 53, § 5º), a compra é finalizada em menos de 1 semana.\n\n• Redução de 70% do tempo de tramitação burocrática."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), border_color=COLOR_BLUE)
tb = s7.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "FIM DO 'COMEÇAR DO ZERO'"
tf.paragraphs[0].font.size = Pt(12)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_BLUE
p = tf.add_paragraph()
p.text = "\n• Promotorias e Centros de Apoio não perdem mais semanas redigindo ETP e Termo de Referência.\n\n• O RAG entrega modelos de sucesso já testados em 12 instituições para qualquer necessidade.\n\n• Tempo de elaboração de TR cai de 30 dias para 48 horas."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), border_color=COLOR_EMERALD)
tb = s7.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.2), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "FORÇA PARA A ATIVIDADE-FIM"
tf.paragraphs[0].font.size = Pt(12)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_EMERALD
p = tf.add_paragraph()
p.text = "\n• O MPPI não existe para comprar bens; existe para defender a sociedade.\n\n• Menos dinheiro gasto em custeio = mais orçamento para interiorização e investigações.\n\n• Promotoria de Justiça com ar-condicionado, computador e viatura sem interrupções."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s7.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 7):\n"
    "O objetivo final do Ministério Público não é fazer licitações; é defender a sociedade piauiense, combater a criminalidade, fiscalizar a saúde e a educação. Quando uma compra direta de ar-condicionado ou manutenção de uma promotoria no extremo sul do Piauí demora 45 dias, quem sofre é o promotor e o cidadão na fila. Com o ANNONA e o rito dos pareceres referenciais automatizados, reduzimos esse tempo em até 70%, concluindo a compra em menos de uma semana. Menos burocracia no meio significa mais força na ponta."
)

# ==============================================================================
# SLIDE 8: CUSTO DE DESENVOLVIMENTO: EXATAMENTE R$ 0,00
# ==============================================================================
s8 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s8)
add_header(s8, "Custo Financeiro de Desenvolvimento: Exatamente R$ 0,00", "RESPONSABILIDADE FISCAL & RETORNO DO INVESTIMENTO")

add_card(s8, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), border_color=COLOR_EMERALD)
tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "INVESTIMENTO ORÇAMENTÁRIO ZERO • FORÇA DE TRABALHO 100% PRÓPRIA"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_EMERALD

p = tf.add_paragraph()
p.text = (
    "\n• R$ 0,00 gastos com consultorias externas privadas;\n\n"
    "• R$ 0,00 em aquisição de licenças de software proprietário;\n\n"
    "• Desenvolvimento executado integralmente pela equipe da Coordenação de Licitações e Contratos (CLC/MPPI);\n\n"
    "• Tecnologias contemporâneas de código aberto (Python, Vite, React, Lucide Icons, Recharts);\n\n"
    "• Retorno sobre o Investimento (ROI): Infinito, com potencial de economia anual de milhões de reais sem onerar o orçamento institucional."
)
p.font.size = Pt(12)
p.font.color.rgb = COLOR_WHITE

s8.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 8):\n"
    "Em tempos de responsabilidade fiscal rigorosa, trago uma informação da qual muito nos orgulhamos: este projeto não custou um único centavo aos cofres do MPPI. Não contratamos consultorias de Brasília ou de São Paulo, não compramos softwares milionários de mercado. Toda a arquitetura de dados, a mineração algorítmica, o banco de 10.504 documentos e o portal web interativo foram construídos pela equipe da CLC em prol do Ministério Público do Piauí."
)

# ==============================================================================
# SLIDE 9: DEMONSTRAÇÃO PRÁTICA DO PORTAL AO VIVO
# ==============================================================================
s9 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s9)
add_header(s9, "Demonstração Prática do Portal ANNONA em Operação Funcional", "TECNOLOGIA EM FUNCIONAMENTO REAL")

add_card(s9, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), border_color=COLOR_GOLD)
tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "O PORTAL ANNONA JÁ ESTÁ PRONTO E OPERANDO EM HTTP://LOCALHOST:5173/"
tf.paragraphs[0].font.size = Pt(14)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD

p = tf.add_paragraph()
p.text = (
    "\n1. PANORAMA REGIONAL: Visualização executiva dos 10.504 documentos e ranking dos 12 órgãos;\n\n"
    "2. SIMULADOR DE DESÁGIO: Cálculo ao vivo de economia projetada e alerta de inexequibilidade;\n\n"
    "3. CONTROLE & MATRIZES: 662 pareceres, 146 riscos e Master Checklist de 15 itens checáveis;\n\n"
    "4. CADERNO NORMATIVO: Minutas de Atos da PGJ (Dispensa, CEAF e Carona) com cópia em 1 clique;\n\n"
    "5. EXPLORADOR SEMÂNTICO RAG: Busca instantânea em toda a base em milissegundos."
)
p.font.size = Pt(12)
p.font.color.rgb = COLOR_WHITE

s9.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 9):\n"
    "Gostaria de convidar Vossas Excelências a verem o ANNONA funcionando ao vivo. Ele não é uma promessa no papel, não é uma ideia abstrata para o futuro: ele está pronto, em operação no nosso servidor local e disponível para uso imediato por todos os servidores do MPPI.\n"
    "(Neste momento, o apresentador gasta 2 minutos demonstrando o portal na tela: faz uma simulação ao vivo de deságio com um valor sugerido pelo PGJ, mostra o checklist e a busca instantânea)."
)

# ==============================================================================
# SLIDE 10: RUMO AO PRÊMIO CNMP 2026 E DELIBERAÇÃO FINAL
# ==============================================================================
s10 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s10)
add_header(s10, "Rumo ao Prêmio CNMP 2026 e Deliberação da Administração Superior", "HOMOLOGAÇÃO & RECONHECIMENTO NACIONAL")

add_card(s10, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), border_color=COLOR_GOLD)
tb = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
tf = tb.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "OS 3 PEDIDOS SUBMETIDOS À ADMINISTRAÇÃO SUPERIOR:"
tf.paragraphs[0].font.size = Pt(14)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = COLOR_GOLD

p = tf.add_paragraph()
p.text = (
    "\n1. APROVAÇÃO E HOMOLOGAÇÃO DO TAP (PROCESSO SEI Nº [Número]):\n"
    "   • Termo de Abertura de Projeto elaborado em estrita conformidade com o Ato PGJ nº 1.254/2022 (Metodologia de Gerenciamento de Projetos do MPPI alinhada ao PMBOK);\n\n"
    "2. PUBLICAÇÃO DAS PROPOSIÇÕES NORMATIVAS DA LEI 14.133/21:\n"
    "   • Minuta de Ato PGJ de Dispensa por Valor com Parecer Referencial;\n"
    "   • Minuta de Ato PGJ de Capacitação CEAF (Inexigibilidade);\n"
    "   • Minuta de Instrução Normativa da CLC para Governança de Carona (Acórdão 300/2025 TCE-PI);\n\n"
    "3. INSCRIÇÃO OFICIAL NO PRÊMIO CNMP 2026 E PRÊMIO MELHORES PRÁTICAS MPPI:\n"
    "   • Autorização para cadastramento pelo interlocutor institucional no Banco Nacional de Projetos (BNP) do CNMP na Categoria 'Governança e Gestão'."
)
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

s10.notes_slide.notes_text_frame.text = (
    "ROTEIRO DE FALA (SLIDE 10):\n"
    "Senhor Procurador-Geral, o PROJETO ANNONA preenche com notas de excelência todos os requisitos do nosso Plano Estratégico Institucional (PEI) e do Prêmio CNMP. Ele coloca o Ministério Público do Estado do Piauí como referência de inovação e vanguarda administrativa para todo o Brasil.\n"
    "Por essas razões, submetemos os autos do processo SEI para a homologação formal do Termo de Abertura de Projeto por Vossa Excelência, solicitando a chancela da Administração Superior para que possamos inscrever oficialmente o MPPI na disputa pelo Prêmio CNMP 2026 na Categoria Governança e Gestão.\n"
    "Muito obrigado e estamos à disposição para os esclarecimentos dos senhores."
)

# Salvar apresentação PPTX
out_pptx = r"E:\Thiago\Dev\Mapeamento TCE\Apresentacao_PROJETO_ANNONA_MPPI.pptx"
prs.save(out_pptx)
print(f"Apresentação executiva salva com sucesso em: {out_pptx}")
