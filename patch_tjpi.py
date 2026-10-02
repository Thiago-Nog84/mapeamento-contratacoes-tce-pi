import re

with open("extrair_tjpi.py", "r", encoding="utf-8") as f:
    code = f.read()

# Make sure existing files are tracked to avoid duplicate entries
patch = """def executar_extracao_tjpi():
    saida_base = Path("corpus_ia")
    indice_path = saida_base / "indice.jsonl"
    
    ultimo_id = 3000
    ja_indexados = set()
    if indice_path.exists():
        with open(indice_path, "r", encoding="utf-8") as f:
            for l in f:
                try:
                    d = json.loads(l)
                    doc_id = d.get("id", "")
                    arq_orig = d.get("arquivo_original", "")
                    arq_md = d.get("arquivo_md", "")
                    if arq_orig:
                        ja_indexados.add(arq_orig)
                    if arq_md:
                        ja_indexados.add(os.path.basename(arq_md))
                    if doc_id.startswith("doc_"):
                        num = int(doc_id.replace("doc_", ""))
                        if num > ultimo_id:
                            ultimo_id = num
                except Exception:
                    pass
                    
    novo_id_counter = [ultimo_id + 1]
    total_docs = 0"""

# Check if target is present
if "def executar_extracao_tjpi():" in code:
    idx_start = code.find("def executar_extracao_tjpi():")
    idx_end = code.find("novo_id_counter = [ultimo_id + 1]", idx_start) + len("novo_id_counter = [ultimo_id + 1]\n    total_docs = 0")
    code = code[:idx_start] + patch + code[idx_end:]

# In processar_arquivo_e_descompactar, skip if already indexed
skip_logic = """def processar_arquivo_e_descompactar(pdf_path: Path, meta: dict, saida_base: Path, indice_path: Path, novo_id_counter: list, ja_indexados: set) -> int:
    novos = 0
    if pdf_path.name in ja_indexados:
        return 0"""

code = code.replace("def processar_arquivo_e_descompactar(pdf_path: Path, meta: dict, saida_base: Path, indice_path: Path, novo_id_counter: list) -> int:\n    novos = 0", skip_logic)
code = code.replace("n_docs = processar_arquivo_e_descompactar(pdf_path, base_meta, saida_base, indice_path, novo_id_counter)", "n_docs = processar_arquivo_e_descompactar(pdf_path, base_meta, saida_base, indice_path, novo_id_counter, ja_indexados)")

with open("extrair_tjpi.py", "w", encoding="utf-8") as f:
    f.write(code)

print("extrair_tjpi.py atualizado para retomada perfeita sem duplicatas!")
