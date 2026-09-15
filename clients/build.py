#!/usr/bin/env python3
"""Build a tradie site from a JSON config.  Usage: python3 clients/build.py clients/<slug>/site.json"""
import json, sys, os, html
cfg=json.load(open(sys.argv[1])); out=os.path.join(os.path.dirname(sys.argv[1]),'index.html')
e=html.escape; tel=cfg['phone'].replace(' ','')
theme={'blue':('#0b5fb8','#f5d000'),'dark':('#0f172a','#f5d000'),'green':('#2f5d3a','#ffffff'),'orange':('#c2410c','#fff7ed'),'navy':('#1b2a41','#ff6b1a')}[cfg.get('theme','blue')]
svc=''.join(f'<div class="card"><h3>{e(s["name"])}</h3><p>{e(s["desc"])}</p>{"<span>"+e(s["price"])+"</span>" if s.get("price") else ""}</div>' for s in cfg['services'])
areas=', '.join(cfg['areas'])
photos=''.join(f'<figure><img src="{e(p["src"])}" alt="{e(p.get("alt",cfg["business"]+" job photo"))}" loading="lazy"></figure>' for p in cfg.get('photos',[]))
revs=''.join(f'<blockquote><span class="stars">★★★★★</span><p>{e(r["text"])}</p><cite>{e(r["by"])}</cite></blockquote>' for r in cfg.get('reviews',[]))
faq=''.join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in cfg.get('faq',[]))
creds=' · '.join(x for x in [cfg.get('licence'),f"ABN {cfg['abn']}" if cfg.get('abn') else '',cfg.get('insured') and 'Fully insured'] if x)
maps=f'<iframe title="Map" loading="lazy" src="https://www.google.com/maps?q={e(cfg["map_query"])}&output=embed"></iframe>' if cfg.get('map_query') else ''
page=f'''<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(cfg['business'])} — {e(cfg['tagline'])}</title><meta name="description" content="{e(cfg['meta'])}">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":cfg.get('schema_type','HomeAndConstructionBusiness'),"name":cfg['business'],"telephone":tel,"areaServed":cfg['areas'],"url":cfg.get('domain',''),"description":cfg['meta']})}</script>
<style>
:root{{--p:{theme[0]};--a:{theme[1]};--ink:#1b2a41;--mute:#5f6b7a;--line:#e3e7ed;--bg:#fff;--card:#f5f7fa}}
*{{box-sizing:border-box;margin:0}}body{{font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5;padding-bottom:4.5rem}}
@media(min-width:48rem){{body{{padding-bottom:0}}}}.wrap{{max-width:64rem;margin:0 auto;padding:0 1.25rem}}a{{color:inherit}}
header{{display:flex;justify-content:space-between;align-items:center;padding:1rem 0;gap:1rem}}.brand{{font-weight:800;font-size:1.25rem;text-decoration:none}}
.btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;font-weight:700;padding:.8rem 1.2rem;border-radius:.3rem}}.btn.alt{{background:var(--a);color:var(--ink)}}
.hero{{background:var(--p);color:#fff;padding:3rem 0}}.hero .tag{{font-size:.9rem;opacity:.9;margin-bottom:.6rem}}.hero h1{{font-size:clamp(1.9rem,5vw,3rem);line-height:1.05;max-width:18ch;margin-bottom:.8rem}}.hero p{{max-width:44ch;margin-bottom:1.25rem;font-size:1.1rem}}.hero .btns{{display:flex;gap:.6rem;flex-wrap:wrap}}
section{{padding:2.75rem 0;border-top:1px solid var(--line)}}h2{{font-size:clamp(1.4rem,3.5vw,2rem);margin-bottom:1.25rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:1rem}}.card{{background:var(--card);border:1px solid var(--line);border-radius:.4rem;padding:1rem}}.card h3{{margin-bottom:.3rem}}.card p{{color:var(--mute)}}.card span{{display:block;margin-top:.5rem;font-weight:700;color:var(--p)}}
.photos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(12rem,1fr));gap:.6rem}}.photos figure{{aspect-ratio:4/3;overflow:hidden;border-radius:.4rem;background:var(--card)}}.photos img{{width:100%;height:100%;object-fit:cover;display:block}}
blockquote{{background:var(--card);border-left:4px solid var(--a);padding:1rem;border-radius:0 .4rem .4rem 0}}.stars{{color:#f5a300}}blockquote p{{margin:.3rem 0}}cite{{color:var(--mute);font-style:normal;font-size:.9rem}}
details{{border-top:1px solid var(--line);padding:.8rem 0}}summary{{font-weight:600;cursor:pointer}}details p{{color:var(--mute);margin-top:.4rem}}
.contact{{background:var(--ink);color:#fff}}.contact h2{{color:#fff}}.contact .g{{display:grid;gap:1.5rem;grid-template-columns:1fr}}@media(min-width:54rem){{.contact .g{{grid-template-columns:1fr 1fr}}}}
.contact a{{text-decoration:none;font-weight:700;border-bottom:2px solid var(--a)}}.contact .big{{font-size:1.4rem;display:block;margin:.5rem 0}}.contact .m{{color:#a3adbb}}
form{{display:grid;gap:.7rem}}input,textarea,select{{font:inherit;padding:.7rem;border-radius:.3rem;border:1px solid #3a4661;background:#0d1322;color:#fff;width:100%}}textarea{{min-height:5rem}}
iframe{{width:100%;height:16rem;border:0;border-radius:.4rem;margin-top:1rem}}footer{{padding:1.25rem 0 2rem;color:var(--mute);font-size:.9rem}}
.bar{{position:fixed;left:0;right:0;bottom:0;display:grid;grid-template-columns:1fr 1fr;gap:.5rem;padding:.6rem .75rem;background:#fff;border-top:1px solid var(--line);z-index:9}}.bar a{{text-align:center;text-decoration:none;font-weight:700;padding:.8rem;border-radius:.3rem}}.bar .c{{background:var(--p);color:#fff}}.bar .q{{background:var(--a);color:var(--ink)}}@media(min-width:48rem){{.bar{{display:none}}}}
</style></head><body>
<div class="wrap"><header><a class="brand" href="#">{e(cfg['business'])}</a><a class="btn" href="tel:{tel}" style="white-space:nowrap">Call now</a></header></div>
<div class="hero"><div class="wrap"><div class="tag">{e(creds)}</div><h1>{e(cfg['headline'])}</h1><p>{e(cfg['sub'])}</p>
<div class="btns"><a class="btn alt" href="#quote">{e(cfg.get('cta','Get a free quote'))}</a><a class="btn" style="background:rgba(255,255,255,.15)" href="tel:{tel}">Call now</a></div>
<p style="margin-top:1.25rem;font-size:.95rem;opacity:.9">Servicing {e(areas)}</p></div></div>
<section><div class="wrap"><h2>What we do</h2><div class="grid">{svc}</div></div></section>
{f'<section><div class="wrap"><h2>Recent work</h2><div class="photos">{photos}</div></div></section>' if photos else ''}
{f'<section><div class="wrap"><h2>What customers say</h2><div class="grid">{revs}</div></div></section>' if revs else ''}
<section><div class="wrap"><h2>About {e(cfg['owner'])}</h2><p style="max-width:60ch">{e(cfg['about'])}</p></div></section>
{f'<section><div class="wrap"><h2>Common questions</h2>{faq}</div></section>' if faq else ''}
<section class="contact" id="quote"><div class="wrap"><h2>Get a quote</h2><div class="g"><div>
<p class="m">Call or text {e(cfg['owner'])} directly</p><a class="big" href="tel:{tel}">{e(cfg['phone'])}</a>
{f'<p class="m">Email</p><a href="mailto:{e(cfg["email"])}">{e(cfg["email"])}</a>' if cfg.get('email') else ''}
<p class="m" style="margin-top:1rem">{e(cfg.get('hours','Mon–Fri 7am–5pm'))}</p>{maps}</div>
<form id="qf" novalidate><input name="name" placeholder="Your name" required><input name="phone" type="tel" placeholder="Your mobile" required><input name="suburb" placeholder="Suburb" required><textarea name="job" placeholder="What do you need done?"></textarea><button class="btn alt" type="submit">Send quote request</button><p id="msg" class="m" aria-live="polite"></p></form>
</div></div></section>
<div class="wrap"><footer>© {e(cfg['business'])} · {e(creds)} · {e(areas)}</footer></div>
<div class="bar"><a class="c" href="tel:{tel}">Call</a><a class="q" href="#quote">Get a quote</a></div>
<script>(function(){{var f=document.getElementById('qf'),m=document.getElementById('msg');f.addEventListener('submit',function(ev){{ev.preventDefault();var d=new FormData(f);if(!d.get('name')||!d.get('phone')){{m.textContent='Add your name and mobile so we can call you back.';return}}var b='Name: '+d.get('name')+'\\nMobile: '+d.get('phone')+'\\nSuburb: '+d.get('suburb')+'\\nJob: '+(d.get('job')||'-');m.textContent='Opening your email app - hit send and we will call you back.';location.href='mailto:{e(cfg.get("email",""))}?subject='+encodeURIComponent('Quote request - '+d.get('suburb'))+'&body='+encodeURIComponent(b)}})}})();</script>
</body></html>'''
open(out,'w').write(page); print('built',out,len(page),'bytes')
