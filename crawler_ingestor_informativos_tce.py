# -*- coding: utf-8 -*-
"""
CRAWLER & INGESTOR DE INFORMATIVOS DE JULGAMENTOS DO TCE-PI
Projeto Lic.IA • Observatório de Governança & Compras Públicas (MPPI)

Categorias rastreadas:
1. Plenário Presencial
2. Plenário Virtual
3. Primeira Câmara Presencial
4. Primeira Câmara Virtual
5. Segunda Câmara Presencial
6. Segunda Câmara Virtual

Objetivo:
- Baixar os PDFs dos Informativos de Julgamentos
- Extrair texto com pypdf
- Estruturar em banco SQLite (dados_jurisprudencia_tce.db)
- Gerar corpus para RAG (corpus_ia/jurisprudencia_tce.json)
"""

import sys
import io
import os
import re
import ssl
import json
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

try:
    import pypdf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

# Configuração de encoding e SSL
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
CTX = ssl._create_unverified_context()

BASE_DIR = r"E:\Thiago\Dev\Mapeamento TCE"
PDF_DIR = os.path.join(BASE_DIR, "jurisprudencia_tce", "informativos_pdf")
DB_PATH = os.path.join(BASE_DIR, "dados_jurisprudencia_tce.db")
CORPUS_DIR = os.path.join(BASE_DIR, "corpus_ia")

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(CORPUS_DIR, exist_ok=True)

CATEGORIAS = [
    {
        "nome": "Plenário Presencial",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-sessao-plenaria/"
    },
    {
        "nome": "Plenário Virtual",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-pleno-virtual/"
    },
    {
        "nome": "Primeira Câmara Presencial",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-primeira-camara/"
    },
    {
        "nome": "Primeira Câmara Virtual",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-primeira-camara-virtual/"
    },
    {
        "nome": "Segunda Câmara Presencial",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-segunda-camara/"
    },
    {
        "nome": "Segunda Câmara Virtual",
        "url": "https://www.tcepi.tc.br/category/downloads/publicacoes/informativos-de-julgamentos/informativos-segunda-camara-virtual/"
    }
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS informativos_tce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colegiado TEXT,
            titulo_sessao TEXT,
            data_sessao TEXT,
            url_post TEXT UNIQUE,
            url_pdf TEXT,
            arquivo_pdf TEXT,
            texto_completo TEXT,
            total_paginas INTEGER,
            data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS julgados_tce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            informativo_id INTEGER,
            colegiado TEXT,
            data_sessao TEXT,
            relator TEXT,
            numero_processo TEXT,
            tipo_processo TEXT,
            unidade_gestora TEXT,
            objeto TEXT,
            resumo_julgamento TEXT,
            texto_bruto TEXT,
            FOREIGN KEY (informativo_id) REFERENCES informativos_tce(id)
        )
    """)
    conn.commit()
    conn.close()

def extrair_posts_categoria(cat_url, max_paginas=2):
    posts = []
    for pag in range(1, max_paginas + 1):
        url = cat_url if pag == 1 else f"{cat_url}page/{pag}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=CTX, timeout=12) as resp:
                html = resp.read().decode("utf-8", "ignore")
                soup = BeautifulSoup(html, "html.parser")
                articles = soup.find_all("article")
                if not articles:
                    break
                for art in articles:
                    title_tag = art.find(["h2", "h3", "h1"])
                    link_tag = art.find("a", href=True)
                    if title_tag and link_tag:
                        titulo = title_tag.get_text(" ", strip=True)
                        post_url = link_tag["href"].strip()
                        posts.append((titulo, post_url))
        except Exception as e:
            print(f"    [!] Erro ao acessar {url}: {e}")
            break
    return posts

def obter_pdf_do_post(post_url):
    try:
        req = urllib.request.Request(post_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=CTX, timeout=12) as resp:
            html = resp.read().decode("utf-8", "ignore")
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if ".pdf" in href.lower():
                    return href
    except Exception as e:
        print(f"    [!] Erro ao buscar PDF em {post_url}: {e}")
    return None

def baixar_e_extrair_pdf(pdf_url, filename):
    filepath = os.path.join(PDF_DIR, filename)
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=CTX, timeout=25) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())
        except Exception as e:
            print(f"    [!] Erro ao baixar {pdf_url}: {e}")
            return "", 0, filepath
            
    # Extrair texto
    try:
        reader = pypdf.PdfReader(filepath)
        total_pags = len(reader.pages)
        texto = []
        for p in reader.pages:
            t = p.extract_text() or ""
            texto.append(t)
        return "\n".join(texto), total_pags, filepath
    except Exception as e:
        print(f"    [!] Erro ao ler PDF {filepath}: {e}")
        return "", 0, filepath

def parsear_julgados_do_texto(texto, colegiado, data_sessao):
    """
    Parser semântico de blocos de processos a partir do texto do Informativo do TCE-PI.
    Padrões comuns:
    - TC/001234/2024
    - CONS. NOME DO RELATOR
    - TOMADA DE CONTAS / PREGÃO / REPRESENTAÇÃO
    - Interessado / Unidade Gestora / Objeto
    """
    julgados = []
    # Divide o texto procurando referências a números de processos TC/XXXXXX/XXXX ou Processo nº
    blocos = re.split(r'(?=(?:TC/\d{5,7}/\d{4}|Processo\s*n[º°]?\s*TC[-/]))', texto)
    
    current_relator = "Não identificado"
    
    for b in blocos:
        b_clean = b.strip()
        if not b_clean:
            continue
            
        # Detectar relator se presente nas linhas anteriores
        rel_match = re.search(r'(?:CONS(?:ELHEIRO|\.)?|AUD(?:ITOR|\.)?)\s+([A-Z\s]{4,35})', b_clean)
        if rel_match:
            cand = rel_match.group(1).strip()
            if len(cand) > 3 and not cand.startswith("SESS"):
                current_relator = cand

        # Match número de processo
        proc_match = re.search(r'(TC/\d{5,7}/\d{4})', b_clean)
        if not proc_match:
            continue
            
        num_proc = proc_match.group(1)
        
        # Unidade Gestora
        ug_match = re.search(r'Unidade Gestora:\s*([^.\n]+)', b_clean, re.IGNORECASE)
        ug = ug_match.group(1).strip() if ug_match else "Não informada"
        
        # Objeto
        obj_match = re.search(r'Objeto:\s*([^.\n]+(?:\.[^.\n]+)?)', b_clean, re.IGNORECASE)
        obj = obj_match.group(1).strip() if obj_match else ""
        
        # Tipo de Processo (ex: TOMADA DE CONTAS, DENUNCIA, REPRESENTACAO, PRESTAÇÃO DE CONTAS)
        tipo = "Outros"
        tipos_conhecidos = [
            "TOMADA DE CONTAS", "REPRESENTAÇÃO", "DENÚNCIA", "PRESTAÇÃO DE CONTAS", 
            "RECURSO", "AGRAVO", "EMBARGOS", "CONSULTA", "MEDIDA CAUTELAR", "AUDITORIA"
        ]
        for tk in tipos_conhecidos:
            if tk in b_clean.upper():
                tipo = tk
                break
                
        # Resumo do Julgamento (Decisão / Voto)
        decisao = ""
        dec_match = re.search(r'(?:Decisão|Decidiu|Julgamento|Resultado|Acórdão):\s*([^.\n]+(?:\.[^.\n]+)?)', b_clean, re.IGNORECASE)
        if dec_match:
            decisao = dec_match.group(1).strip()
        else:
            # Pega as primeiras linhas do bloco
            linhas = [l.strip() for l in b_clean.split("\n") if l.strip()]
            decisao = " | ".join(linhas[:3])[:250]

        julgados.append({
            "colegiado": colegiado,
            "data_sessao": data_sessao,
            "relator": current_relator,
            "numero_processo": num_proc,
            "tipo_processo": tipo,
            "unidade_gestora": ug,
            "objeto": obj[:400],
            "resumo_julgamento": decisao[:400],
            "texto_bruto": b_clean[:2000]
        })
        
    return julgados

def executar_extracao(max_paginas_por_categoria=2):
    print("=" * 80)
    print(" INICIANDO CRAWLER DE JURISPRUDÊNCIA & INFORMATIVOS DE JULGAMENTOS DO TCE-PI")
    print(" Projeto Lic.IA • Módulo de Governança Jurisprudencial")
    print("=" * 80)
    
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    total_informativos = 0
    total_julgados = 0
    corpus_julgados = []

    for cat in CATEGORIAS:
        nome_cat = cat["nome"]
        url_cat = cat["url"]
        print(f"\n[+] Rastreando Colegiado: {nome_cat}...")
        posts = extrair_posts_categoria(url_cat, max_paginas=max_paginas_por_categoria)
        print(f"    -> Encontradas {len(posts)} sessões publicadas.")
        
        for titulo, post_url in posts:
            # Verificar se já foi baixado
            cur.execute("SELECT id FROM informativos_tce WHERE url_post = ?", (post_url,))
            existe = cur.fetchone()
            if existe:
                continue

            pdf_url = obter_pdf_do_post(post_url)
            if not pdf_url:
                continue
                
            # Extrair data da sessão a partir do título (ex: '... 17 de setembro de 2026')
            data_match = re.search(r'(\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})', titulo, re.IGNORECASE)
            data_sessao = data_match.group(1) if data_match else ""

            # Nome seguro para o arquivo
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', f"{nome_cat}_{titulo}")[:80] + ".pdf"
            print(f"    [>] Ingerindo: {titulo[:65]}...")
            
            texto, total_pags, filepath = baixar_e_extrair_pdf(pdf_url, safe_name)
            if not texto:
                continue
                
            cur.execute("""
                INSERT INTO informativos_tce 
                (colegiado, titulo_sessao, data_sessao, url_post, url_pdf, arquivo_pdf, texto_completo, total_paginas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome_cat, titulo, data_sessao, post_url, pdf_url, safe_name, texto, total_pags))
            info_id = cur.lastrowid
            total_informativos += 1
            
            # Parsear julgados específicos
            julgados = parsear_julgados_do_texto(texto, nome_cat, data_sessao)
            for j in julgados:
                cur.execute("""
                    INSERT INTO julgados_tce
                    (informativo_id, colegiado, data_sessao, relator, numero_processo, tipo_processo, unidade_gestora, objeto, resumo_julgamento, texto_bruto)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (info_id, j["colegiado"], j["data_sessao"], j["relator"], j["numero_processo"], j["tipo_processo"], j["unidade_gestora"], j["objeto"], j["resumo_julgamento"], j["texto_bruto"]))
                total_julgados += 1
                corpus_julgados.append(j)

            conn.commit()

    conn.close()

    # Exportar corpus em JSON para consumo da IA
    corpus_file = os.path.join(CORPUS_DIR, "jurisprudencia_tce_julgados.json")
    with open(corpus_file, "w", encoding="utf-8") as f:
        json.dump(corpus_julgados, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print(f" EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f" Total de Informativos de Julgamentos baixados: {total_informativos}")
    print(f" Total de Julgados/Processos estruturados no banco: {total_julgados}")
    print(f" Banco SQLite: {DB_PATH}")
    print(f" Corpus JSON para RAG: {corpus_file}")
    print("=" * 80)

if __name__ == "__main__":
    executar_extracao(max_paginas_por_categoria=2)
