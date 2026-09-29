"""
Cliente HTTP para consumo da API do Portal Nacional de Contratações Públicas (PNCP).
Documentação: https://pncp.gov.br/api/consulta/swagger-ui/index.html
"""

import urllib.request
import urllib.parse
import json
import ssl
import os
from typing import List, Dict, Any, Optional

class PNCPClient:
    BASE_CONSULTA = "https://pncp.gov.br/api/consulta/v1"
    BASE_PNCP = "https://pncp.gov.br/api/pncp/v1"

    # CNPJs oficiais do TCE-PI
    CNPJ_TCE = "05818935000101"   # Tribunal de Contas do Estado
    CNPJ_FMTC = "11536694000100"  # Fundo de Modernização do Tribunal de Contas

    def __init__(self, timeout: int = 25):
        self.timeout = timeout
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _get(self, url: str) -> Any:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def consultar_contratacoes(
        self,
        cnpj: str = CNPJ_TCE,
        ano: int = 2026,
        codigo_modalidade: int = 6,  # 6=Pregão, 8=Dispensa, 9=Inexigibilidade
        pagina: int = 1,
        tamanho_pagina: int = 50
    ) -> Dict[str, Any]:
        """
        Consulta contratações publicadas no PNCP para o órgão e modalidade no ano informado.
        """
        data_ini = f"{ano}0101"
        data_fim = f"{ano}1231"
        params = (
            f"dataInicial={data_ini}&dataFinal={data_fim}"
            f"&codigoModalidadeContratacao={codigo_modalidade}"
            f"&cnpj={cnpj}&pagina={pagina}&tamanhoPagina={tamanho_pagina}"
        )
        url = f"{self.BASE_CONSULTA}/contratacoes/publicacao?{params}"
        return self._get(url)

    def listar_arquivos_contratacao(self, cnpj: str, ano: int, sequencial: int) -> List[Dict[str, Any]]:
        """
        Lista todos os arquivos vinculados a uma contratação no PNCP (Edital, ETP, TR, etc.).
        """
        url = f"{self.BASE_PNCP}/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos"
        try:
            return self._get(url)
        except Exception:
            return []

    def baixar_arquivo(self, cnpj: str, ano: int, sequencial: int, sequencial_documento: int, destino: str) -> str:
        """
        Baixa o arquivo físico do PNCP e salva no caminho de destino.
        """
        url = f"{self.BASE_PNCP}/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos/{sequencial_documento}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
            conteudo = resp.read()

        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "wb") as f:
            f.write(conteudo)
        return destino
