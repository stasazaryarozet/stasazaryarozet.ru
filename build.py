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
    
    rose_vignette = (
        '<div class="vignette">'
        '<svg class="rose-icon" viewBox="0 0 24 24">'
        '<path d="M12,2c0,0-2,4-2,6c0,2.2,1.8,4,4,4s4-1.8,4-4C18,6,16,2,16,2s-0.5,3-2,3S12,2,12,2z '
        'M12,22v-9c0,0-5,0.5-5-4s5-4.5,5-4.5V2"/>'
        '</svg></div>'
    )

    for line in content.split('\n'):
        if line.startswith('## '):
            if current_key:
                val = '\n'.join(current_value).strip()
                # 1. Handle Markdown Links [text](url)
                val = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: inherit; text-decoration: underline;">\1</a>', val)
                # 2. Handle Markdown Bold **text**
                val = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', val)
                # 3. Handle Vignette Dividers ---
                val = val.replace('---', rose_vignette)
                # 4. Replace internal newlines with <br> for HTML
                data[current_key] = val.replace('\n', '<br>')
            current_key = line[3:].strip()
            current_value = []
        elif current_key:
            current_value.append(line)
    
    if current_key:
        val = '\n'.join(current_value).strip()
        val = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: inherit; text-decoration: underline;">\1</a>', val)
        val = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', val)
        val = val.replace('---', rose_vignette)
        data[current_key] = val.replace('\n', '<br>')
    
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
