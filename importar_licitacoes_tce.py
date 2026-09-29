"""
Módulo de Integração com a API do Portal da Cidadania - TCE-PI
Permite listar órgãos, municípios, datas de licitações e importar os procedimentos licitatórios completos.
"""

import urllib.request
import json
import ssl
from datetime import datetime

class TCEPIClient:
    BASE_URL = "https://sistemas.tce.pi.gov.br/api/portaldacidadania"

    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _get(self, path: str):
        url = f"{self.BASE_URL}{path}"
        req = urllib.request.Request(
            url, 
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, context=self.ctx, timeout=20) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def listar_orgaos_estaduais(self, exercicio: int = 2024):
        """Retorna todos os órgãos e unidades gestoras estaduais."""
        return self._get(f"/orgaos/lista/{exercicio}")

    def listar_municipios(self):
        """Retorna todos os 224 municípios do Piauí com seus IDs de UG."""
        return self._get("/prefeituras")

    def listar_datas_licitacoes_estado(self):
        """Retorna datas com licitações estaduais previstas/cadastradas."""
        return self._get("/licitacoes/estado")

    def listar_datas_licitacoes_municipais(self, id_ug: int = 0):
        """
        Retorna datas com licitações municipais.
        id_ug = 0 consolida todos os municípios.
        """
        return self._get(f"/licitacoes/{id_ug}")

    def obter_licitacoes_detalhadas(self, id_ug: str or int, esfera: int, data_aaaammdd: str, pagina: int = 1, qtde: int = 50):
        """
        Retorna a lista detalhada de licitações para uma UG, esfera e data.
        - esfera: 1 para Municipal, 2 para Estadual
        - data_aaaammdd: formato YYYYMMDD (ex: '20260929')
        """
        path = f"/licitacoes/{id_ug}/{esfera}/{data_aaaammdd}?pagina={pagina}&qtdePorPagina={qtde}"
        return self._get(path)


if __name__ == "__main__":
    client = TCEPIClient()
    print("=== TESTE DE IMPORTAÇÃO - API TCE-PI ===")
    
    # 1. Órgãos estaduais - filtrando TCE-PI
    orgaos = client.listar_orgaos_estaduais(2024)
    tce_ugs = [o for o in orgaos if "020101" in o.get('id', '') or "TCE" in o.get('sigla', '')]
    print(f"UGs encontradas do TCE-PI: {tce_ugs}")

    # 2. Datas de licitações municipais recentes
    datas_mun = client.listar_datas_licitacoes_municipais(0)
    print(f"\nTotal de datas de licitações municipais disponíveis: {len(datas_mun)}")
    if datas_mun:
        primeira_data = datas_mun[0]
        data_link = primeira_data.get('link')
        print(f"Consultando licitações da data: {data_link}...")
        
        # Testar com a primeira UG municipal da lista (ex: Acauã 1473)
        lics = client.obter_licitacoes_detalhadas(1473, 1, "20260929")
        print(f"Licitações retornadas: {len(lics)}")
        for lic in lics:
            print(f" - [{lic.get('unidadeOrcamentaria')}] {lic.get('modalidade')} | Previsto: R$ {lic.get('previsto'):,.2f}")
            print(f"   Objeto: {lic.get('objeto')}")
            print(f"   Link Mural TCE: {lic.get('mural')}")
            print(f"   ID Licitação Web: {lic.get('idLicitacaoWeb')}")
