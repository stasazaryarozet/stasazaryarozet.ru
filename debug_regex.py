import re

text = "Всю сумму получит Художница,\nуставшая от многолетней административной и лекционной работой."

def process(val):
    for _ in range(2):
        val = re.sub(r'\b([а-яА-Яa-zA-Z]{1,5}) +', lambda m: m.group(1) + '\u00A0', val)
    return val

result = process(text)
print(f"Original: {text!r}")
print(f"Result:   {result!r}")
print(f"Has NBSP: {'\u00a0' in result}")

matches = re.findall(r'\b([а-яА-Яa-zA-Z]{1,5}) +', text)
print(f"Matches found: {matches}")
