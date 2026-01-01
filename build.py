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
    # Expanded set of distinct, recognizable botanical rose silhouettes
    # Unambiguous Botanical Rose Silhouette
    ROSE_PATHS = [
        "M12 2C6.48 2 2 6.48 2 12c0 1.54.36 2.98.97 4.29L1 21l4.71-1.97C7.02 19.64 8.46 20 10 20c5.52 0 10-4.48 10-10S15.52 2 10 2zm0 16c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"
    ] * 5

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
