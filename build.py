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
        '<path d="M12 2c-1.5 0-2.5 1-2.5 2.5s1 2.5 2.5 3c1.5-.5 2.5-1.5 2.5-3S13.5 2 12 2zM9.5 8c-2 0-3.5 1.5-3.5 4s1.5 4.5 3.5 4.5c1 0 2-.5 2.5-1.5.5 1 1.5 1.5 2.5 1.5 2 0 3.5-1.5 3.5-4s-1.5-4-3.5-4c-1 0-2 .5-2.5 1.5C11.5 8.5 10.5 8 9.5 8zM12 17v5M12 19l-3 2M12 20l3 1"/>'
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
