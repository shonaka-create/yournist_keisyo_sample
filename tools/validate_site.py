from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re

ROOT=Path(__file__).resolve().parents[1]/'site'
BASE='https://yournist-keisyo-sample.vercel.app'

class Scan(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set(); self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag in ('a','link','script','img'):
            key={'a':'href','link':'href','script':'src','img':'src'}[tag]
            if a.get(key):self.links.append(a[key])

errors=[]; pages=list(ROOT.rglob('*.html'))
for page in pages:
    scan=Scan(); scan.feed(page.read_text(encoding='utf-8'))
    if scan.h1!=1: errors.append(f'H1={scan.h1}: {page.relative_to(ROOT)}')
    for link in scan.links:
        if link.startswith(('http:','https:','mailto:','tel:','data:','javascript:','#')):continue
        path=urlsplit(link).path
        target=(page.parent/path).resolve()
        if path.endswith('/') or not target.suffix: target=target/'index.html'
        if not target.exists():errors.append(f'BROKEN {page.relative_to(ROOT)} -> {link}')

urls=[]
for page in pages:
    rel=page.relative_to(ROOT).as_posix()
    if rel=='index.html':url=BASE+'/'
    else:url=BASE+'/'+rel.removesuffix('index.html')
    urls.append(url)
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in sorted(urls))+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml,encoding='utf-8')
print(f'pages={len(pages)} errors={len(errors)}')
for e in errors:print(e)
raise SystemExit(1 if errors else 0)
