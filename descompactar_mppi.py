import os
import sys
import json
import zipfile
from pathlib import Path
import pdfplumber

sys.stdout.reconfigure(encoding="utf-8")

def categorizar_arquivo(titulo: str, tipo_nome: str) -> tuple:
    txt = (titulo + " " + tipo_nome).lower()
    if any(k in txt for k in ["termo de refer", " tr ", "tr_", "projeto basico"]):
        return "tr", "Termo de Referência"
    if any(k in txt for k in ["estudo t", "etp"]):
        return "etp", "Estudo Técnico Preliminar"
    if any(k in txt for k in ["edital", "aviso de licit", "aviso de dispensa"]):
        return "edital", "Edital / Aviso Convocatório"
    if any(k in txt for k in ["contrato", "minuta", "termo aditivo", "rescisao"]):
        return "contrato", "Contrato / Minuta"
    if any(k in txt for k in ["dfd", "dod", "formalizacao da demanda", "oficializacao"]):
        return "dfd", "Documento de Formalização da Demanda"
    if any(k in txt for k in ["risco", "matriz"]):
        return "mapa_riscos", "Mapa / Matriz de Riscos"
    if any(k in txt for k in ["parecer", "despacho", "nota tecnica"]):
        return "parecer", "Parecer / Despacho Jurídico"
    if any(k in txt for k in ["pesquisa", "preco", "cotacao", "mapa comparativo"]):
        return "pesquisa_precos", "Pesquisa de Preços"
    if any(k in txt for k in ["ratificacao", "homologacao", "adjudicacao", "autorizacao"]):
        return "ratificacao", "Autorização / Ratificação"
    return "outros", "Outros Documentos"

def converter_pdf_para_md(pdf_path: str, meta: dict, saida_base: Path) -> dict:
    try:
        texto_paginas = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pags = len(pdf.pages)
            for i, p in enumerate(pdf.pages):
                txt = p.extract_text() or ""
                if txt.strip():
                    texto_paginas.append(f"<!-- Pagina {i+1} -->\n{txt.strip()}")
        
        if not texto_paginas:
            return None
            
        conteudo_completo = "\n\n".join(texto_paginas)
        resumo = texto_paginas[0][:500].replace("\n", " ").strip()
        
        cat_slug = meta["categoria"]
        cat_dir = saida_base / cat_slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        safe_name = Path(pdf_path).stem[:35]
        md_nome = f"mppi_{meta['ano']}_{meta['num_compra']}_{safe_name}_{cat_slug}.md"
        md_path = cat_dir / md_nome
        
        frontmatter = f"""---
id: {meta['id']}
tipo: {meta['label']}
categoria: {cat_slug}
modalidade: {meta.get('modalidade', 'Pregão')}
ano: {meta['ano']}
arquivo_original: {os.path.basename(pdf_path)}
paginas: {total_pags}
orgao: MPPI
fonte: PNCP
---

# {meta['label']} - MPPI ({meta['num_compra']}/{meta['ano']})

**Órgão:** Ministério Público do Estado do Piauí (MPPI)
**Arquivo:** {os.path.basename(pdf_path)}

## Resumo Inicial
{resumo}

## Conteúdo Integral
{conteudo_completo}
"""
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(frontmatter)
            
        return {
            "id": meta["id"],
            "sigla": meta["label"],
            "categoria": cat_slug,
            "label": meta["label"],
            "modalidade": meta.get("modalidade", "Pregão"),
            "ano": str(meta["ano"]),
            "orgao": "MPPI",
            "arquivo_original": os.path.basename(pdf_path),
            "paginas": str(total_pags),
            "chars": len(conteudo_completo),
            "arquivo_md": str(md_path),
            "texto_resumo": resumo
        }
    except Exception:
        return None

def descompactar_e_indexar_mppi():
    saida_base = Path("corpus_ia")
    indice_path = saida_base / "indice.jsonl"
    
    ultimo_id = 2500
    if indice_path.exists():
        with open(indice_path, "r", encoding="utf-8") as f:
            for l in f:
                try:
                    d = json.loads(l)
                    doc_id = d.get("id", "")
                    if doc_id.startswith("doc_"):
                        num = int(doc_id.replace("doc_", ""))
                        if num > ultimo_id:
                            ultimo_id = num
                except Exception:
                    pass
                    
    novos = 0
    for ano in [2025, 2026]:
        pasta_ano = Path(f"downloads/mppi_pncp_{ano}")
        if not pasta_ano.exists():
            continue
            
        for proc in pasta_ano.iterdir():
            if not proc.is_dir():
                continue
            num_compra = proc.name.split("_")[0]
            
            for arq in proc.iterdir():
                if arq.is_file() and arq.suffix.lower() == ".pdf":
                    # Checar se eh zip
                    try:
                        with open(arq, "rb") as fp:
                            magic = fp.read(4)
                        if magic.startswith(b"PK"):
                            unzip_dir = proc / (arq.stem + "_unpacked")
                            unzip_dir.mkdir(parents=True, exist_ok=True)
                            with zipfile.ZipFile(arq, "r") as zf:
                                zf.extractall(unzip_dir)
                                
                            for root, dirs, files in os.walk(unzip_dir):
                                for f in files:
                                    if f.lower().endswith(".zip"):
                                        nested_zip = Path(root) / f
                                        nested_dir = nested_zip.parent / (nested_zip.stem + "_sub")
                                        nested_dir.mkdir(parents=True, exist_ok=True)
                                        try:
                                            with zipfile.ZipFile(nested_zip, "r") as nz:
                                                nz.extractall(nested_dir)
                                        except Exception:
                                            pass
                                            
                            for root, dirs, files in os.walk(unzip_dir):
                                for f in files:
                                    if f.lower().endswith(".pdf"):
                                        sub_pdf = Path(root) / f
                                        cat_slug, cat_label = categorizar_arquivo(f, "Edital Anexo")
                                        meta = {
                                            "id": f"doc_{ultimo_id + 1:04d}",
                                            "label": cat_label,
                                            "categoria": cat_slug,
                                            "ano": str(ano),
                                            "num_compra": num_compra,
                                            "modalidade": "Pregão Eletrônico"
                                        }
                                        item = converter_pdf_para_md(str(sub_pdf), meta, saida_base)
                                        if item:
                                            ultimo_id += 1
                                            novos += 1
                                            with open(indice_path, "a", encoding="utf-8") as f_idx:
                                                f_idx.write(json.dumps(item, ensure_ascii=False) + "\n")
                    except Exception:
                        pass
                        
    print(f"[CONCLUÍDO] Total de artefatos de pregões descompactados e indexados do MPPI: {novos}")

if __name__ == "__main__":
    descompactar_e_indexar_mppi()
