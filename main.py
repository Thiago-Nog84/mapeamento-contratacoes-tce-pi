"""
Script Principal - Pipeline de Mapeamento de Contratações e Artefatos do TCE-PI.

Uso:
  python main.py --demo           # Executa uma demonstração completa com extração de procedimento e artefatos
  python main.py --estado         # Lista licitações recentes do Estado
  python main.py --municipios     # Lista licitações recentes dos Municípios
  python main.py --licitacao ID   # Extrai detalhes e artefatos de um ID de licitação específico
"""

import argparse
import os
import sys
from src.api_client import TCEPIClient
from src.muralic_scraper import MuralicScraper
from src.storage import TCEStorage

def executar_demo():
    print("="*70)
    print("ECOSISTEMA DE CONTRATAÇÕES TCE-PI - PIPELINE DE MAPEAMENTO")
    print("="*70)

    client = TCEPIClient()
    scraper = MuralicScraper()
    storage = TCEStorage("dados_tce.db")

    # 1. Obter calendário municipal
    print("\n[1/4] Consultando calendário de licitações na API do Portal da Cidadania...")
    datas = client.listar_datas_licitacoes_municipios(0)
    print(f"-> Encontradas {len(datas)} datas com procedimentos cadastrados.")
    
    if not datas:
        print("Nenhuma data encontrada.")
        return

    # Pegar uma data de exemplo
    data_alvo = datas[0]['link']
    print(f"\n[2/4] Buscando procedimentos da data {data_alvo}...")
    
    # Exemplo: UG 1473 (Acauã) na data 20260929
    id_ug = 1473
    lics = client.obter_licitacoes_detalhadas(id_ug, 1, "20260929")
    print(f"-> Procedimentos encontrados para a UG {id_ug}: {len(lics)}")

    if not lics:
        # Se vazio, busca o primeiro que tiver licitação
        print("Buscando primeiro procedimento com ID válido...")
        id_lic_web = 1174594
    else:
        id_lic_web = lics[0].get('idLicitacaoWeb', 1174594)

    print(f"\n[3/4] Mapeando procedimento e artefatos no Muralic (ID: {id_lic_web})...")
    proc = scraper.obter_detalhes_e_artefatos(id_lic_web)
    
    print("\n" + "-"*50)
    print(f"DETALHES DO PROCEDIMENTO:")
    print(f"  Controle TCE:       {proc.controle_tce}")
    print(f"  Órgão:              {proc.orgao_nome}")
    print(f"  Procedimento:       {proc.numero_procedimento}")
    print(f"  Regime Jurídico:    {proc.regime_juridico}")
    print(f"  Modo de Disputa:    {proc.modo_disputa}")
    print(f"  Critério:           {proc.criterio_julgamento}")
    print(f"  Status:             {proc.status_licitacao}")
    print(f"  Objeto:             {proc.objeto}")
    print(f"  Link Mural:         {proc.link_mural}")
    print("-"*50)
    
    print(f"\nARTEFATOS DO PROCEDIMENTO ({len(proc.artefatos)} encontrados):")
    pasta_downloads = os.path.join(os.getcwd(), "downloads", str(id_lic_web))
    
    for art in proc.artefatos:
        print(f"  [{art.numero_ordem}] Tipo: {art.tipo}")
        print(f"      Descrição: {art.descricao}")
        print(f"      Arquivo:   {art.nome_arquivo} (cadastrado em {art.data_cadastro})")
        
        # Testar download do primeiro artefato (ex: Projeto ou Edital)
        if art.numero_ordem == 1 and art.botao_download_id:
            print(f"      -> Baixando artefato para pasta local...")
            caminho = scraper.baixar_artefato(id_lic_web, art, pasta_downloads)
            print(f"      -> Salvo com sucesso em: {caminho} ({art.tamanho_bytes:,} bytes)")

    # 4. Salvar na base de dados SQLite
    print("\n[4/4] Gravando procedimento e artefatos no banco SQLite local...")
    storage.salvar_procedimento(proc)
    json_path = storage.exportar_para_json()
    print(f"-> Salvo em 'dados_tce.db' e exportado para '{json_path}' com sucesso!")

def main():
    parser = argparse.ArgumentParser(description="Mapeamento do Ecossistema de Contratações do TCE-PI")
    parser.add_argument("--demo", action="store_true", help="Executa demonstração completa")
    parser.add_argument("--licitacao", type=int, help="ID Licitação Web para inspecionar")
    parser.add_argument("--download", action="store_true", help="Baixa todos os artefatos da licitação")

    args = parser.parse_args()

    if args.licitacao:
        scraper = MuralicScraper()
        storage = TCEStorage()
        print(f"Extraindo dados da licitação {args.licitacao}...")
        proc = scraper.obter_detalhes_e_artefatos(args.licitacao)
        print(f"Controle: {proc.controle_tce} | Órgão: {proc.orgao_nome}")
        print(f"Total de artefatos: {len(proc.artefatos)}")
        for a in proc.artefatos:
            print(f" - [{a.tipo}] {a.nome_arquivo}")
            if args.download and a.botao_download_id:
                pasta = os.path.join(os.getcwd(), "downloads", str(args.licitacao))
                scraper.baixar_artefato(args.licitacao, a, pasta)
                print(f"   Arquivo baixado em: {a.caminho_local}")
        storage.salvar_procedimento(proc)
        print("Salvo no banco de dados!")
    else:
        executar_demo()

if __name__ == "__main__":
    main()
