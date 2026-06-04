# DIGI405-final-project

This submission is intended to be distributed as a zip archive.

## How to unpack and run

Extract the archive and keep the top-level folder `FINAL-PROJECT/` intact.

The notebook should remain inside `FINAL-PROJECT/python/*.ipynb`.
Do not move the notebook file to another directory before opening it.

For one-line execution after extraction, run:

```bash
python run_submission.py
```

This launcher executes the notebook in place by calling Jupyter `nbconvert` for you.

The notebook uses relative paths and expects enough headroom inside `FINAL-PROJECT/` to create and use sibling folders such as:

- `data/`
- `figs/`
- `results/`
- `report/`

If the folder structure is preserved, the user should not need to be given any additional path instructions.

After the first run has created the working folders, the notebook can also be run manually in the usual way, provided it remains inside the same `FINAL-PROJECT/python/` location.

## Expected structure

```text
README.md
run_submission.py
FINAL-PROJECT/
	python/
		*.ipynb
```

## Notes

- Keep the extracted folder structure unchanged.
- `python run_submission.py` is the intended one-line execution path.
- After the first run has created the working folders, the notebook can also be run manually in the usual way, provided it remains inside the same `FINAL-PROJECT/python/` location.
- The report repeats these same setup instructions so the package can be used without separate guidance.
