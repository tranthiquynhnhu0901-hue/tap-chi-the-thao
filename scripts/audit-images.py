#!/usr/bin/env python3
from pathlib import Path
import json, collections, hashlib
from PIL import Image
root=Path(__file__).resolve().parent.parent
articles=json.loads((root/'data/articles.json').read_text(encoding='utf-8'))
assert len(articles)>=48
paths=[root/a['heroImage'] for a in articles]
missing=[str(p) for p in paths if not p.is_file()]
assert not missing,missing
hashes=[]
for p in paths:
 with Image.open(p) as im: im.verify()
 hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
assert len(set(hashes))==len(paths),'Duplicate image bytes'
for p in root.rglob('*.html'):
 s=p.read_text(encoding='utf-8')
 assert 'images.unsplash.com' not in s,p
assert 'images.unsplash.com' not in (root/'assets/css/style.css').read_text(), 'Remote CSS background detected'
print(json.dumps({'article_images':len(paths),'distinct_images':len(set(hashes)),'missing':len(missing),'all_local':True,'categories':dict(collections.Counter(a['category'] for a in articles))},ensure_ascii=False,indent=2))
