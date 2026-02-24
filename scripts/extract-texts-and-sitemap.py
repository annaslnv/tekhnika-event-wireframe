#!/usr/bin/env python3
# Извлекает все тексты и карту сайта из HTML-страниц. Результат: teksty-i-karta-sajta.md

import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "teksty-i-karta-sajta.md"

def path_to_url(rel_path):
    if rel_path == "index.html":
        return "/"
    d = os.path.dirname(rel_path)
    return "/" + d + "/" if d else "/"

def strip_html(html):
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&mdash;", "—", text)
    text = re.sub(r"&ndash;", "–", text)
    text = re.sub(r"&laquo;", "«", text)
    text = re.sub(r"&raquo;", "»", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_title(html):
    m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
    return m.group(1).strip() if m else ""

def get_main_block(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else html

def extract_texts(html):
    main = get_main_block(html)
    texts = []
    # Заголовки и параграфы
    indent_map = {"h1": 0, "h2": 1, "h3": 2, "h4": 3, "p": 1}
    for tag in ["h1", "h2", "h3", "h4", "p"]:
        indent = "  " * indent_map.get(tag, 1)
        for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", main, re.DOTALL | re.IGNORECASE):
            t = strip_html(m.group(1))
            if t and t not in ("Фото", "Фото / Видео", "Слайдер", "Описание"):
                texts.append((indent, t))
    # Списки
    for m in re.finditer(r"<li[^>]*>(.*?)</li>", main, re.DOTALL | re.IGNORECASE):
        t = strip_html(m.group(1))
        if t and len(t) > 2:
            texts.append(("    • ", t))
    # summary в details (FAQ)
    for m in re.finditer(r"<summary[^>]*>(.*?)</summary>", main, re.DOTALL | re.IGNORECASE):
        t = strip_html(m.group(1))
        if t:
            texts.append(("  [FAQ] ", t))
    # Кнопки и ссылки в main (только с текстом)
    for m in re.finditer(r"<a[^>]+href=[^>]*>(.*?)</a>", main, re.DOTALL | re.IGNORECASE):
        t = strip_html(m.group(1))
        if t and len(t) > 1 and t not in ("→", "←", "Подробнее →", "Смотреть портфолио", "Смотреть все кейсы"):
            if not re.match(r"^[\s←→]+$", t):
                texts.append(("  [ссылка] ", t))
    for m in re.finditer(r"<button[^>]*>(.*?)</button>", main, re.DOTALL | re.IGNORECASE):
        t = strip_html(m.group(1))
        if t:
            texts.append(("  [кнопка] ", t))
    return texts

def main():
    pages = []
    for root, dirs, files in os.walk(BASE):
        if "index.html" not in files:
            continue
        if "node_modules" in root or "__pycache__" in root or "scripts" in root:
            continue
        path = os.path.join(root, "index.html")
        rel = os.path.relpath(path, BASE)
        url = path_to_url(rel)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        title = get_title(html)
        texts = extract_texts(html)
        pages.append((url, title, texts))

    pages.sort(key=lambda x: (x[0].count("/"), x[0]))

    lines = []
    lines.append("# Тексты сайта и карта страниц")
    lines.append("")
    lines.append("## Карта сайта")
    lines.append("")
    for url, title, _ in pages:
        lines.append(f"- **{url}** — {title}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Тексты по страницам")
    lines.append("")

    for url, title, texts in pages:
        lines.append(f"### {url} — {title}")
        lines.append("")
        seen = set()
        for prefix, t in texts:
            if t in seen or not t.strip():
                continue
            seen.add(t)
            lines.append(prefix + t)
        lines.append("")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Готово: {OUT}")

if __name__ == "__main__":
    main()
