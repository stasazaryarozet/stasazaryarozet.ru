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
    # Varied rose silhouettes for a more natural look
    ROSE_PATHS = [
        "M14.5 4c0 0 .4-1.6-1-2-1.1-.3-2.3.2-2.8 1.2C10.3 2.2 9 1.7 7.9 2c-1.4.4-1 2-1 2s-1.8-.3-2.1 1.1c-.3 1 .5 1.9 1.4 2.2-.3.9-1.2 1.3-1 2.5.3 1.6 2.2 2.2 2.2 2.2s-1.2 2.5.7 4.3c1.7 1.7 4.3.7 4.3.7s.8 4.1 2.6 3.7c1.4-.3 1.3-2.5 1.3-2.5s2.5 1.2 4.3-.7c1.7-1.7.7-4.3.7-4.3s4.1-.8 3.7-2.6c-.3-1.4-2.5-1.3-2.5-1.3s1.2-2.5-.7-4.3C20.4 3.3 17.8 4.3 17.8 4.3s-.8-4.1-2.6-3.7C13.8.9 13.9 3.1 13.9 3.1S14.5 4 14.5 4zM12 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z", # Blooming
        "M12 2C8.7 2 6 4.7 6 8a5.5 5.5 0 0 0 1.5 3.7c.3.3.6.5.9.8.4.4.8.9 1.1 1.5a15 15 0 0 1 1 4v5a1 1 0 0 0 2 0v-5c0-1.4.3-2.8.9-4.1.3-.6.7-1.1 1.1-1.5.3-.3.6-.5.9-.8A5.5 5.5 0 0 0 18 8c0-3.3-2.7-6-6-6zm0 2a4 4 0 0 1 4 4c0 1-.3 1.9-.9 2.6l-1 .8c-.4.4-.8 1-1.2 1.6l-.3.6a13 13 0 0 0-.6 2.4l-.1.4a13 13 0 0 0-.6-2.4l-.3-.6a8 8 0 0 0-1.2-1.6l-1-.8A4 4 0 0 1 8 8a4 4 0 0 1 4-4z", # Bud
        "M12 2c0 0-2 1.5-2 3.5 0 2 2 3.5 2 3.5s2-1.5 2-3.5C14 3.5 12 2 12 2zm0 8c-3 0-5.5 2-5.5 5 0 2.5 2.5 4.5 5.5 4.5s5.5-2 5.5-4.5c0-1.5-2.5-5-5.5-5zm-1 6.5c-2 0-3.5-1-3.5-2s1.5-2 3.5-2 3.5 1 3.5 2-1.5 2-3.5 2z" # Tilted
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
