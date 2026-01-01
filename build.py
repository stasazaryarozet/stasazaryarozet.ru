#!/usr/bin/env python3
"""
Build pegasus/index.html from content.md and template
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
CONTENT = BASE / 'content.md'
TEMPLATE = BASE / 'src' / 'template.html'
STYLES = BASE / 'src' / 'style.css'
OUTPUT = BASE / 'pegasus' / 'index.html'

def parse_content(md_path: Path) -> dict:
    """Parse key-value markdown into dict"""
    content = md_path.read_text(encoding='utf-8')
    data = {}
    # Expanded set of distinct botanical rose silhouettes
    ROSE_PATHS = [
        # 1. Antique Dense Bloom (Standard)
        "M14.5 4c0 0 .4-1.6-1-2-1.1-.3-2.3.2-2.8 1.2C10.3 2.2 9 1.7 7.9 2c-1.4.4-1 2-1 2s-1.8-.3-2.1 1.1c-.3 1 .5 1.9 1.4 2.2-.3.9-1.2 1.3-1 2.5.3 1.6 2.2 2.2 2.2 2.2s-1.2 2.5.7 4.3c1.7 1.7 4.3.7 4.3.7s.8 4.1 2.6 3.7c1.4-.3 1.3-2.5 1.3-2.5s2.5 1.2 4.3-.7c1.7-1.7.7-4.3.7-4.3s4.1-.8 3.7-2.6c-.3-1.4-2.5-1.3-2.5-1.3s1.2-2.5-.7-4.3C20.4 3.3 17.8 4.3 17.8 4.3s-.8-4.1-2.6-3.7C13.8.9 13.9 3.1 13.9 3.1S14.5 4 14.5 4zM12 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z",
        # 2. Detailed Multi-petal Bloom (New for 2)
        "M12 1.5c.9 0 1.7.5 2.2 1.3.5-.8 1.3-1.3 2.2-1.3 1.5 0 2.8 1.3 2.8 2.8 0 .5-.1 1-.4 1.5.8.1 1.5.6 1.9 1.3.4.7.4 1.5.1 2.1.8.4 1.3 1.2 1.3 2.1a2.8 2.8 0 0 1-2.8 2.8c-.5 0-1-.1-1.5-.4.1.8-.1 1.5-.6 2.1-.5.6-1.3.9-2.2.9-.9 0-1.7-.5-2.2-1.3-.5.8-1.3 1.3-2.2 1.3-1.5 0-2.8-1.3-2.8-2.8 0-.5.1-1 .4-1.5-.8-.1-1.5-.6-1.9-1.3a2.8 2.8 0 0 1-.1-4.2c.8-.4 1.3-1.2 1.3-2.1 0-1.5 1.3-2.8 2.8-2.8zm0 5.6a2.8 2.8 0 0 0-2.8 2.8c0 1.5 1.3 2.8 2.8 2.8s2.8-1.3 2.8-2.8-1.3-2.8-2.8-2.8z",
        # 3. Wild Open Rose (Simple/Natural)
        "M12 6.5c-1-2.5-4-3.5-6-2s-1.5 5 2 6c-3.5 1-4 4-2 6s5 1.5 6-2c1 3.5 4 4 6 2s1.5-5-2-6c3.5-1 4-4 2-6s-5-1.5-6 2zM12 10 a2 2 0 1 1 0 4 2 2 0 0 1 0-4z",
        # 4. Botanical Rose Bud (Explicit floral shape)
        "M12 3a4 4 0 0 1 4 4c0 2-2 5-4 8-2-3-4-6-4-8a4 4 0 0 1 4-4zm0 2c-1.1 0-2 .9-2 2 0 .8.5 1.8 1.2 2.8.5.6.8 1.2.8 2.2 0-1 .3-1.6.8-2.2.7-1 1.2-2 1.2-2.8 0-1.1-.9-2-2-2zM12 15v7h1v-7h-1z",
        # 5. Rose with Leaf (Traditional)
        "M13 2c-3 0-5 3-5 6 0 2 2 4 4 6 .5.4 1 .8 1.5 1.5s1 2 1 3.5v3h1v-3c0-2.5-.5-5-1.5-7-1-1.5-2-3-2-4 0-1.5 1-3 1-3zm-5 13c-3 0-6 1-6 4s3 3 6 3 6-3 6-3c-2 0-3-.5-4-1s-1.5-1.5-2-3z"
    ]

    rose_count = 0
    current_key = None
    current_value = []

    def get_rose_html(clean=False):
        nonlocal rose_count
        path = ROSE_PATHS[rose_count % len(ROSE_PATHS)]
        rose_count += 1
        klass = "vignette no-lines" if clean else "vignette"
        return f'<div class="{klass}"><svg class="rose-icon" viewBox="0 0 24 24" fill="currentColor"><path d="{path}"/></svg></div>'

    def process_val(lines):
        val = '\n'.join(lines).strip('\n') # Strip only trailing/leading newlines, not spaces
        # 1. Handle Markdown Links [text](url)
        val = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: inherit; text-decoration: underline; text-decoration-color: #ff0000; text-underline-offset: 5px;">\1</a>', val)
        # 2. Handle Markdown Bold **text**
        val = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', val)
        # 3. Handle Red Text ++text++
        val = re.sub(r'\+\+([^+]+)\+\+', r'<span style="color: #ff0000;">\1</span>', val)
        
        # 4. Handle Vignettes with rotation/variation
        while '---' in val or '@@@' in val:
            if '@@@' in val and (not '---' in val or val.find('@@@') < val.find('---')):
                val = val.replace('@@@', get_rose_html(clean=True), 1)
            else:
                val = val.replace('---', get_rose_html(clean=False), 1)

        # 5. Replace ALL newlines with <br> for HTML rendering
        return val.replace('\n', '<br>')

    for line in content.split('\n'):
        if line.startswith('## '):
            if current_key:
                data[current_key] = process_val(current_value)
            current_key = line[3:].strip()
            current_value = []
        elif current_key:
            current_value.append(line)
    
    if current_key:
        data[current_key] = process_val(current_value)
    
    return data

def build():
    if not TEMPLATE.exists():
        print(f"Template not found: {TEMPLATE}")
        return
    
    # 1. Parse Content
    data = parse_content(CONTENT)
    
    # 2. Load Template
    template = TEMPLATE.read_text(encoding='utf-8')
    
    # 3. Inject Styles (Architectural Assembly)
    if STYLES.exists():
        print(f"Injecting styles from {STYLES}...")
        styles_content = STYLES.read_text(encoding='utf-8')
        template = template.replace('/* STYLES_INJECTED_HERE */', styles_content)
    else:
        print(f"WARNING: Styles not found at {STYLES}")

    # 4. Inject Data
    for key, value in data.items():
        placeholder = f'{{{{ {key} }}}}'
        template = template.replace(placeholder, value)
    
    OUTPUT.write_text(template, encoding='utf-8')
    print(f"Built Masterpiece: {OUTPUT}")

if __name__ == '__main__':
    build()
