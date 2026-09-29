"""
Extrator (Scraper) de Metadados e Artefatos do Mural de Licitações (Muralic) do TCE-PI.
Interage com a interface JSF/PrimeFaces do Muralic para extrair:
- Metadados aprofundados (Regime jurídico, Modo de disputa, Critério de julgamento)
- Tabela de arquivos/artefatos (Editais, Termos de Referência, Projetos Básicos, Planilhas)
- Download sob demanda dos arquivos (PDFs, planilhas)
"""

import urllib.request
import urllib.parse
import http.cookiejar
import ssl
import re
import os
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup

from .models import ProcedimentoLicitatorio, ArtefatoLicitacao

class MuralicScraper:
    BASE_URL = "https://sistemas.tce.pi.gov.br/muralic"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _criar_sessao(self) -> Tuple[urllib.request.OpenerDirector, http.cookiejar.CookieJar]:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj),
            urllib.request.HTTPSHandler(context=self.ctx)
        )
        return opener, cj

    def obter_detalhes_e_artefatos(self, id_licitacao_web: int) -> ProcedimentoLicitatorio:
        """
        Carrega a página do Muralic para o ID especificado e extrai os metadados e a lista de artefatos.
        """
        opener, cj = self._criar_sessao()
        url = f"{self.BASE_URL}/detalhelicitacao.xhtml?id={id_licitacao_web}"
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml,application/xml"
        })
        resp = opener.open(req, timeout=self.timeout)
        html = resp.read().decode('utf-8', errors='ignore')

        soup = BeautifulSoup(html, 'html.parser')

        # Extrair campos da página principal
        orgao = ""
        controle_tce = ""
        cabecalho = soup.find('div', id='cabecalho_content')
        if cabecalho:
            texto = cabecalho.get_text(" ", strip=True)
            m_orgao = re.search(r'ÓRGÃO:\s*(.*?)\s*CONTROLE TCE:', texto)
            if m_orgao:
                orgao = m_orgao.group(1).strip()
            m_ctrl = re.search(r'CONTROLE TCE:\s*([^\s]+)', texto)
            if m_ctrl:
                controle_tce = m_ctrl.group(1).strip()

        # Helper para buscar valor após um rótulo
        def get_field_val(label_pattern: str) -> Optional[str]:
            el = soup.find(text=re.compile(label_pattern, re.I))
            if el and el.parent:
                # 1. Tentar pegar label ou span irmão
                parent = el.parent
                sibling = parent.find_next_sibling(['label', 'span', 'div'])
                if sibling:
                    return sibling.get_text(" ", strip=True)
                
                # 2. Tentar subir para o container grid
                container = el.find_parent('div')
                if container:
                    sibling_div = container.find_next_sibling('div')
                    if sibling_div:
                        return sibling_div.get_text(" ", strip=True)
            return None

        proc = ProcedimentoLicitatorio(
            id_licitacao_web=id_licitacao_web,
            controle_tce=controle_tce,
            orgao_nome=orgao,
            numero_procedimento=get_field_val(r'Nº do procedimento'),
            objeto=get_field_val(r'Objeto'),
            numero_processo_adm=get_field_val(r'Nº do processo admin'),
            data_abertura=get_field_val(r'Data abertura'),
            status_licitacao=get_field_val(r'Status licitação'),
            regime_juridico=get_field_val(r'Regime Jurídico'),
            forma_realizacao=get_field_val(r'Forma Realização'),
            modo_disputa=get_field_val(r'Modo de Disputa'),
            criterio_julgamento=get_field_val(r'Critério julgamento'),
            tipo_objeto=get_field_val(r'Tipo objeto'),
            link_mural=url
        )

        # Agora, expandir a aba de arquivos via AJAX JSF para extrair a lista de artefatos
        try:
            artefatos = self._extrair_artefatos_ajax(opener, url, soup, id_licitacao_web)
            proc.artefatos = artefatos
        except Exception as e:
            print(f"Aviso ao extrair artefatos via AJAX para licitação {id_licitacao_web}: {e}")

        return proc

    def _extrair_artefatos_ajax(
        self, 
        opener: urllib.request.OpenerDirector, 
        url_lic: str, 
        soup_inicial: BeautifulSoup,
        id_licitacao_web: int
    ) -> List[ArtefatoLicitacao]:
        form = soup_inicial.find('form')
        form_id = form.get('id') if form else 'j_idt572'
        view_state_el = soup_inicial.find('input', {'name': 'javax.faces.ViewState'})
        view_state = view_state_el.get('value') if view_state_el else ''

        # Localizar ID do Accordion e da aba de Arquivos
        aba_arquivos = soup_inicial.find(text=re.compile(r'Arquivos', re.I))
        accordion_id = "j_idt162"
        tab_id = "j_idt162:j_idt303"
        if aba_arquivos and aba_arquivos.parent:
            header_div = aba_arquivos.find_parent('div', class_=re.compile(r'ui-accordion-header'))
            if header_div and header_div.get('id'):
                tab_header_id = header_div.get('id')
                tab_id = tab_header_id.replace('_header', '')
                accordion = header_div.find_parent('div', class_=re.compile(r'ui-accordion'))
                if accordion and accordion.get('id'):
                    accordion_id = accordion.get('id')

        post_data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': accordion_id,
            'javax.faces.partial.execute': accordion_id,
            'javax.faces.partial.render': accordion_id,
            f'{accordion_id}_tabChange': 'true',
            f'{accordion_id}_newTab': tab_id,
            f'{accordion_id}_active': '4',
            form_id: form_id,
            'javax.faces.ViewState': view_state
        }

        req = urllib.request.Request(
            url_lic,
            data=urllib.parse.urlencode(post_data).encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Faces-Request': 'partial/ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url_lic
            }
        )
        resp = opener.open(req, timeout=self.timeout)
        ajax_content = resp.read().decode('utf-8', errors='ignore')

        # Parsear a tabela arquivosLicitacao dentro do fragmento retornado
        import warnings
        from bs4 import XMLParsedAsHTMLWarning
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

        # O PrimeFaces retorna o HTML encapsulado em CDATA dentro de <update>
        cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', ajax_content, re.DOTALL)
        html_fragment = cdata_match.group(1) if cdata_match else ajax_content

        soup_ajax = BeautifulSoup(html_fragment, 'html.parser')
        artefatos = []
        table = soup_ajax.find('tbody', id=re.compile(r'arquivosLicitacao_data'))
        if table:
            rows = table.find_all('tr')
            for r in rows:
                cols = r.find_all('td')
                if len(cols) >= 5:
                    ordem_str = cols[0].get_text(strip=True)
                    tipo = cols[1].get_text(strip=True)
                    descricao = cols[2].get_text(strip=True)
                    nome_arquivo = cols[3].get_text(strip=True)
                    data_cad = cols[4].get_text(strip=True)
                    
                    btn = cols[-1].find('button')
                    btn_id = btn.get('id') if btn else None

                    try:
                        ordem = int(ordem_str)
                    except ValueError:
                        ordem = len(artefatos) + 1

                    artefatos.append(
                        ArtefatoLicitacao(
                            id_licitacao_web=id_licitacao_web,
                            numero_ordem=ordem,
                            tipo=tipo,
                            descricao=descricao,
                            nome_arquivo=nome_arquivo,
                            data_cadastro=data_cad,
                            botao_download_id=btn_id
                        )
                    )

        return artefatos

    def baixar_artefato(
        self, 
        id_licitacao_web: int, 
        artefato: ArtefatoLicitacao, 
        diretorio_destino: str
    ) -> Optional[str]:
        """
        Baixa o arquivo físico do artefato e salva no diretório de destino.
        Retorna o caminho absoluto do arquivo salvo.
        """
        if not artefato.botao_download_id:
            return None

        opener, cj = self._criar_sessao()
        url = f"{self.BASE_URL}/detalhelicitacao.xhtml?id={id_licitacao_web}"

        # 1. Carregar página
        resp = opener.open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
        html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        view_state = soup.find('input', {'name': 'javax.faces.ViewState'})['value']

        # 2. Expandir aba
        accordion_id = "j_idt162"
        tab_id = "j_idt162:j_idt303"
        form_id = "j_idt572"

        post_data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': accordion_id,
            'javax.faces.partial.execute': accordion_id,
            'javax.faces.partial.render': accordion_id,
            f'{accordion_id}_tabChange': 'true',
            f'{accordion_id}_newTab': tab_id,
            f'{accordion_id}_active': '4',
            form_id: form_id,
            'javax.faces.ViewState': view_state
        }

        req_ajax = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(post_data).encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Faces-Request': 'partial/ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url
            }
        )
        resp_ajax = opener.open(req_ajax)
        ajax_content = resp_ajax.read().decode('utf-8', errors='ignore')

        # Atualizar ViewState
        vs_match = re.search(r'<update id="[^"]*ViewState[^"]*"><!\[CDATA\[(.*?)\]\]></update>', ajax_content)
        if vs_match:
            view_state = vs_match.group(1)

        # 3. Submeter formulário do botão de download
        # O formulário interno da tabela é tipicamente j_idt162:j_idt304
        form_arquivos = "j_idt162:j_idt304"
        post_dl = {
            form_arquivos: form_arquivos,
            artefato.botao_download_id: artefato.botao_download_id,
            'javax.faces.ViewState': view_state
        }

        req_dl = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(post_dl).encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': url
            }
        )

        resp_dl = opener.open(req_dl)
        conteudo = resp_dl.read()

        os.makedirs(diretorio_destino, exist_ok=True)
        # Limpar caracteres inválidos no nome do arquivo
        nome_limpo = re.sub(r'[\\/*?:"<>|]', '_', artefato.nome_arquivo)
        caminho_final = os.path.join(diretorio_destino, nome_limpo)

        with open(caminho_final, 'wb') as f:
            f.write(conteudo)

        artefato.caminho_local = caminho_final
        artefato.tamanho_bytes = len(conteudo)
        return caminho_final

    def pesquisar_licitacoes_orgao(self, nome_orgao: str = "TCE - TRIBUNAL DE CONTAS DO ESTADO DO PIAUI") -> List[dict]:
        """
        Pesquisa e retorna todas as licitações do órgão informado no Muralic.
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
            'j_idt20': 'j_idt20',
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

        # 3. Disparar btnPesquisar via AJAX
        post_search = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'btnPesquisar',
            'javax.faces.partial.execute': 'j_idt20',
            'javax.faces.partial.render': 'growl j_idt20 formListaLic:listaLic',
            'btnPesquisar': 'btnPesquisar',
            'j_idt20': 'j_idt20',
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
        ajax_result = resp_search.read().decode('utf-8', errors='ignore')

        # Extrair tabela do fragmento CDATA
        cdata_match = re.search(r'<update id="formListaLic:listaLic[^"]*"><!\[CDATA\[(.*?)\]\]></update>', ajax_result, re.DOTALL)
        if not cdata_match:
            cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', ajax_result, re.DOTALL)

        html_frag = cdata_match.group(1) if cdata_match else ajax_result
        soup_res = BeautifulSoup(html_frag, 'html.parser')

        resultados = []
        rows = soup_res.find_all('tr')
        for r in rows:
            cols = [td.get_text(" ", strip=True) for td in r.find_all('td')]
            if len(cols) >= 12:
                # O link com o id da licitação fica em cols[21] ou em alguma coluna com 'detalhelicitacao'
                link_href = ""
                for c in cols:
                    if 'detalhelicitacao.xhtml?id=' in c:
                        link_href = c
                        break
                
                id_lic = None
                if link_href:
                    m_id = re.search(r'id=(\d+)', link_href)
                    if m_id:
                        id_lic = int(m_id.group(1))

                # Extrair valor previsto float
                val_str = cols[12] if len(cols) > 12 else "0"
                val_str = val_str.replace('\xa0', '').replace('.', '').replace(',', '.')
                try:
                    valor = float(val_str)
                except ValueError:
                    valor = 0.0

                resultados.append({
                    'id_licitacao_web': id_lic,
                    'orgao': cols[0] if len(cols) > 0 else nome_orgao,
                    'esfera': cols[1] if len(cols) > 1 else 'Estadual',
                    'controle_tce': cols[2] if len(cols) > 2 else '',
                    'numero_procedimento': cols[3] if len(cols) > 3 else '',
                    'regime_juridico': cols[4] if len(cols) > 4 else '',
                    'modalidade': cols[5] if len(cols) > 5 else '',
                    'forma_realizacao': cols[6] if len(cols) > 6 else '',
                    'criterio_julgamento': cols[7] if len(cols) > 7 else '',
                    'tipo_objeto': cols[8] if len(cols) > 8 else '',
                    'objeto': cols[9] if len(cols) > 9 else '',
                    'data_abertura': cols[10] if len(cols) > 10 else '',
                    'valor_previsto': valor,
                    'status': cols[14] if len(cols) > 14 else '',
                    'link_detalhe': link_href
                })

        return resultados

