#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render policy Markdown with Python 3's standard library; no build required to host."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
CHROME = json.loads((ROOT / 'scripts/chrome.json').read_text(encoding='utf-8'))
LOCALES = {
    'en': ('English', 'Privacy policy', 'Privacy and information handling for Mop To-Do.'),
    'zh-Hans': ('简体中文', '隐私政策', '拖把待办的信息处理、权限、同步与隐私说明。'),
    'zh-Hant': ('繁體中文', '隱私權政策', '拖把待辦的資訊處理、權限、同步與隱私說明。'),
    'ja': ('日本語', 'プライバシーポリシー', 'Mop To-Do の情報の取り扱いとプライバシー。'),
    'ko': ('한국어', '개인정보 처리방침', 'Mop To-Do 정보 처리 및 개인정보 안내.'),
}


def stem(lang):
    return 'privacy-policy' if lang == 'en' else 'privacy-policy.' + lang


def inline(text):
    text = escape(text)
    return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', r'<a href="\2">\1</a>', text)


def render(markdown):
    """Only headings, paragraphs, lists and links are used in these policy sources."""
    result, paragraph, items = [], [], []

    def flush():
        if paragraph:
            result.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
        if items:
            result.append('<ul>' + ''.join('<li>' + inline(i) + '</li>' for i in items) + '</ul>')
            items.clear()

    for line in markdown.splitlines():
        if line.startswith('# '):
            flush()  # The document supplies its own visible h1.
        elif line.startswith('## '):
            flush()
            result.append('<h2>' + inline(line[3:]) + '</h2>')
        elif line.startswith('- '):
            if paragraph:
                flush()
            items.append(line[2:])
        elif not line.strip():
            flush()
        else:
            if items:
                flush()
            paragraph.append(line.strip())
    flush()
    return '\n'.join(result)


def languages(current):
    links = []
    for lang, (label, _, _) in LOCALES.items():
        active = ' aria-current="page"' if lang == current else ''
        links.append(f'<a href="./{stem(lang)}.html" lang="{lang}"{active}>{label}</a>')
    return '<nav class="policy-languages" aria-label="Privacy policy languages">' + ''.join(links) + '</nav>'


def format_html(text):
    for tag in ('head', 'body', 'header', 'main', 'section', 'article',
                'aside', 'footer', 'nav', 'details', 'div', 'ul', 'li'):
        text = text.replace('><' + tag, '>\n<' + tag)
        text = text.replace('></' + tag, '>\n</' + tag)
    return text


def main():
    for lang, (_, _, description) in LOCALES.items():
        markdown = (ROOT / (stem(lang) + '.md')).read_text(encoding='utf-8')
        title = markdown.splitlines()[0][2:]
        body = render(markdown)
        zh = lang in ('zh-Hans', 'zh-Hant')
        chrome_key = 'zh' if zh else 'en'
        home = './' if zh else './index.en.html'
        back = '回到产品首页' if zh else 'Back to Mop To-Do'
        alternate = ''.join(
            f'<link rel="alternate" hreflang="{code}" href="./{stem(code)}.html">'
            for code in LOCALES
        )
        document = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#fffaf3">
<link rel="canonical" href="https://dreamnest.mrbun.cn/{stem(lang)}">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="icon" type="image/png" href="./assets/app-icon.png">
<link rel="stylesheet" href="./styles.css">
{alternate}
</head>
<body>
{CHROME['header_' + chrome_key]}
<main id="main" class="document">
<p class="eyebrow">MOP TO-DO / PRIVACY</p>
<h1>{escape(title)}</h1>
{languages(lang)}
<article class="prose">{body}</article>
<a class="back-link" href="{home}">← {back}</a>
</main>
{CHROME['footer_' + chrome_key]}
</body>
</html>
'''
        (ROOT / (stem(lang) + '.html')).write_text(format_html(document), encoding='utf-8')
        if lang in ('zh-Hans', 'en'):
            index = ROOT / ('index.en.html' if lang == 'en' else 'index.html')
            original = index.read_text(encoding='utf-8')
            start, end = '<!-- privacy:start -->', '<!-- privacy:end -->'
            if original.count(start) != 1 or original.count(end) != 1:
                raise ValueError(f'Missing or duplicate policy markers in {index.name}')
            prefix, rest = original.split(start)
            _, suffix = rest.split(end)
            updated = prefix + start + '\n' + body + '\n' + end + suffix
            index.write_text(format_html(updated), encoding='utf-8')
    print('Rendered 5 privacy pages and updated both homepages.')


if __name__ == '__main__':
    main()
