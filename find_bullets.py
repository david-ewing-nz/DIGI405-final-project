import re

with open('ai.analysis/20260601A-ANALYSIS-OF-DRAFT-REPORT.tex', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = line.rstrip('\n')
    if not line.endswith(r'\\[2pt]'):
        continue
    if ' & ' not in line:
        continue
    parts = line.rsplit(' & ', 1)
    s = parts[0]
    clean = re.sub(r'\\[a-zA-Z]+', ' ', s)
    clean = re.sub(r'[{}\[\]]', ' ', clean).strip()
    wc = len(clean.split())
    commas = clean.count(',')
    has_colon = ':' in clean
    has_dash = '---' in s
    multi_and = clean.lower().count(' and ') >= 2
    if wc > 22 and (commas >= 3 or has_colon or has_dash or multi_and):
        print(f'L{i+1} ({wc}w): {clean[:130]}')
        print()
