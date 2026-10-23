#!/usr/bin/env python3
"""Render the RU/EN support and privacy pages without third-party dependencies."""
from pathlib import Path
from urllib.parse import quote, urlencode
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
site = json.loads((ROOT / 'content/site.json').read_text())
esc = html.escape
email = site.get('email', '')
if not site.get('owner'):
    raise SystemExit('A verified developer name is required.')
if email and (not re.fullmatch(r'[^\s@<>\"]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email) or email.endswith('.invalid')):
    raise SystemExit('Use the owner-approved public contact email, or leave it empty.')
if site.get('testflight_url') and not re.fullmatch(r'https://testflight\.apple\.com/join/[A-Za-z0-9]+', site['testflight_url']):
    raise SystemExit('Use an actual public TestFlight invitation link.')
contact_url = site['contact_url']

def render(lang, kind, data):
    path = ('' if lang == 'ru' else 'en/') + ('' if kind == 'support' else 'privacy/')
    prefix = '../' * len(Path(path).parts) if path else './'
    def route(page, language=lang):
        return prefix + ('' if language == 'ru' else 'en/') + ('' if page == 'support' else 'privacy/')
    title = data['title' if kind == 'support' else 'privacy_title']
    description = data['description' if kind == 'support' else 'privacy_description']
    nav = ''.join(f'<a href="{route(p)}"'+(' aria-current="page"' if p == kind else '')+f'>{esc(data[p+"_label"])}</a>' for p in ['support','privacy'])
    languages = ''.join(f'<a href="{route(kind,l)}" lang="{l}" hreflang="{l}" aria-label="{name}"'+(' aria-current="true"' if l == lang else '')+f'>{label}</a>' for l,name,label in [('ru','Русский','RU'),('en','English','EN')])
    if email:
        mail = 'mailto:' + email + '?' + urlencode({'subject':data['email_subject'],'body':data['email_body']}, quote_via=quote)
        contact_link = f'<a href="mailto:{esc(email,quote=True)}">{esc(email)}</a>'
        contact_body = f'''<div class="email-line"><a class="email" href="{esc(mail,quote=True)}">{esc(email).replace('@','<wbr>@')}</a><button class="copy" type="button" data-copy-email="{esc(email,quote=True)}" data-success="{esc(data['copied'],quote=True)}" data-fallback="{esc(data['copy_fallback'],quote=True)}" aria-label="{esc(data['copy_label'],quote=True)}" aria-describedby="copy-status"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M15 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h3"/></svg></button></div><a class="primary" href="{esc(mail,quote=True)}">{esc(data['email_button'])} ↗</a><span id="copy-status" class="copy-status" role="status" aria-live="polite"></span>'''
    else:
        contact_link = f'<a href="{esc(contact_url,quote=True)}">GitHub</a>'
        contact_body = f'<p class="contact-pending">{esc(data["contact_pending"])}</p><a class="primary" href="{esc(contact_url,quote=True)}">{esc(data["github_button"])} ↗</a><p class="small">{esc(data["github_note"])}</p>'
    contact = f'<aside class="contact" aria-labelledby="contact-title"><h2 id="contact-title">{esc(data["contact_title"])}</h2><p>{esc(data["contact_intro"])}</p>{contact_body}<p class="small">{esc(data["contact_note"])}</p></aside>'
    if kind == 'support':
        questions = ''.join(f'<details><summary>{esc(q)}</summary><div class="answer">{answer}</div></details>' for q,answer in data['faq'])
        beta_link = site.get('testflight_url','')
        cta = f'<a class="primary" href="{esc(beta_link,quote=True)}">{esc(data["beta_button"])} ↗</a>' if beta_link else ''
        beta_status = data['beta_review'] if beta_link and site.get('testflight_state') != 'testing' else data['beta_pending'] if not beta_link else ''
        beta = f'<section class="beta" aria-labelledby="beta-title"><span class="badge">TestFlight · beta</span><h2 id="beta-title">{esc(data["beta_title"])}</h2><p>{esc(data["beta_intro"])}</p>{cta}<p class="privacy-state">{esc(beta_status)}</p></section>'
        features = '<div class="features">'+''.join(f'<div class="feature"><strong>{esc(v)}</strong><span>{esc(k)}</span></div>' for v,k in data['features'])+'</div>'
        body = f'<div class="intro"><div><p class="eyebrow">{esc(data["eyebrow"])}</p><h1>{esc(title)}</h1><p class="lead">{esc(data["intro"])}</p>{features}{beta}</div>{contact}</div><section class="faq" aria-labelledby="faq-title"><p class="section-label">{esc(data["faq_label"])}</p><h2 id="faq-title">{esc(data["faq_title"])}</h2>{questions}</section><p class="note">{esc(data["privacy_note"])} <a href="{route("privacy")}">{esc(data["privacy_link"])}</a></p>'
    else:
        sections = data['privacy_sections']
        toc = ''.join(f'<a href="#{esc(key,quote=True)}">{esc(heading)}</a>' for key,heading,_ in sections)
        article = ''.join(f'<section aria-labelledby="{esc(key,quote=True)}"><h2 id="{esc(key,quote=True)}">{esc(heading)}</h2>{content.replace("{{email_link}}",contact_link)}</section>' for key,heading,content in sections)
        body = f'<div class="legal-head"><p class="updated">{esc(data["updated_label"])}</p><h1>{esc(title)}</h1><p class="lead">{esc(data["privacy_intro"])}</p><p class="owner">{esc(data["owner_label"])}: {esc(site["owner"])}. {contact_link}</p></div><div class="legal-layout"><nav class="contents" aria-label="{esc(data["contents_label"],quote=True)}"><p>{esc(data["contents_label"])}</p>{toc}</nav><article class="legal">{article}</article></div>'
    page = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#294035"><title>{esc(title)} · Piss on Trees</title><meta name="description" content="{esc(description,quote=True)}"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{site['url']+path}"><link rel="alternate" hreflang="ru" href="{site['url']+('' if kind=='support' else 'privacy/')}"><link rel="alternate" hreflang="en" href="{site['url']+'en/'+('' if kind=='support' else 'privacy/')}"><link rel="icon" type="image/png" href="{prefix}assets/app-icon.png"><link rel="apple-touch-icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script></head><body><a class="skip" href="#main">{esc(data['skip'])}</a><div class="wrap"><header class="header"><a class="brand" href="{route('support')}"><img src="{prefix}assets/app-icon.png" alt="" width="42" height="42">Piss on Trees</a><nav class="nav" aria-label="{esc(data['nav_label'],quote=True)}">{nav}<div class="languages" aria-label="{esc(data['language_label'],quote=True)}">{languages}</div></nav></header><main id="main">{body}</main><footer class="footer"><p>Piss on Trees · {esc(data['footer'])}</p><div class="footer-links"><a href="{route('privacy')}">{esc(data['privacy_label'])}</a>{contact_link}</div></footer></div></body></html>
'''
    dest = OUT / path / 'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(page)

for lang in ['ru','en']:
    data = json.loads((ROOT/f'content/{lang}.json').read_text())
    for kind in ['support','privacy']:
        render(lang,kind,data)
(OUT/'.nojekyll').touch()
print('Built four static pages; public email:', 'configured' if email else 'GitHub/TestFlight contact only')
