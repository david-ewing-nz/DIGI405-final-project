# DIGI405 Final Project

Course: DIGI405 Digital Text Analysis, University of Canterbury, 2026 S1  
Repo: https://github.com/david-ewing-nz/DIGI405-final-project  
Purpose: Clean, shareable version of the Assignment 2 final submission — no course materials, drafts, or reference clutter.

Shared rules (British English, agent compliance, AI detection, humanising, LaTeX FLD, PDF workflow, machine info) are in `d:\github\CLAUDE.md`.

---

## Assignment 2 Summary

Topic: Machine-generated text detection using stylometric features (sentence length CV, lexical signals).  
Submission: 2000-word report (.tex → PDF) + Jupyter notebook (.ipynb).  
Grade weighting: 35% of DIGI405.

---

## Environment

- Python: `D:\Python` (system install, no venv)
- LaTeX: XeLaTeX via MiKTeX at `D:\MiKTeX`
- GitHub: https://github.com/david-ewing-nz/DIGI405-final-project

---

## Folder Structure

```
report/      — .tex source and refs.bib
figs/        — figures referenced in the report
data/        — data files used by the notebook
results/
  pdf/       — compiled PDFs
  html/      — HTML versions (preferred for Claude to read)
archive/     — timestamped compile archives
scripts/     — utility scripts (not committed)
```

---

## Key Files

- Report source: `report/20260528A-DIGI405-Assignment-2-David-Ewing-82171165-draft.tex`
- Compiled PDF: `results/pdf/20260528C-DIGI405-Assignment-David-Ewing-82171165-draft.pdf`
- Notebook: `20260528G-DIGI405-David-Ewing-82171165.ipynb`
- Bibliography: `report/refs.bib`

---

## Compile

```
D:\Python\python.exe scripts/archive_tex.py report/<file>.tex
```

Read compiled reports via `results/html/<name>.html` — preferred over PDF for Claude.

---

## Key Rules

- Do not commit/push without explicit instruction
- `scripts/` is not committed (in .gitignore)
- Only the latest version of each file belongs here — no date-stamped drafts
- This repo is intended to be shared; keep it clean
