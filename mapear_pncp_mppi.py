"""
Mapeamento de Contratações e Artefatos do MPPI via API Oficial do PNCP.
Abrange: Pregões Eletrônicos, Dispensas de Licitação e Inexigibilidades.

Uso:
  python mapear_pncp_tce.py                # Lista contratações de 2026 de todas as modalidades
  python mapear_pncp_tce.py --ano 2025    # Consulta ano de 2025
  python mapear_pncp_tce.py --download     # Baixa todos os arquivos dos certames
"""

import argparse
import os
import json
from src.pncp_client import PNCPClient

def mapear_pncp(ano: int = 2026, baixar: bool = False):
    print("="*75)
    print(f"  MAPEAMENTO DE CONTRATAÇÕES DO MPPI VIA API DO PNCP ({ano})")
    print(f"  CNPJ TCE: {'05805924000189'} | CNPJ FMTC: {'10551559000163'}")
    print("="*75)

    client = PNCPClient()
    modalidades = [
        (6, "Pregão Eletrônico"),
        (8, "Dispensa de Licitação"),
        (9, "Inexigibilidade de Licitação")
    ]

    total_coletado = []

    for mod_cod, mod_nome in modalidades:
        print(f"\n[+] Consultando {mod_nome} (código {mod_cod}) no PNCP...")
        import time
        pagina = 1
        total_reg = 1
        itens_coletados = 0
        
        while itens_coletados < total_reg:
            resultado = client.consultar_contratacoes(
                cnpj='05805924000189',
                ano=ano,
                codigo_modalidade=mod_cod,
                pagina=pagina,
                tamanho_pagina=50
            )
            if pagina == 1:
                total_reg = resultado.get('totalRegistros', 0)
                print(f"    -> {total_reg} contratações encontradas.")
            
            items = resultado.get('data', [])
            if not items:
                break
                
            for it in items:
                itens_coletados += 1
                seq = it.get('sequencialCompra')
                num = it.get('numeroCompra')
                obj = it.get('objetoCompra', '')
                val = it.get('valorTotalEstimado', 0.0)

                # Buscar arquivos anexos da compra no PNCP
                arquivos = client.listar_arquivos_contratacao('05805924000189', ano, seq)

                registro = {
                    "modalidade": mod_nome,
                    "codigo_modalidade": mod_cod,
                    "numero_compra": num,
                    "ano": ano,
                    "sequencial_pncp": seq,
                    "numero_controle_pncp": it.get('numeroContratacaoPNCP'),
                    "objeto": obj,
                    "valor_estimado": val,
                    "total_arquivos": len(arquivos),
                    "arquivos": []
                }

                print(f"    • {num}/{ano} (Seq: {seq}) | R$ {val:,.2f} | {len(arquivos)} arquivos")
                print(f"      Objeto: {obj[:100]}...")

                for a in arquivos:
                    tipo_doc = a.get('tipoDocumentoNome', 'Documento')
                    titulo = a.get('titulo')
                    seq_doc = a.get('sequencialDocumento')
                    url_doc = f"{client.BASE_PNCP}/orgaos/{'05805924000189'}/compras/{ano}/{seq}/arquivos/{seq_doc}"

                    caminho_local = None
                    if baixar:
                        pasta = os.path.join(os.getcwd(), "downloads", "PNCP", f"{ano}_{mod_nome}", str(seq))
                        nome_arq = f"{seq_doc}_{titulo}.pdf"
                        destino = os.path.join(pasta, nome_arq)
                        try:
                            caminho_local = client.baixar_arquivo('05805924000189', ano, seq, seq_doc, destino)
                            print(f"        [Download OK] {titulo} -> {caminho_local}")
                        except Exception as e:
                            print(f"        [Erro Download] {titulo}: {e}")

                    registro["arquivos"].append({
                        "tipo": tipo_doc,
                        "titulo": titulo,
                        "sequencial_documento": seq_doc,
                        "url_download": url_doc,
                        "caminho_local": caminho_local
                    })

                total_coletado.append(registro)
            
        pagina += 1

    # Exportar JSON consolidado
    out_file = f"contratacoes_mppi_pncp_{ano}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(total_coletado, f, indent=2, ensure_ascii=False)

    print("\n" + "="*75)
    print(f"  MAPEAMENTO PNCP CONCLUÍDO COM SUCESSO!")
    print(f"  -> Total de contratações mapeadas: {len(total_coletado)}")
    print(f"  -> Arquivo gerado: '{out_file}'")
    print("="*75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mapeador de Contratações do MPPI no PNCP")
    parser.add_argument("--ano", type=int, default=2026, help="Ano das contratações")
    parser.add_argument("--download", action="store_true", help="Baixa todos os arquivos e editais do PNCP")
    args = parser.parse_args()

    mapear_pncp(ano=args.ano, baixar=args.download)
