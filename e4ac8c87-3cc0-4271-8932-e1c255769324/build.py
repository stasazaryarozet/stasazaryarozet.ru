#!/usr/bin/env python3
"""index.html = f(books.json) — чистый детерминированный проектор, stdlib-only.

Подача — из исследования эргономики веб-текста (Butterick «Practical Typography»:
кегль 15–25px / интерлиньяж 120–145% / строка 45–90 зн.; iA: постоянная мера через
брейкпоинты; WCAG 2.2: контраст ≥4.5:1, тап-цели ≥44px, тёмная #121212 не-чисто-чёрная).
Типографический nbsp-пасс — младший брат site_generator._load_typo_rules(ru) из контура
Dela; при фолде сайта в owner-пайплайн заменяется на те правила (данные переживают,
проектор одноразов).

Запуск: python3 build.py   (из каталога страницы; пишет ./index.html)
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
D = json.loads((HERE / "books.json").read_text(encoding="utf-8"))

NBSP = " "
_SHORT = r"(?:в|во|и|к|ко|с|со|о|об|у|а|но|на|не|ни|от|до|по|за|из|изо|над|под|при|для|без|же|бы|ли|или|как|что|его|её|их)"


def typo(s: str) -> str:
    """RU-микротипографика поверх УЖЕ экранированного текста: короткое слово + nbsp,
    число+единица, №№, диапазоны уже с en-dash в данных."""
    s = re.sub(rf"(^|[\s(«]){_SHORT} ", lambda m: m.group(0)[:-1] + NBSP, s, flags=re.IGNORECASE)
    s = re.sub(r"(\d) (лет|л\.|книг|задач)", rf"\1{NBSP}\2", s)
    s = s.replace("№№ ", f"№№{NBSP}").replace("№ ", f"№{NBSP}")
    s = re.sub(r" —", f"{NBSP}—", s)
    return s


def esc(s: str) -> str:
    return typo(html.escape(s, quote=False))


def book_li(b: dict) -> str:
    shops = "\n".join(
        f'          <a href="{html.escape(s["url"])}">{esc(s["name"])}</a>'
        for s in b["shops"])
    return f"""    <li class="bk">
      <div>
        <p class="t"><span class="au">{esc(b["author"])}.</span> «{esc(b["title"])}»<span class="age">{esc(b["age"])}</span></p>
        <p class="why">{esc(b["why"])}</p>
        <div class="shops">
{shops}
        </div>
      </div>
    </li>"""


CSS = """\
  /* Исследование → решения (Butterick: 4 столпа; iA: постоянная мера; WCAG 2.2):
     кегль 19–21px fluid · интерлиньяж 1.45 · мера 34em ≈ 66 зн. · серифный текст,
     системный санс для действий · контраст ≥4.5:1 · тёмная #121212 · тапы ≥44px */
  :root {
    --bg: #faf9f7; --ink: #1e1c1a; --muted: #6f6a63;
    --rule: #e4e0da; --chip-bg: #efece7; --chip-ink: #3d3a35; --accent: #8a4b12;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #121212; --ink: #e8e6e3; --muted: #a09a92;
      --rule: #2a2a2a; --chip-bg: #1f1f1f; --chip-ink: #cfcac3; --accent: #d99a5b;
    }
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    background: var(--bg); color: var(--ink);
    font: 400 clamp(1.1875rem, 1.05rem + 0.6vw, 1.3125rem)/1.45 Georgia, 'Times New Roman', serif;
    padding: clamp(1.25rem, 4vw, 3rem) 1.25rem 4rem;
  }
  main { max-width: 34em; margin: 0 auto; }
  header { margin-bottom: 2.5rem; }
  h1 {
    font-size: clamp(1.6rem, 1.3rem + 1.6vw, 2.1rem);
    line-height: 1.2; font-weight: 700; letter-spacing: -0.01em;
    text-wrap: balance;
  }
  .sub { color: var(--muted); margin-top: 0.6rem; font-style: italic; }
  .pole {
    font: 600 0.72em/1.3 system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    text-transform: uppercase; letter-spacing: 0.09em; color: var(--accent);
    margin: 1.8rem 0 0.9rem;
  }
  .pole--down { margin-top: 0.4rem; text-align: right; }
  ol { list-style: none; counter-reset: bk; }
  li.bk {
    counter-increment: bk;
    display: grid; grid-template-columns: 2.1rem 1fr; column-gap: 0.9rem;
    padding: 1.15rem 0; border-top: 1px solid var(--rule);
  }
  li.bk::before {
    content: counter(bk);
    /* w400: у Georgia нет 300 — синтетика была бы ложью; приглушение цветом */
    font: 400 1.5rem/1 Georgia, serif; color: var(--muted);
    padding-top: 0.15rem; text-align: right;
  }
  .t { font-weight: 700; }
  .t .au { font-weight: 400; }
  .age {
    font: 500 0.68em/1 system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    color: var(--muted); letter-spacing: 0.04em; white-space: nowrap;
    border: 1px solid var(--rule); border-radius: 99px; padding: 0.28em 0.6em;
    vertical-align: 0.25em; margin-left: 0.45em;
  }
  .why { margin-top: 0.35rem; }
  .shops { margin-top: 0.7rem; display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .shops a {
    font: 500 0.75em/1 system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    color: var(--chip-ink); background: var(--chip-bg);
    text-decoration: none; border-radius: 8px;
    display: inline-flex; align-items: center;
    min-height: 44px; padding: 0 1.1em;   /* WCAG/thumb: тап-цель ≥44px — явно, не следствием кегля */
    border: 1px solid var(--rule);
  }
  .shops a:hover, .shops a:focus-visible { border-color: var(--accent); color: var(--accent); }
  .note { margin-top: 2.2rem; padding-top: 1.1rem; border-top: 1px solid var(--rule); color: var(--muted); font-size: 0.88em; }
  footer { margin-top: 2.6rem; color: var(--muted); font-size: 0.78em;
           font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }
  @media print {
    .shops a { background: none; border: none; padding: 0; min-height: 0; text-decoration: underline; }
    body { padding: 0; }
  }"""

page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(D["title"])}</title>
<meta name="description" content="{html.escape(D["subtitle"])}">
<style>
{CSS}
</style>
</head>
<body>
<main>
  <header>
    <h1>{esc(D["title"])}</h1>
    <p class="sub">{esc(D["subtitle"])}</p>
  </header>

  <p class="pole">{esc(D["pole_top"])}</p>

  <ol>
{chr(10).join(book_li(b) for b in D["books"])}
  </ol>

  <p class="pole pole--down">{esc(D["pole_bottom"])}</p>

  <p class="note">{esc(D["note"])}</p>

  <footer>{esc(D["credit"])} · наличие проверено {esc(D["verified"])}</footer>
</main>
</body>
</html>
"""

(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"index.html: {len(page)} байт, книг: {len(D['books'])}")
