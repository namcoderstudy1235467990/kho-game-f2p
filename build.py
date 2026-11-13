#!/usr/bin/env python3
"""Tạo lại trang chủ, sơ đồ trang và thẻ tìm kiếm cho từng game từ games.json.
Chạy: python3 build.py  (sau mỗi lần thêm/sửa game)"""
import datetime
import html
import json
import os
import re

SITE = 'https://khogamef2p.pages.dev'
NAME = 'Kho Game F2P'
ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
games = json.load(open(os.path.join(ROOT, 'games.json'), encoding='utf-8'))
E = html.escape


def absu(u):
    return u if u.startswith('http') else SITE + '/' + u.lstrip('/')


# ---------- thẻ SEO cho từng game ----------
for g in games:
    if g['url'].startswith('http'):
        continue
    p = os.path.join(ROOT, g['url'], 'index.html')
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    title = f"{g['title']} — {g['genre'].replace(' · ', ', ')} chơi miễn phí | {NAME}"
    desc = g['about'][:300]
    ld = {
        '@context': 'https://schema.org', '@type': 'VideoGame', 'name': g['title'], 'url': absu(g['url']),
        'description': g['about'], 'genre': g['genre_en'], 'inLanguage': 'vi', 'gamePlatform': 'Web browser',
        'applicationCategory': 'Game', 'operatingSystem': 'Any', 'isAccessibleForFree': True,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'VND'},
        'author': {'@type': 'Person', 'name': 'Phạm Vũ Hoài Nam'},
        'publisher': {'@type': 'Organization', 'name': NAME, 'url': SITE + '/'},
    }
    if g.get('cover'):
        ld['image'] = absu(g['cover'])
    block = '\n'.join([
        '<!--SEO-->',
        f'<meta name="description" content="{E(desc)}">',
        f'<meta name="keywords" content="{E(g["keywords"])}, kho game, game online miễn phí">',
        f'<link rel="canonical" href="{absu(g["url"])}">',
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:title" content="{E(g["title"])} — chơi miễn phí trên trình duyệt">',
        f'<meta property="og:description" content="{E(desc)}">',
        f'<meta property="og:url" content="{absu(g["url"])}">',
        (f'<meta property="og:image" content="{absu(g["cover"])}"><meta name="twitter:card" content="summary_large_image">' if g.get('cover') else ''),
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
        '<!--/SEO-->'])
    s = re.sub(r'<!--SEO-->.*?<!--/SEO-->\n?', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description"[^>]*>\n?', '', s)
    s = s.replace('</title>', '</title>\n' + block, 1)
    nos = (f'<noscript><div style="color:#dfe6f5;font:16px system-ui;max-width:640px;margin:40px auto;padding:0 20px">'
           f'<h1>{E(g["title"])}</h1><p>{E(g["about"])}</p><p>Hãy bật JavaScript để chơi. '
           f'<a style="color:#ffe08a" href="{SITE}/">Xem thêm game tại {NAME}</a></p></div></noscript>')
    s = re.sub(r'<noscript>.*?</noscript>\n?', '', s, flags=re.S)
    s = s.replace('<body>', '<body>\n' + nos, 1)
    open(p, 'w', encoding='utf-8').write(s)

# ---------- trang chủ ----------
cards = []
for g in games:
    ext = g['url'].startswith('http')
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    cover = (f'<img src="{E(g["cover"])}" alt="Ảnh game {E(g["title"])}" width="800" height="450" loading="lazy">'
             if g.get('cover') else E(g['title'][0]))
    ctl = f'<div class="ctl">{E(g["controls"])}</div>' if g.get('controls') else ''
    cards.append(f'''<a class="card" href="{E(g["url"])}"{tgt}>
<div class="cv">{cover}</div>
<div class="bd"><div class="tag">{E(g["genre"])}</div><h3>{E(g["title"])}</h3><p>{E(g["desc"])}</p>{ctl}<span class="play">Chơi ngay</span></div></a>''')
cards.append('<div class="card soon"><div>✦</div><div>Game mới sắp ra mắt</div></div>')
credits = '<br>'.join(E(g['title'] + ' — ' + g['credit']) for g in games if g.get('credit'))
ld = [
    {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'alternateName': ['Kho game F2P', 'Kho game online miễn phí'], 'url': SITE + '/', 'inLanguage': 'vi'},
    {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Danh sách game trong ' + NAME,
     'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': absu(g['url']), 'name': g['title']} for i, g in enumerate(games)]},
]
names = ', '.join(g['title'] for g in games)
page = open(os.path.join(ROOT, 'templates', 'home.html'), encoding='utf-8').read()
page = (page.replace('{{CARDS}}', '\n'.join(cards)).replace('{{CREDITS}}', credits)
        .replace('{{LD}}', json.dumps(ld, ensure_ascii=False)).replace('{{NAMES}}', E(names))
        .replace('{{COUNT}}', str(len(games))).replace('{{SITE}}', SITE))
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)

# ---------- sơ đồ trang ----------
urls = [SITE + '/'] + [absu(g['url']) for g in games if not g['url'].startswith('http')] + [SITE + '/gioi-thieu.html', SITE + '/chinh-sach-bao-mat.html']
for g in games:
    if not g['url'].startswith('http') and os.path.exists(os.path.join(ROOT, g['url'], 'credits.html')):
        urls.append(absu(g['url']) + 'credits.html')
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls]
sm.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
print('Đã tạo lại trang chủ, sitemap (%d địa chỉ) và thẻ SEO cho %d game.' % (len(urls), len(games)))
