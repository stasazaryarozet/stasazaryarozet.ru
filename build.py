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
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_key:
                val = '\n'.join(current_value).strip()
                # Replace internal newlines with <br> for HTML
                data[current_key] = val.replace('\n', '<br>')
            current_key = line[3:].strip()
            current_value = []
        elif current_key:
            current_value.append(line)
    
    if current_key:
        val = '\n'.join(current_value).strip()
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
