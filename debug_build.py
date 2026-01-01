import build
import re

text = "**РАБОТ [ОЛЬГИ](https://olgarozet.ru)**"
processed = build.parse_content.__closure__[0].cell_contents(text.split('\n')) # Accessing inner function is hard
# Instead, let's just copy the logic or import the function if it was top level. It's nested.

# Okay, let's just modify the build script to export process_val or move it out.
# Or better, just run a script that does the same regex.

test_regex = r'\[([^\]]+)\]\(([^)]+)\)'
replacement = r'<a href="\2" class="red-link">\1</a>'
result = re.sub(test_regex, replacement, text)
print(f"Test Regex Result: {result}")

# Now let's try to run the actual build script against a dummy content file
from pathlib import Path
dummy_md = Path("dummy.md")
dummy_md.write_text("## test\n" + text, encoding='utf-8')

# We need to monkeypath or just call the function if we can reach it.
# Since process_val is inside parse_content, we can't easily call it directly.
# But we can call parse_content.

data = build.parse_content(dummy_md)
print(f"Build Script Result: {data['test']}")
