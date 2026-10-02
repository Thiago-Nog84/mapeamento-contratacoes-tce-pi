import urllib.request, ssl, re
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for ep in ['muralic', 'muralcon']:
    url = f'https://portal.tce.pi.gov.br/{ep}/doc/index.html'
    try:
        with urllib.request.urlopen(url, context=ctx) as r:
            html = r.read().decode('utf-8', errors='ignore')
            m = re.findall(r'url:\s*["\']([^"\']+)["\']', html)
            print(f'{ep} spec:', m)
    except Exception as e:
        print(f'{ep} erro:', e)
