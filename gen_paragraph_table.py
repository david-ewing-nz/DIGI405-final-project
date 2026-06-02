import re, os

with open('report/20260528C-DIGI405-Assignment-David-Ewing-82171165-draft.tex', encoding='utf-8') as f:
    raw = f.read()

# Start from \maketitle
body_match = re.search(r'\\maketitle', raw)
text = raw[body_match.end():] if body_match else raw

# Remove comments
text = re.sub(r'%.*', '', text)
# Remove math environments
text = re.sub(r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}', '[formula]', text, flags=re.DOTALL)
text = re.sub(r'\$[^$]+\$', '[formula]', text)

# Mark section/subsection headings
text = re.sub(r'\\(?:sub)*section\*?\{([^}]*)\}(?:\{[^}]*\})?', r'\n\n<<<SECTION:\1>>>\n\n', text)

# Preserve text from common commands
for cmd in ['textbf', 'emph', 'textit', 'text']:
    text = re.sub(r'\\' + cmd + r'\{([^}]*)\}', r'\1', text)
text = re.sub(r'\\parencite\{[^}]*\}', '', text)
text = re.sub(r'\\textcite\{[^}]*\}', '', text)
text = re.sub(r'\\cite\{[^}]*\}', '', text)
text = re.sub(r'\\ref\{[^}]*\}', '[ref]', text)
text = re.sub(r'\\label\{[^}]*\}', '', text)
text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*', ' ', text)
text = re.sub(r'[{}\\]', ' ', text)

# Split into blocks by double newline
blocks = re.split(r'\n{2,}', text)

# entries: ('section', title) or ('para', text, section_title_or_None)
entries = []
current_section = None

for block in blocks:
    block = block.strip()
    if not block:
        continue

    m = re.match(r'<<<SECTION:(.+?)>>>', block)
    if m:
        current_section = re.sub(r'\s+', ' ', m.group(1).strip())
        continue

    block = re.sub(r'\s+', ' ', block).strip()
    if len(block) < 20:
        continue

    entries.append(('para', block, current_section))
    current_section = None  # only attach to first para of each section


# --- AI signal analysis ---

DELETE_ON_SIGHT = [
    r'it is worth noting that',
    r'it is clear that',
    r'it can be seen that',
    r'as expected',
    r'\bnotably\b',
    r'\binterestingly\b',
    r'\bimportantly\b',
    r'it should be noted that',
    r'this confirms that',
    r'as demonstrated above',
    r'as will be shown',
]

def analyse(para):
    signals = []
    lo = para.lower()

    # Delete-on-sight phrases
    for pat in DELETE_ON_SIGHT:
        if re.search(pat, lo):
            phrase = pat.replace(r'\b', '').replace('\\b', '')
            signals.append(f'Delete-on-sight: \\textit{{{phrase}}}')

    # Passive constructions: is/are/was/were/be + past participle
    passives = re.findall(
        r'\b(?:is|are|was|were|be|been|being)\s+\w+ed\b', lo)
    if passives:
        examples = ', '.join(dict.fromkeys(passives[:3]))
        signals.append(f'Passive ({examples}) --- agent suppressed')

    # Tripartite lists: X, Y, and Z
    triparts = re.findall(r'[\w\s]+,\s[\w\s]+,\s(?:and|or)\s[\w\s]+', lo)
    if triparts:
        signals.append('Tripartite parallel list --- AI defaults to exactly three items')

    # Modal hedging: count distinct modals
    modals = re.findall(r'\b(may|might|could|would|should)\b', lo)
    if len(modals) >= 2:
        signals.append(f'Modal hedging ({len(modals)} modals) --- uniform uncertainty distribution')

    # Delete-on-sight hedge words used as hedges
    for phrase in ['consistent with', 'appropriate', 'it is important']:
        if phrase in lo:
            signals.append(f'\\textit{{{phrase}}} --- AI preferred hedge')

    # Prolepsis: present tense results in what sounds like intro/methods
    prolepsis_verbs = re.findall(
        r'\b(?:correctly|successfully|effectively|accurately)\s+\w+s\b', lo)
    if prolepsis_verbs:
        signals.append('Prolepsis --- result narrated as foregone conclusion')

    # Long sentences (split by . ! ?)
    sentences = [s.strip() for s in re.split(r'[.!?]', para) if len(s.strip()) > 10]
    long_sents = [s for s in sentences if len(s.split()) > 35]
    if long_sents:
        wc = max(len(s.split()) for s in long_sents)
        signals.append(f'Long sentence ({wc}w) --- dense uniform packing')

    # First-person absence check (flag only if multiple sentences and no I/my/mine)
    if len(sentences) >= 3 and not re.search(r'\b[Ii]\b|\bmy\b|\bmine\b', para):
        signals.append('No first-person --- absence of I/my')

    return signals


def escape(s):
    s = s.replace('&', r'\&')
    s = s.replace('#', r'\#')
    s = s.replace('_', r'\_')
    s = s.replace('^', r'\^{}')
    s = s.replace('~', r'\~{}')
    s = s.replace('[formula]', r'\textit{[formula]}')
    return s


out = []
out.append(r'\documentclass[11pt]{article}')
out.append(r'')
out.append(r'\usepackage{fontspec}')
out.append(r'\setmainfont{Georgia}')
out.append(r'\usepackage[a4paper, landscape, margin=2cm]{geometry}')
out.append(r'\usepackage{enumitem}')
out.append(r'\usepackage{longtable}')
out.append(r'\usepackage{array}')
out.append(r'\setlength{\extrarowheight}{2pt}')
out.append(r'\setlength{\parindent}{0pt}')
out.append(r'')
out.append(r'\title{AI Analysis of Draft Report --- Paragraph View}')
out.append(r'\author{David Ewing (82171165)}')
out.append(r'\date{1 June 2026}')
out.append(r'')
out.append(r'\begin{document}')
out.append(r'\maketitle')
out.append(r'\thispagestyle{empty}')
out.append(r'\newpage')
out.append(r'')
out.append(r'\setlength{\LTleft}{0pt}')
out.append(r'\setlength{\LTright}{0pt}')
out.append(r'\begin{longtable}{|p{0.55\linewidth}|p{0.40\linewidth}|}')
out.append(r'\hline')
out.append(r'\centering\textbf{PARAGRAPHS} & \centering\textbf{ANALYSIS} \tabularnewline[2pt]')
out.append(r'\hline')
out.append(r'\endhead')

for kind, para, section in entries:
    # Left cell: bold section title on its own line, then paragraph
    if section:
        left = r'\textbf{' + escape(section) + r'}\\[4pt]' + '\n' + escape(para)
    else:
        left = escape(para)

    # Right cell: bullet list of signals, or blank
    signals = analyse(para)
    if signals:
        items = '\n'.join(r'  \item ' + s for s in signals)
        right = ('\\begin{itemize}[leftmargin=1em,itemsep=1pt,topsep=1pt,parsep=0pt]\n'
                 + items + '\n'
                 + r'\end{itemize}')
    else:
        right = ''

    out.append(left + ' & ' + right + r' \\[2pt]')
    out.append(r'\hline')
    out.append(r'\rule[-3.5cm]{0pt}{3.5cm} & \\')
    out.append(r'\hline')

out.append(r'\end{longtable}')
out.append(r'\end{document}')

outpath = 'ai.analysis/20260601D-ANALYSIS-OF-DRAFT-REPORT.tex'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

paras = entries
print(f'{len(paras)} paragraphs -> {outpath}')
print(f'First left: {paras[0][1][:80]}')
print(f'First section: {paras[0][2]}')
