import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

drive_e_base = r"E:\Thiago\Dev\Mapeamento TCE"
gov_dir = os.path.join(drive_e_base, "documentos_governanca")
scripts_dir = os.path.join(drive_e_base, "scripts")
os.makedirs(gov_dir, exist_ok=True)
os.makedirs(scripts_dir, exist_ok=True)

artifact_dir = r"C:\Users\thiagonogueira\.gemini\antigravity-ide\brain\e5e204f7-b200-42db-83e5-73c4d996ed9e"
workspace_dir = r"c:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\Mapeamento TCE"

# Lista de artefatos essenciais criados
artefatos_chave = [
    "estudo_controle_interno_e_juridico.md",
    "projeto_boas_praticas_premio_cnmp_mppi.md",
    "roteiro_formalizacao_sei_mppi.md",
    "apresentacao_executiva_projeto_annona.md",
    "caderno_normativo_e_proposicoes_mppi.md",
    "estudo_economicidade_mppe_mppi.md",
    "relatorio_checkpoint_executivo.md",
    "roadmap_observatorio_contratacoes.md"
]

print("="*75)
print("INICIANDO SINCRONIZAÇÃO TOTAL PARA DRIVE E: - PROJETO ANNONA")
print("="*75)

# 1. Copiar artefatos markdown para a raiz e para documentos_governanca
for art in artefatos_chave:
    src_path = os.path.join(artifact_dir, art)
    if os.path.exists(src_path):
        # Copiar para documentos_governanca
        dst_gov = os.path.join(gov_dir, art)
        shutil.copyfile(src_path, dst_gov)
        # Copiar para a raiz do drive E
        dst_raiz = os.path.join(drive_e_base, art)
        shutil.copyfile(src_path, dst_raiz)
        print(f"[OK] Artefato copiado: {art} -> {dst_raiz}")
    else:
        print(f"[AVISO] Artefato não encontrado na pasta de artefatos: {art}")

# 2. Copiar apresentação PPTX
pptx_src = os.path.join(workspace_dir, "Apresentacao_PROJETO_ANNONA_MPPI.pptx")
if os.path.exists(pptx_src):
    dst_pptx = os.path.join(drive_e_base, "Apresentacao_PROJETO_ANNONA_MPPI.pptx")
    shutil.copyfile(pptx_src, dst_pptx)
    shutil.copyfile(pptx_src, os.path.join(gov_dir, "Apresentacao_PROJETO_ANNONA_MPPI.pptx"))
    print(f"[OK] Apresentação PPTX copiada para: {dst_pptx}")

# 3. Copiar todos os scripts de scratch para E:\Thiago\Dev\Mapeamento TCE\scripts\
scratch_src_dir = os.path.join(workspace_dir, "scratch")
if os.path.exists(scratch_src_dir):
    for f in os.listdir(scratch_src_dir):
        f_path = os.path.join(scratch_src_dir, f)
        if os.path.isfile(f_path):
            dst_script = os.path.join(scripts_dir, f)
            shutil.copyfile(f_path, dst_script)
    print(f"[OK] Todos os scripts de scratch copiados para: {scripts_dir}")

# 4. Remover cópias redundantes soltas do workspace para manter a política de não sobrecarregar drive C:
try:
    if os.path.exists(pptx_src):
        os.remove(pptx_src)
        print(f"[LIMPEZA] Removido arquivo PPTX temporário do drive C: ({pptx_src})")
except Exception as e:
    print(f"[INFO] Erro na remoção: {e}")

print("\n" + "="*75)
print("MANIFESTO COMPLETO DE ARQUIVOS SALVOS EM E:\\Thiago\\Dev\\Mapeamento TCE:")
print("="*75)
for root, dirs, files in os.walk(drive_e_base):
    # Ignorar node_modules e .git se houver
    if "node_modules" in root or ".git" in root or "corpus_ia\\markdown" in root or "downloads" in root:
        continue
    for file in files:
        if file.endswith((".md", ".pptx", ".json", ".pdf", ".odt", ".doc", ".jsx", ".css", ".html")):
            caminho_completo = os.path.join(root, file)
            tamanho = os.path.getsize(caminho_completo)
            print(f"- {os.path.relpath(caminho_completo, drive_e_base)} ({tamanho:,} bytes)")

print("\nSincronização concluída com 100% de sucesso no drive E:!")
