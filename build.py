#!/usr/bin/env python3
"""
Build pegasus/index.html from content.md and template
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
CONTENT = BASE / 'content.md'
TEMPLATE = BASE / 'template.html'
OUTPUT = BASE / 'pegasus' / 'index.html'

def parse_content(md_path: Path) -> dict:
    """Parse key-value markdown into dict"""
    content = md_path.read_text(encoding='utf-8')
    data = {}
    # Expanded set of distinct botanical rose silhouettes
    ROSE_PATHS = [
        # 1. Antique Dense Bloom (Standard)
        "M14.5 4c0 0 .4-1.6-1-2-1.1-.3-2.3.2-2.8 1.2C10.3 2.2 9 1.7 7.9 2c-1.4.4-1 2-1 2s-1.8-.3-2.1 1.1c-.3 1 .5 1.9 1.4 2.2-.3.9-1.2 1.3-1 2.5.3 1.6 2.2 2.2 2.2 2.2s-1.2 2.5.7 4.3c1.7 1.7 4.3.7 4.3.7s.8 4.1 2.6 3.7c1.4-.3 1.3-2.5 1.3-2.5s2.5 1.2 4.3-.7c1.7-1.7.7-4.3.7-4.3s4.1-.8 3.7-2.6c-.3-1.4-2.5-1.3-2.5-1.3s1.2-2.5-.7-4.3C20.4 3.3 17.8 4.3 17.8 4.3s-.8-4.1-2.6-3.7C13.8.9 13.9 3.1 13.9 3.1S14.5 4 14.5 4zM12 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z",
        # 2. Side-view Rose Bud (Elegant)
        "M12 2C8 2 6 5 6 8s2.5 6 6 8.5V22h1v-5.5c3.5-2.5 6-5.5 6-8.5s-2-6-6-6zm-1 6.5C11 7 10 6 8 6s-2 1-2 3s2.5 3.5 5 4.5l-.5-.5c-.5-.5-.5-2-0.5-4.5z",
        # 3. Simple Wild Rose (Five petals)
        "M12 6.5c-1-2.5-4-3.5-6-2s-1.5 5 2 6c-3.5 1-4 4-2 6s5 1.5 6-2c1 3.5 4 4 6 2s1.5-5-2-6c3.5-1 4-4 2-6s-5-1.5-6 2zM12 10a2 2 0 110 4 2 2 0 010-4z",
        # 4. Tilted Blooming Rose
        "M12 2c0 0-2 1.5-2 3.5 0 2 2 3.5 2 3.5s2-1.5 2-3.5C14 3.5 12 2 12 2zm0 8c-3 0-5.5 2-5.5 5 0 2.5 2.5 4.5 5.5 4.5s5.5-2 5.5-4.5c0-1.5-2.5-5-5.5-5z",
        # 5. Rose with Leaf (Botanical)
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
        print("Creating from current index.html...")
        # Use current index.html as base, mark placeholders
        return
    
    data = parse_content(CONTENT)
    template = TEMPLATE.read_text(encoding='utf-8')
    
    # Replace placeholders
    for key, value in data.items():
        placeholder = f'{{{{ {key} }}}}'
        template = template.replace(placeholder, value)
    
    OUTPUT.write_text(template, encoding='utf-8')
    print(f"Built: {OUTPUT}")

if __name__ == '__main__':
    build()
