#!/usr/bin/env python3
"""
Shim: delegate notebook/python archive runs to the shared runner in ../self.

Why this exists:
- Keeps one source of truth for archive_py logic.
- Avoids code drift from copying the full runner into each repo.

Usage (same as shared script):
    python scripts/archive_py.py <target.py|target.ipynb> [extra args...]

Optional override:
    Set ARCHIVE_PY_SHIM_TARGET to an absolute path for archive_py.py.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _resolve_shared_runner() -> Path:
    override = os.environ.get("ARCHIVE_PY_SHIM_TARGET", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.exists():
            return candidate

    here = Path(__file__).resolve()

    # Expected sibling layout: <root>/DIGI405-final-project and <root>/self
    sibling_candidate = here.parents[2] / "self" / "scripts" / "archive_py.py"
    if sibling_candidate.exists():
        return sibling_candidate

    # Fallback: same parent folder, useful in alternate layouts.
    alt_candidate = here.parents[1] / "archive_py_shared.py"
    if alt_candidate.exists():
        return alt_candidate

    raise FileNotFoundError(
        "Could not find shared archive_py.py. "
        "Expected ../self/scripts/archive_py.py relative to this repo, "
        "or set ARCHIVE_PY_SHIM_TARGET to the full path."
    )


def main() -> int:
    try:
        shared_runner = _resolve_shared_runner()
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2

    cmd = [sys.executable, str(shared_runner), *sys.argv[1:]]
    print(f"Delegating to shared runner: {shared_runner}")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
