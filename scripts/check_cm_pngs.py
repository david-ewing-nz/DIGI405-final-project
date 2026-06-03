from pathlib import Path
import sys

import numpy as np
from PIL import Image


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_cm_pngs.py <figs_dir>")
        return 2

    figs_dir = Path(sys.argv[1]).resolve()
    if not figs_dir.exists():
        print(f"Error: {figs_dir} not found")
        return 2

    rows = []
    for png in sorted(figs_dir.glob("cm_run*.png")):
        arr = np.array(Image.open(png).convert("L"), dtype=np.uint8)
        white_ratio = float((arr >= 250).mean())
        std = float(arr.std())
        rows.append((png.name, white_ratio, std, int(arr.min()), int(arr.max()), png.stat().st_size))

    blank = [r for r in rows if r[1] > 0.995 and r[2] < 2]
    nonblank = [r for r in rows if r not in blank]

    print(f"dir={figs_dir}")
    print(f"total={len(rows)} blank={len(blank)} nonblank={len(nonblank)}")

    if nonblank:
        print("sample nonblank:")
        for r in nonblank[:8]:
            print(
                f"{r[0]} | white={r[1]:.4f} std={r[2]:.2f} "
                f"min={r[3]} max={r[4]} bytes={r[5]:,}"
            )

    if blank:
        print("blank files:")
        for r in blank:
            print(r[0])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
