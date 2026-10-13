#!/usr/bin/env python3
"""Replace canonical site origin/base path without altering SPORTHUB destinations.
Usage: python scripts/change-base.py https://new-account.github.io/new-repo/
"""
from pathlib import Path
import sys
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'data/site-config.json'
if len(sys.argv)!=2:
 print('Usage: python scripts/change-base.py https://username.github.io/tap-chi-the-thao/');sys.exit(2)
new=sys.argv[1].strip().rstrip('/')+'/'
u=urlparse(new)
if u.scheme!='https' or not u.hostname:
 print('An https:// canonical base URL is required.');sys.exit(2)
old=__import__('json').loads(CONFIG.read_text(encoding='utf8'))['siteUrl']
count=0
for p in list(ROOT.rglob('*.html'))+[ROOT/'robots.txt',ROOT/'sitemap.xml',ROOT/'feed.xml']:
 raw=p.read_text(encoding='utf8')
 text=raw.replace(old,new)
 if text!=raw:p.write_text(text,encoding='utf8');count+=1
CONFIG.write_text(__import__('json').dumps({'siteUrl':new},ensure_ascii=False,indent=2),encoding='utf8')
print(f'Updated {count} public files: {old} => {new}')
