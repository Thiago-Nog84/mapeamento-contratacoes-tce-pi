# -*- coding: utf-8 -*-
import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()
url = "https://sistemas.tce.pi.gov.br/api/portaldacidadania/licitacoes/estado?pagina=1&qtdePorPagina=2"

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        print("Status Code:", resp.status)
        data = json.loads(resp.read().decode("utf-8"))
        print("Tipo de dado retornado:", type(data))
        print("Dados:", json.dumps(data, indent=2, ensure_ascii=False)[:600])
except Exception as e:
    print("Erro ao consultar:", e)
