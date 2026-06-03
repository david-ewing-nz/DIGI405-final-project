"""
archive_tex.py - Archive compiler for LaTeX documents.

Usage (from project root):
    python scripts/archive_tex.py report/myfile.tex
    python scripts/archive_tex.py results/pdf/myfile.pdf
    python scripts/archive_tex.py results/html/myfile.html

When given a .pdf or .html, the source .tex is resolved via the PDF Subject metadata field.

Steps:
    1. Creates archive/<YYYYMMDDHHMMSS>/tex/
    2. Copies .tex file; rewrites relative references to absolute paths
    3. Compiles with xelatex (pass 1), Biber (if .bcf present), xelatex (pass 2), xelatex (pass 3)
    4. Generates HTML via pandoc
    5. Copies PDF -> results/pdf/ and HTML -> results/html/
"""

import sys
import re
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

MIKTEX_BIN = Path("D:/MiKTeX/miktex/bin/x64")

REF_PATTERNS = [
    (re.compile(r'(\\bibliography\{)([^}]+)(\})'),      ".bib"),
    (re.compile(r'(\\addbibresource\{)([^}]+)(\})'),    ".bib"),
    (re.compile(r'(\\input\{)([^}]+)(\})'),              ".tex"),
    (re.compile(r'(\\include\{)([^}]+)(\})'),            ".tex"),
    (re.compile(r'(\\verbatiminput\{)([^}]+)(\})'),      ""),
]


def rewrite_refs(tex_content, tex_dir, arch_tex_dir):
    """Copy referenced files to archive and rewrite paths to absolute."""
    for pattern, default_ext in REF_PATTERNS:
        def replacer(m, td=tex_dir, ad=arch_tex_dir, ext=default_ext):
            prefix, ref_val, suffix = m.group(1), m.group(2), m.group(3)
            refs = [r.strip() for r in ref_val.split(",")]
            new_refs = []
            for ref in refs:
                p = Path(ref)
                if not p.suffix:
                    p = p.with_suffix(ext)
                src = (td / p).resolve()
                if src.exists():
                    dest = ad / src.name
                    shutil.copy2(src, dest)
                    new_refs.append(str(dest).replace("\\", "/"))
                else:
                    new_refs.append(ref)
            return prefix + ", ".join(new_refs) + suffix
        tex_content = pattern.sub(replacer, tex_content)
    return tex_content


def resolve_tex_from_pdf(pdf_path, project_root):
    """Extract Subject metadata from a PDF and resolve to a .tex file in report/."""
    pdfinfo = MIKTEX_BIN / "pdfinfo.exe"
    result = subprocess.run(
        [str(pdfinfo), str(pdf_path)],
        capture_output=True, text=True
    )
    subject = None
    for line in result.stdout.splitlines():
        if line.startswith("Subject:"):
            subject = line.split(":", 1)[1].strip()
            break

    # \jobname wraps filenames with spaces in quotes: e.g. "my file".tex -> strip them
    if subject:
        import re as _re
        m = _re.match(r'^"(.+)"(\.\w+)$', subject)
        if m:
            subject = m.group(1) + m.group(2)

    if not subject or not subject.endswith(".tex"):
        print(
            f"Error: Cannot resolve source .tex file.\n"
            f"  PDF Subject field contains: {subject!r}\n"
            f"  To fix: add the following to your .tex preamble and recompile:\n"
            f"    \\hypersetup{{pdfsubject = {{\\jobname.tex}}}}"
        )
        sys.exit(1)

    tex_candidate = project_root / "report" / subject
    if not tex_candidate.exists():
        print(
            f"Error: Source .tex '{subject}' not found in report/.\n"
            f"  Expected: {tex_candidate}"
        )
        sys.exit(1)

    print(f"Resolved source .tex: {tex_candidate}")
    return tex_candidate


def run(cmd, cwd=None):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, cwd=cwd)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/archive_tex.py <path/to/file.tex>")
        sys.exit(1)

    project_root = Path(__file__).parent.parent.resolve()
    target       = (project_root / sys.argv[1]).resolve()

    if not target.exists():
        print(f"Error: {target} not found.")
        sys.exit(1)

    # Resolve .pdf or .html to source .tex via PDF metadata
    if target.suffix.lower() == ".html":
        pdf_candidate = project_root / "results" / "pdf" / (target.stem + ".pdf")
        if not pdf_candidate.exists():
            print(f"Error: no matching PDF found for '{target.name}' in results/pdf/")
            sys.exit(1)
        target = resolve_tex_from_pdf(pdf_candidate, project_root)
    elif target.suffix.lower() == ".pdf":
        target = resolve_tex_from_pdf(target, project_root)

    tex_dir  = target.parent
    tex_base = target.stem

    timestamp    = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_base = project_root / "archive" / timestamp
    arch_tex     = archive_base / "tex"
    arch_tex.mkdir(parents=True, exist_ok=True)

    results_pdf  = project_root / "results" / "pdf"
    results_html = project_root / "results" / "html"
    results_pdf.mkdir(parents=True, exist_ok=True)
    results_html.mkdir(parents=True, exist_ok=True)

    # Rewrite relative refs to absolute and copy referenced files into archive
    tex_content   = target.read_text(encoding="utf-8")
    tex_content   = rewrite_refs(tex_content, tex_dir, arch_tex)
    arch_tex_file = arch_tex / target.name
    arch_tex_file.write_text(tex_content, encoding="utf-8")
    print(f"Archived tex: {arch_tex_file}")

    # Ensure MiKTeX is on PATH
    miktex = str(MIKTEX_BIN)
    if miktex not in os.environ.get("PATH", ""):
        os.environ["PATH"] = miktex + os.pathsep + os.environ.get("PATH", "")

    xelatex_cmd = ["xelatex", "-interaction=nonstopmode", str(arch_tex_file)]

    print("\nPass 1 - xelatex...")
    run(xelatex_cmd, cwd=str(arch_tex))

    bcf = arch_tex / f"{tex_base}.bcf"
    has_biblatex = bcf.exists()
    has_natbib_bib = "\\bibliography{" in tex_content

    if has_biblatex:
        print("Running Biber...")
        run(["biber", tex_base], cwd=str(arch_tex))
        print("Pass 2 - xelatex (post-Biber)...")
        run(xelatex_cmd, cwd=str(arch_tex))
    elif has_natbib_bib:
        print("Running BibTeX...")
        run(["bibtex", tex_base], cwd=str(arch_tex))
        print("Pass 2 - xelatex (post-BibTeX)...")
        run(xelatex_cmd, cwd=str(arch_tex))

    print("Pass 3 - xelatex (final)...")
    run(xelatex_cmd, cwd=str(arch_tex))

    # Copy PDF to results
    pdf_out = arch_tex / f"{tex_base}.pdf"
    if pdf_out.exists():
        dest = results_pdf / pdf_out.name
        shutil.copy2(pdf_out, dest)
        print(f"\nPDF -> {dest}")

        source_pdf = tex_dir / pdf_out.name
        shutil.copy2(pdf_out, source_pdf)
        print(f"PDF -> {source_pdf}")
    else:
        print("\nWarning: no PDF produced - check compile log")

    # Generate HTML via pandoc
    html_out = arch_tex / f"{tex_base}.html"
    r = run(
        ["pandoc", str(arch_tex_file), "-o", str(html_out), "--standalone", "--mathjax"],
        cwd=str(arch_tex),
    )
    if r.returncode == 0 and html_out.exists():
        dest = results_html / html_out.name
        shutil.copy2(html_out, dest)
        print(f"HTML -> {dest}")
    else:
        print("Warning: pandoc did not produce HTML")

    print(f"\nArchive: {archive_base}")


if __name__ == "__main__":
    main()
