import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"

for ano in [2025, 2026]:
    dt_fim = f"{ano}1231" if ano == 2025 else "20260928"
    for mod_cod, mod_nome in [(6, "Pregao"), (8, "Dispensa"), (9, "Inexigibilidade")]:
        params = f"dataInicial={ano}0101&dataFinal={dt_fim}&codigoModalidadeContratacao={mod_cod}&cnpj=05805924000189&pagina=1&tamanhoPagina=10"
        url = f"{base}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
                tot = data.get("totalRegistros", 0)
                print(f"[{ano}] MPPI {mod_nome}: {tot} registros")
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            print(f"[{ano}] MPPI {mod_nome} HTTPError: {e.code} - {err_msg[:120]}")
        except Exception as e:
            print(f"[{ano}] MPPI {mod_nome} Erro: {e}")
        time.sleep(2)
