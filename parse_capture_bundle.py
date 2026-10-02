# -*- coding: utf-8 -*-
import urllib.request
import ssl
import re

ctx = ssl._create_unverified_context()
url = "https://portal.tce.pi.gov.br/capture/main-es2015.2133e33da242ef436728.js"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    content = resp.read().decode("utf-8", "ignore")

print(f"Baixado {len(content)} bytes.")

# Search for baseUrl or api definitions
apis = set(re.findall(r'https?://[a-zA-Z0-9\.\-]+(?:/[a-zA-Z0-9_\-]+)*/api[a-zA-Z0-9_\-/]*', content))
print(f"APIs explícitas encontradas ({len(apis)}):")
for a in sorted(apis):
    print(" ->", a)

# Search for endpoints matching /processo, /acordao, /decisao, /sessao, /julgamento
patterns = [
    r'\"(/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+)*processo[a-zA-Z0-9_\-/]*)\"',
    r'\"(/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+)*decisao[a-zA-Z0-9_\-/]*)\"',
    r'\"(/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+)*acordao[a-zA-Z0-9_\-/]*)\"',
    r'\"(/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+)*sessao[a-zA-Z0-9_\-/]*)\"',
    r'\"(/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+)*jurisprudencia[a-zA-Z0-9_\-/]*)\"',
]
matches = set()
for p in patterns:
    for m in re.findall(p, content, re.IGNORECASE):
        matches.add(m)

print(f"\nRotas de Julgamento / Processo encontradas ({len(matches)}):")
for m in sorted(matches)[:30]:
    print(" *", m)
