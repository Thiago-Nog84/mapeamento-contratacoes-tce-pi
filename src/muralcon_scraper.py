"""
Extrator de Contratos do TCE-PI no Mural de Contratos (Muralcon).
Permite pesquisar contratos, dispensas e inexigibilidades do Tribunal de Contas do Estado.
"""

import urllib.request
import urllib.parse
import http.cookiejar
import ssl
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

class MuralconScraper:
    BASE_URL = "https://sistemas.tce.pi.gov.br/muralcon"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _criar_sessao(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj),
            urllib.request.HTTPSHandler(context=self.ctx)
        )
        return opener, cj

    def pesquisar_contratos_orgao(self, nome_orgao: str = "TCE - TRIBUNAL DE CONTAS DO ESTADO DO PIAUI") -> List[Dict[str, Any]]:
        """
        Pesquisa contratos registrados para o órgão no Muralcon.
        """
        opener, cj = self._criar_sessao()
        url_index = f"{self.BASE_URL}/"

        # 1. Carregar tela inicial
        req_init = urllib.request.Request(url_index, headers={'User-Agent': 'Mozilla/5.0'})
        resp_init = opener.open(req_init, timeout=self.timeout)
        html_init = resp_init.read().decode('utf-8', errors='ignore')
        soup_init = BeautifulSoup(html_init, 'html.parser')
        view_state = soup_init.find('input', {'name': 'javax.faces.ViewState'})['value']

        # 2. Selecionar órgão no AutoComplete
        post_select = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'tvPrincipal:ug',
            'javax.faces.partial.execute': 'tvPrincipal:ug',
            'javax.faces.behavior.event': 'itemSelect',
            'javax.faces.partial.event': 'itemSelect',
            'j_idt21': 'j_idt21',
            'tvPrincipal:ug_input': nome_orgao,
            'javax.faces.ViewState': view_state
        }

        req_sel = urllib.request.Request(
            url_index,
            data=urllib.parse.urlencode(post_select).encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Faces-Request': 'partial/ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url_index
            }
        )
        resp_sel = opener.open(req_sel, timeout=self.timeout)
        ajax_sel = resp_sel.read().decode('utf-8', errors='ignore')

        vs_match = re.search(r'<update id="[^"]*ViewState[^"]*"><!\[CDATA\[(.*?)\]\]></update>', ajax_sel)
        if vs_match:
            view_state = vs_match.group(1)

        # 3. Disparar botão bPesquisar
        post_search = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'bPesquisar',
            'javax.faces.partial.execute': 'j_idt21',
            'javax.faces.partial.render': 'formResultado growl',
            'bPesquisar': 'bPesquisar',
            'j_idt21': 'j_idt21',
            'tvPrincipal:ug_input': nome_orgao,
            'tvPrincipal_activeIndex': '0',
            'javax.faces.ViewState': view_state
        }

        req_search = urllib.request.Request(
            url_index,
            data=urllib.parse.urlencode(post_search).encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Faces-Request': 'partial/ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url_index
            }
        )

        resp_search = opener.open(req_search, timeout=self.timeout)
        ajax_res = resp_search.read().decode('utf-8', errors='ignore')

        cdata_match = re.search(r'<update id="formResultado[^"]*"><!\[CDATA\[(.*?)\]\]></update>', ajax_res, re.DOTALL)
        html_fragment = cdata_match.group(1) if cdata_match else ajax_res

        soup_res = BeautifulSoup(html_fragment, 'html.parser')
        contratos = []
        table = soup_res.find('table')
        if table:
            rows = table.find_all('tr')
            for r in rows:
                cols = [td.get_text(" ", strip=True) for td in r.find_all('td')]
                if len(cols) >= 6:
                    link_el = r.find('a', href=re.compile(r'detalhecontrato|id='))
                    link_href = link_el.get('href') if link_el else None
                    contratos.append({
                        'numero_contrato': cols[1] if len(cols) > 1 else '',
                        'contratado': cols[2] if len(cols) > 2 else '',
                        'objeto': cols[3] if len(cols) > 3 else '',
                        'valor': cols[4] if len(cols) > 4 else '',
                        'vigencia': cols[5] if len(cols) > 5 else '',
                        'link': f"{self.BASE_URL}/{link_href}" if link_href and not link_href.startswith('http') else link_href,
                        'cols_completas': cols
                    })

        return contratos
