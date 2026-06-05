# DIGI405-final-project

This submission is distributed as a zip archive: `FINAL-PROJECT-SUBMISSION.zip`.

## Contents

```text
FINAL-PROJECT-SUBMISSION.zip
├── README.md
├── FINAL-PROJECT/
│   ├── python/
│   │   ├── David-Ewing-82171165.ipynb        (notebook, outputs cleared)
│   │   └── run_submission.py                 (one-line launcher)
│   └── REPORT/
│       ├── David-Ewing-82171165.pdf          (compiled report, 20 pages)
│       ├── David-Ewing-82171165.docx         (Word version of report)
│       └── David-Ewing-82171165.executed.html  (executed notebook as HTML)
```

## How to unpack and run

Extract the archive keeping the top-level folder `FINAL-PROJECT/` intact:

```bash
python -m zipfile -e FINAL-PROJECT-SUBMISSION.zip .
python FINAL-PROJECT/python/run_submission.py
```

The launcher executes the notebook in place using Jupyter `nbconvert`.

The notebook uses relative paths and creates sibling folders during execution (`data/`, `figs/`, `results/`). Keep the folder structure intact — do not move the notebook before running.

After the first run, the notebook can also be opened and run manually from inside `FINAL-PROJECT/python/`.

## Prerequisites

- Python 3
- Jupyter (`pip install notebook` or `pip install jupyterlab`)
- nbconvert (`pip install nbconvert`)
- Standard data science packages used in the notebook: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `nltk`, `gensim`

On JupyterHub these are already available — no installation needed.

## Notes

- Run the two commands above from the directory where you extracted the zip.
- The REPORT folder contains the written report in PDF and Word formats, and an HTML rendering of the executed notebook.
