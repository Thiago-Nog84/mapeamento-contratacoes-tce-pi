"""
Cliente HTTP para consumo da API do Portal da Cidadania do TCE-PI.
Documentação: https://sistemas.tce.pi.gov.br/api/portaldacidadania/docs/
"""

import urllib.request
import json
import ssl
from typing import List, Dict, Any, Optional

class TCEPIClient:
    BASE_URL = "https://sistemas.tce.pi.gov.br/api/portaldacidadania"

    def __init__(self, timeout: int = 25):
        self.timeout = timeout
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _get(self, path: str) -> Any:
        url = f"{self.BASE_URL}{path}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))

    # ==========================
    # ÓRGÃOS E MUNICÍPIOS
    # ==========================
    def listar_orgaos_estaduais(self, exercicio: int = 2024) -> List[Dict[str, Any]]:
        """Lista todas as Unidades Gestoras estaduais registradas para o exercício."""
        return self._get(f"/orgaos/lista/{exercicio}")

    def listar_municipios(self) -> List[Dict[str, Any]]:
        """Lista os 224 municípios do Piauí com IDs de UG e metadados."""
        return self._get("/prefeituras")

    def buscar_municipio_por_nome(self, nome: str) -> List[Dict[str, Any]]:
        """Filtra municípios pelo nome."""
        return self._get(f"/prefeituras/{urllib.parse.quote(nome)}")

    # ==========================
    # CALENDÁRIO DE LICITAÇÕES
    # ==========================
    def listar_datas_licitacoes_estado(self) -> List[Dict[str, Any]]:
        """Retorna datas e valores previstos acumulados para licitações estaduais."""
        return self._get("/licitacoes/estado")

    def listar_datas_licitacoes_municipios(self, id_ug: int = 0) -> List[Dict[str, Any]]:
        """
        Retorna datas e valores previstos para licitações municipais.
        id_ug = 0 consolida todos os municípios.
        """
        return self._get(f"/licitacoes/{id_ug}")

    # ==========================
    # PROCEDIMENTOS LICITATÓRIOS
    # ==========================
    def obter_licitacoes_detalhadas(
        self, 
        id_ug: str or int, 
        esfera: int, 
        data_aaaammdd: str, 
        pagina: int = 1, 
        qtde: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtém os procedimentos licitatórios completos cadastrados para a data e UG informadas.
        esfera: 1 (Municipal), 2 (Estadual)
        data_aaaammdd: Data no formato AAAAMMDD (ex: '20260929')
        """
        path = f"/licitacoes/{id_ug}/{esfera}/{data_aaaammdd}?pagina={pagina}&qtdePorPagina={qtde}"
        return self._get(path)

    # ==========================
    # DOCUMENTOS E PRESTAÇÃO DE CONTAS
    # ==========================
    def listar_documentos_estado(self, pagina: int = 1, qtde: int = 50) -> List[Dict[str, Any]]:
        """Lista documentos e prestações de contas enviadas por órgãos estaduais."""
        return self._get(f"/documentos/estado?pagina={pagina}&qtdePorPagina={qtde}")

    def listar_documentos_municipio(self, id_ug: int, pagina: int = 1, qtde: int = 50) -> List[Dict[str, Any]]:
        """Lista documentos enviados por um município ao TCE."""
        return self._get(f"/documentos/{id_ug}?pagina={pagina}&qtdePorPagina={qtde}")

    def listar_documentos_digitalizados_municipio(self, id_ug: int) -> List[Dict[str, Any]]:
        """Lista documentos digitalizados pelo TCE com URLs de download direto."""
        return self._get(f"/documentos/{id_ug}/digitalizados")
