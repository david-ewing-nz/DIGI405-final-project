from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

NOTEBOOK_NAME = "David-Ewing-82171165.ipynb"
PROJECT_DIR = Path("FINAL-PROJECT")
NOTEBOOK_PATH = PROJECT_DIR / "python" / NOTEBOOK_NAME
OUTPUT_NAME = "20260604E-executed.ipynb"


def main() -> int:
    if not NOTEBOOK_PATH.exists():
        print(f"ERROR: Notebook not found at {NOTEBOOK_PATH}")
        print("Run this script from the extracted package root.")
        return 1

    if shutil.which("jupyter") is None:
        print("ERROR: 'jupyter' was not found on PATH.")
        print("Install Jupyter Notebook or JupyterLab, then try again.")
        return 1

    command = [
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        str(NOTEBOOK_PATH),
        "--output",
        OUTPUT_NAME,
    ]

    print("Executing notebook with:")
    print(" ".join(command))

    completed = subprocess.run(command)
    if completed.returncode != 0:
        print("ERROR: Notebook execution failed.")
        return completed.returncode

    output_path = NOTEBOOK_PATH.with_name(OUTPUT_NAME)
    print(f"OK: Executed notebook written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
