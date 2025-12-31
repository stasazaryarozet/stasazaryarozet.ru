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
    current_key = None
    current_value = []
    
    rose_svg = (
        '<svg class="rose-icon" viewBox="0 0 24 24" fill="currentColor">'
        '<path d="M14.5 4c0 0 .4-1.6-1-2-1.1-.3-2.3.2-2.8 1.2C10.3 2.2 9 1.7 7.9 2c-1.4.4-1 2-1 2s-1.8-.3-2.1 1.1c-.3 1 .5 1.9 1.4 2.2-.3.9-1.2 1.3-1 2.5.3 1.6 2.2 2.2 2.2 2.2s-1.2 2.5.7 4.3c1.7 1.7 4.3.7 4.3.7s.8 4.1 2.6 3.7c1.4-.3 1.3-2.5 1.3-2.5s2.5 1.2 4.3-.7c1.7-1.7.7-4.3.7-4.3s4.1-.8 3.7-2.6c-.3-1.4-2.5-1.3-2.5-1.3s1.2-2.5-.7-4.3C20.4 3.3 17.8 4.3 17.8 4.3s-.8-4.1-2.6-3.7C13.8.9 13.9 3.1 13.9 3.1S14.5 4 14.5 4zM12 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>'
        '</svg>'
    )
    
    rose_vignette = f'<div class="vignette">{rose_svg}</div>'
    rose_clean = f'<div class="vignette no-lines">{rose_svg}</div>'

    def process_val(lines):
        val = '\n'.join(lines).strip('\n') # Strip only trailing/leading newlines, not spaces
        # 1. Handle Markdown Links [text](url)
        val = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: inherit; text-decoration: underline; text-decoration-color: #ff0000; text-underline-offset: 5px;">\1</a>', val)
        # 2. Handle Markdown Bold **text**
        val = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', val)
        # 3. Handle Red Text ++text++
        val = re.sub(r'\+\+([^+]+)\+\+', r'<span style="color: #ff0000;">\1</span>', val)
        # 4. Handle Vignettes
        val = re.sub(r'\n?---\n?', rose_vignette, val)
        val = re.sub(r'\n?@@@\n?', rose_clean, val)
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
