#!/usr/bin/env python3
"""Audit generated static pages using the standard library (no pip install).
Run from any location: python scripts/audit-seo.py
Creates reports/seo-audit.csv and reports/seo-audit-summary.json.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET
import csv, json, re

ROOT=Path(__file__).resolve().parents[1]
BASE=json.loads((ROOT/'data/site-config.json').read_text(encoding='utf-8'))['siteUrl']
ARTS=json.loads((ROOT/'data/articles.json').read_text(encoding='utf-8'))
BYSLUG={a['slug']:a for a in ARTS}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=''; self.is_title=False; self.h1=0;self.heading_levels=[]
        self.meta={};self.canonical=[];self.jsonld=[];self.in_schema=False;self.current_schema=''
        self.images=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.is_title=True
        if re.fullmatch(r'h[1-6]',tag):
            self.heading_levels.append(int(tag[1]))
            if tag=='h1':self.h1+=1
        if tag=='meta':
            key=a.get('name') or a.get('property')
            if key:self.meta[key]=a.get('content','')
        if tag=='link' and 'canonical' in a.get('rel','').split():self.canonical.append(a.get('href',''))
        if tag=='script' and a.get('type')=='application/ld+json':self.in_schema=True;self.current_schema=''
        if tag=='img':self.images.append(a)
        if tag=='a':self.links.append(a.get('href',''))
    def handle_data(self,data):
        if self.is_title:self.title+=data
        if self.in_schema:self.current_schema+=data
    def handle_endtag(self,tag):
        if tag=='title':self.is_title=False
        if tag=='script' and self.in_schema:
            try:self.jsonld.append(json.loads(self.current_schema))
            except (ValueError,TypeError):self.jsonld.append(None)
            self.in_schema=False

def expected_url(p):
    rel=p.relative_to(ROOT).as_posix()
    if rel=='index.html':return BASE
    if rel.endswith('/index.html'):return BASE+rel[:-len('index.html')]
    return BASE+rel

def local_href_broken(page,href):
    if not href or href.startswith(('#','mailto:','tel:','javascript:','data:','//')):return False
    parsed=urlparse(href)
    if parsed.scheme in ('http','https'):
        if not href.startswith(BASE):return False
        target=parsed.path[len(urlparse(BASE).path):].lstrip('/')
    elif parsed.scheme:return False
    else:
        path=unquote(parsed.path)
        target=(page.parent/path).resolve()
        if ROOT not in target.parents and ROOT!=target:return False
        return not (target.is_file() or (target/'index.html').is_file())
    candidate=ROOT/target
    return not (candidate.is_file() or (candidate/'index.html').is_file())

xml=ET.parse(ROOT/'sitemap.xml')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap={e.text for e in xml.findall('.//s:loc',ns)}
results=[]
for p in sorted(ROOT.rglob('*.html')):
    page=Page();page.feed(p.read_text(encoding='utf-8'))
    kind='article' if 'bai-viet' in p.parts else ('category' if 'chuyen-muc' in p.parts else p.relative_to(ROOT).as_posix())
    noindex=kind in ('404.html','tim-kiem.html')
    expected='noindex, follow' if noindex else 'index, follow'
    url=expected_url(p)
    expected_schema={'article':'Article','category':'CollectionPage','index.html':'WebPage','gioi-thieu/index.html':'AboutPage','tim-kiem.html':'SearchResultsPage','404.html':'WebPage'}[kind]
    schema_types=[]
    for js in page.jsonld:
        if not isinstance(js,dict):continue
        schema_types.extend([item.get('@type') for item in js.get('@graph',[js]) if isinstance(item,dict)])
    slug=p.parent.name if kind=='article' else None
    keyword=BYSLUG[slug]['primaryKeyword'] if slug in BYSLUG else ''
    issues=[]
    if not 50<=len(page.title)<=60:issues.append('title_not_50_60')
    if not 105<=len(page.meta.get('description',''))<=125:issues.append('description_not_105_125')
    if keyword and keyword.casefold() not in page.title.casefold():issues.append('primary_keyword_missing_in_title')
    if page.h1!=1:issues.append('h1_not_one')
    if page.canonical!=[url]:issues.append('canonical_mismatch')
    if page.meta.get('robots','').replace(' ','').lower()!=expected.replace(' ',''):issues.append('meta_robots_mismatch')
    if (url in sitemap)==noindex:issues.append('sitemap_indexation_mismatch')
    if not page.jsonld or None in page.jsonld or expected_schema not in schema_types:issues.append('schema_type_or_json_invalid')
    if any(not i.get('alt','').strip() for i in page.images):issues.append('image_missing_alt')
    if any(local_href_broken(p,x) for x in page.links):issues.append('internal_link_missing')
    results.append({'type':kind,'file':str(p.relative_to(ROOT)),'canonical':url,'title':page.title,'title_length':len(page.title),'description_length':len(page.meta.get('description','')),'robots':page.meta.get('robots',''),'h1_count':page.h1,'schema_type':expected_schema,'image_count':len(page.images),'internal_links_total':len(page.links),'status':'PASS' if not issues else 'REVIEW','issues':';'.join(issues)})

titles=[r['title'] for r in results]
canonicals=[r['canonical'] for r in results]
if len(titles)!=len(set(titles)):
    for r in results:
        if titles.count(r['title'])>1:r['status']='REVIEW';r['issues']+=';duplicate_title'
if len(canonicals)!=len(set(canonicals)):
    for r in results:
        if canonicals.count(r['canonical'])>1:r['status']='REVIEW';r['issues']+=';duplicate_canonical'
public_urls={r['canonical'] for r in results if r['robots']=='index, follow'}
sitemap_matches=(sitemap==public_urls)
with (ROOT/'reports/seo-audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(results[0].keys()));writer.writeheader();writer.writerows(results)
summary={'pages_audited':len(results),'published_articles':sum(r['type']=='article' for r in results),'categories':sum(r['type']=='category' for r in results),'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']!='PASS' for r in results),'indexable_urls':len(public_urls),'sitemap_urls':len(sitemap),'sitemap_exactly_matches_indexable':sitemap_matches,'noindex_pages':[r['file'] for r in results if r['robots']=='noindex, follow'],'canonical_base':BASE,'unchecked_external_assets':'All article images are bundled; Google Fonts may require network access','seo_score':'Not a Google score'}
(ROOT/'reports/seo-audit-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(0 if summary['failed']==0 and sitemap_matches and len(results)==60 else 1)
