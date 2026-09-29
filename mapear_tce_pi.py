"""
Script de Mapeamento Específico das Contratações do TCE-PI
Órgão Contratante:
- UG 020101: Tribunal de Contas do Estado (TCE)
- UG 020102: Fundo de Modernização do Tribunal de Contas (FMTC)

Coleta:
1. Procedimentos licitatórios no Muralic
2. Catálogo de artefatos de cada procedimento
3. Fornecedores/Credores e despesas contratuais via API
4. Gravação no banco SQLite e exportação JSON
"""

import os
import json
from src.muralic_scraper import MuralicScraper
from src.api_client import TCEPIClient
from src.storage import TCEStorage

def mapear_tce(baixar_artefatos: bool = False, limite_procedimentos: int = 10):
    print("="*75)
    print("  MAPEAMENTO DE CONTRATAÇÕES DO TCE-PI (ÓRGÃO CONTRATANTE)")
    print("  UGs: 020101 (TCE) e 020102 (Fundo de Modernização - FMTC)")
    print("="*75)

    scraper = MuralicScraper()
    api = TCEPIClient()
    storage = TCEStorage("dados_tce.db")

    orgaos_alvo = [
        {"nome": "TCE - TRIBUNAL DE CONTAS DO ESTADO DO PIAUI", "ug": "020101", "sigla": "TCE"},
        {"nome": "FUNDO DE MODERNIZAÇÃO DO TCE", "ug": "020102", "sigla": "FMTC"}
    ]

    total_procedimentos = []

    for alvo in orgaos_alvo:
        nome = alvo["nome"]
        ug = alvo["ug"]
        sigla = alvo["sigla"]
        print(f"\n[+] Buscando procedimentos licitatórios para: {sigla} ({nome})...")
        lics = scraper.pesquisar_licitacoes_orgao(nome)
        print(f"    -> Encontradas {len(lics)} licitações registradas no Muralic.")

        for i, item in enumerate(lics[:limite_procedimentos]):
            id_lic = item['id_licitacao_web']
            ctrl = item['controle_tce']
            num_proc = item['numero_procedimento']
            valor = item['valor_previsto']
            status = item['status']
            objeto = item['objeto']

            print(f"\n    [{i+1}/{min(len(lics), limite_procedimentos)}] {num_proc} ({ctrl}) | Valor: R$ {valor:,.2f}")
            print(f"        Status: {status}")
            print(f"        Objeto: {objeto[:120]}...")

            if id_lic:
                print(f"        -> Inspecionando artefatos da licitação (ID: {id_lic})...")
                proc = scraper.obter_detalhes_e_artefatos(id_lic)
                proc.id_unidade_gestora = ug
                proc.esfera = "Estadual"
                
                print(f"        -> {len(proc.artefatos)} artefatos vinculados:")
                for art in proc.artefatos:
                    print(f"           • [{art.tipo}] {art.nome_arquivo} ({art.descricao})")
                    
                    if baixar_artefatos and art.botao_download_id:
                        dest = os.path.join(os.getcwd(), "downloads", f"TCE_{ug}", str(id_lic))
                        scraper.baixar_artefato(id_lic, art, dest)
                        print(f"             [Download OK] {art.nome_arquivo}")

                storage.salvar_procedimento(proc)
                total_procedimentos.append(proc.to_dict())

    # 2. Consultar Fornecedores/Credores e Execução de Despesas do TCE-PI via API
    print("\n" + "="*75)
    print("  FORNECEDORES E EXECUÇÃO ORÇAMENTÁRIA DO TCE-PI (API)")
    print("="*75)
    
    dados_financeiros = {}
    for alvo in orgaos_alvo:
        ug = alvo["ug"]
        sigla = alvo["sigla"]
        print(f"\n[+] Consultando credores e despesas contratuais da UG {ug} ({sigla})...")
        try:
            credores = api._get(f"/credores/estado/{ug}/2024/lista")
            print(f"    -> {len(credores)} credores/fornecedores cadastrados em 2024:")
            for c in credores[:5]:
                print(f"       • {c.get('nome')} ({c.get('documento')}) | Pago: R$ {c.get('pago', 0):,.2f}")
            
            despesas = api._get(f"/despesas/estado/{ug}/2024/maiores/porElemento")
            print(f"    -> Maiores elementos de despesa em 2024:")
            for d in despesas[:3]:
                print(f"       • {d.get('elemento')}: R$ {d.get('paga', 0):,.2f}")

            dados_financeiros[ug] = {
                "sigla": sigla,
                "credores": credores,
                "despesas_por_elemento": despesas
            }
        except Exception as e:
            print(f"    -> Aviso ao consultar dados financeiros da UG {ug}: {e}")

    # 3. Exportar relatório consolidado
    relatorio = {
        "orgao": "Tribunal de Contas do Estado do Piauí - TCE-PI",
        "unidades_gestoras": orgaos_alvo,
        "total_procedimentos_mapeados": len(total_procedimentos),
        "procedimentos": total_procedimentos,
        "dados_financeiros_fornecedores": dados_financeiros
    }

    out_file = "contratacoes_tce_pi.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print("\n" + "="*75)
    print(f"  MAPEAMENTO DO TCE-PI CONCLUÍDO COM SUCESSO!")
    print(f"  -> Total de procedimentos catalogados: {len(total_procedimentos)}")
    print(f"  -> Base SQLite atualizada: 'dados_tce.db'")
    print(f"  -> Relatório estruturado gerado: '{out_file}'")
    print("="*75)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mapeador de Contratações do TCE-PI")
    parser.add_argument("--download", action="store_true", help="Baixa todos os arquivos e editais em PDF")
    parser.add_argument("--limite", type=int, default=5, help="Quantidade de procedimentos para detalhar artefatos")
    args = parser.parse_args()

    mapear_tce(baixar_artefatos=args.download, limite_procedimentos=args.limite)
