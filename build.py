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
        '<path d="M12 2C8.7 2 6 4.7 6 8a5.5 5.5 0 0 0 1.5 3.7c.3.3.6.5.9.8.4.4.8.9 1.1 1.5a15 15 0 0 1 1 4v5a1 1 0 0 0 2 0v-5c0-1.4.3-2.8.9-4.1.3-.6.7-1.1 1.1-1.5.3-.3.6-.5.9-.8A5.5 5.5 0 0 0 18 8c0-3.3-2.7-6-6-6zm0 2a4 4 0 0 1 4 4c0 1-.3 1.9-.9 2.6l-1 .8c-.4.4-.8 1-1.2 1.6l-.3.6a13 13 0 0 0-.6 2.4l-.1.4a13 13 0 0 0-.6-2.4l-.3-.6a8 8 0 0 0-1.2-1.6l-1-.8A4 4 0 0 1 8 8a4 4 0 0 1 4-4z"/>'
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
