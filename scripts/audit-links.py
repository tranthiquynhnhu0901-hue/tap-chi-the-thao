#!/usr/bin/env python3
"""Offline audit for static Vietnamese sports magazine. No third party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from urllib.parse import urlparse, unquote
import csv, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={x['url'] for x in json.loads((ROOT/'data/ecosystem-links.json').read_text(encoding='utf-8'))['links']}
PREFIX='https://tranthiquynhnhu0901-hue.github.io/shopthethao/'
class Extract(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.a=[];self.img=[];self.headings=[];self.meta={};self.article_links=[];self.body_links=[];self.tags=[];self.text=[];self.flags=[];self.article_depth=0;self.in_article=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append(tag)
  if tag=='article' and 'article-body' in d.get('class','').split():self.in_article=True;self.article_depth=len(self.tags)
  if tag=='a':
   self.a.append({'href':d.get('href',''),'inside_article':self.in_article})
  if tag=='img':self.img.append(d)
  if tag in ['h1','h2','h3']:self.headings.append(tag)
  if tag=='meta' and d.get('name')=='description':self.meta['description']=d.get('content','')
  if tag=='title':self.flags.append('title')
  if d.get('id')=='tim-hieu-them':self.flags.append('tim-hieu-them')
 def handle_endtag(self,tag):
  if tag=='article' and self.in_article:self.in_article=False
  # stack depth is only used for simple article wrapper
 def handle_data(self,data):self.text.append(data)
def target_exists(href,html_file):
 if not href or href.startswith(('#','mailto:','tel:','javascript:')):return True
 if urlparse(href).scheme or href.startswith('//'):return True
 relative=unquote(href.split('?',1)[0].split('#',1)[0]);target=(html_file.parent/relative)
 if not target.exists():return False
 return (target/'index.html').exists() if target.is_dir() else target.is_file()

def audit():
 paths=sorted((ROOT/'bai-viet').glob('*/index.html'))
 rows=[];links=[];imgs=[];tot=0;broken=0;bad=0;preview=False
 src=json.loads((ROOT/'data/articles.json').read_text(encoding='utf-8'))
 docs={a['slug']:a for a in src}
 for path in paths:
  slug=path.parent.name;a=docs.get(slug,{})
  p=Extract();raw=path.read_text(encoding='utf-8');p.feed(raw)
  sport=[l for l in p.a if l['inside_article'] and l['href'].startswith(PREFIX)]
  internal=[l for l in p.a if l['inside_article'] and l['href'].startswith('../../bai-viet/')]
  duplicate=max(Counter(l['href'] for l in sport).values(),default=0)
  invalid=[l['href'] for l in sport if l['href'] not in ALLOWED]
  miss=[l['href'] for l in p.a if not target_exists(l['href'],path)]
  missing_imgs=[d.get('src','') for d in p.img if not target_exists(d.get('src',''),path)]
  count=len(sport);tot+=count;bad+=len(invalid);broken+=len(miss)+len(missing_imgs)
  concerns=[]
  if count<5 or count>8:concerns.append('Số link SPORTHUB ngoài khoảng 5-8')
  if not 'tim-hieu-them' in p.flags:concerns.append('Thiếu Tìm hiểu thêm')
  if duplicate>2:concerns.append('SPORTHUB URL lặp bất thường trong bài')
  if invalid:concerns.append('URL SPORTHUB không thuộc whitelist')
  if miss:concerns.append('Broken link: '+str(miss[:3]))
  if missing_imgs:concerns.append('Broken image: '+str(missing_imgs[:3]))
  if p.headings.count('h1')!=1:concerns.append('Số H1 khác 1')
  if len(internal)<2:concerns.append('Dưới 2 internal link trong thân bài')
  wc=a.get('wordCount',0)
  if wc<900:concerns.append('Nội dung dưới mốc định hướng 900 từ')
  concerns.append('URL đích SPORTHUB chưa xác minh trực tuyến; các trang danh sách được sử dụng cho anchor chủ đề chung')
  if not raw.count('application/ld+json')>=2:concerns.append('Thiếu structured data Article/Breadcrumb')
  rows.append({'Title':a.get('title',''),'Slug':slug,'Category':a.get('category',''),'Primary keyword':a.get('primaryKeyword',''),'Words':wc,'Meta title':a.get('metaTitle',''),'Meta description':p.meta.get('description',''),'Headings H1':p.headings.count('h1'),'Headings H2':p.headings.count('h2'),'Internal links in body':len(internal),'SPORTHUB links in body':count,'Images':len(p.img),'Technical status':'PASS' if not miss and not missing_imgs and not invalid and 5<=count<=8 and 'tim-hieu-them' in p.flags else 'FAIL','Editorial verification':'PENDING','Issues':'; '.join(concerns)})
  for l in sport:
   links.append({'article':slug,'url':l['href'],'allowlisted':'yes' if l['href'] in ALLOWED else 'no','external_verified':'unverified','duplicates_per_article':Counter(x['href'] for x in sport)[l['href']],'location':'article body'})
  for im in p.img:imgs.append({'article':slug,'image':im.get('src',''),'alt':im.get('alt',''),'path_exists':'yes' if target_exists(im.get('src',''),path) else 'no'})
 (ROOT/'reports').mkdir(exist_ok=True)
 for name,info in [('link-audit.csv',links),('content-audit.csv',rows),('image-path-audit.csv',imgs)]:
  with (ROOT/'reports'/name).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(info[0]));w.writeheader();w.writerows(info)
 report={'published_articles':len(paths),'categories':len({a['category'] for a in src}),'total_sporthub_link_occurrences':tot,'unique_sporthub_destinations_used':len(set(l['url'] for l in links)),'internal_article_links_in_body':sum(int(r['Internal links in body']) for r in rows),'images_referenced_in_article_pages':sum(int(r['Images']) for r in rows),'local_images':len(list((ROOT/'assets/images').glob('*'))),'unverified_sporthub_urls':len(ALLOWED),'remote_photos_pending_load_verification':sum(a['heroImage'].startswith(('https://','http://')) for a in src),'local_image_files_verified':len(list((ROOT/'assets/images').glob('*.webp'))),'invalid_sporthub_url_occurrences':bad,'missing_internal_links_or_images':broken,'articles_meeting_link_count':sum(5<=int(r['SPORTHUB links in body'])<=8 for r in rows),'articles_with_editorial_verification_pending':len(rows),'article_word_count_range':[min(a.get('wordCount',0) for a in src),max(a.get('wordCount',0) for a in src)],'overall_technical_result':'PASS' if len(paths)>=48 and tot>=240 and bad==0 and broken==0 and all(r['Technical status']=='PASS' for r in rows) else 'FAIL','browser_runtime_tests':'See reports/browser-tests.json; not part of this offline script.'}
 (ROOT/'reports/audit-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['overall_technical_result']=='PASS' else 1
if __name__=='__main__':sys.exit(audit())
