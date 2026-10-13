"""Resolve the remaining prose/code conflicts: CLI usage, js_ui, redact, create, README."""
import io
import os
import subprocess

ROOT = r"D:\sakura\sakura_homework\XueLuoPDF"


def git_show(rev_path):
    out = subprocess.run(["git", "show", rev_path], cwd=ROOT, capture_output=True)
    if out.returncode != 0:
        raise SystemExit(f"git show {rev_path} failed: {out.stderr.decode()}")
    return out.stdout.decode("utf-8")


def hunks(text):
    lines = text.splitlines()
    res, i = [], 0
    while i < len(lines):
        if lines[i].startswith("<<<<<<<"):
            j = i + 1
            mid = end = None
            while j < len(lines):
                if lines[j].startswith("=======") and mid is None:
                    mid = j
                elif lines[j].startswith(">>>>>>>"):
                    end = j
                    break
                j += 1
            res.append((i, mid, end))
            i = end + 1
        else:
            i += 1
    return res, lines


def resolve(path, replacements):
    full = os.path.join(ROOT, path)
    with io.open(full, encoding="utf-8", newline="") as f:
        text = f.read()
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"NOT FOUND in {path}: {old.splitlines()[0][:80]!r}")
        text = text.replace(old, new, 1)
    with io.open(full, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("resolved", path)


CLI_USAGE_OLD = """<<<<<<< HEAD
xueluopdf-cli combine <a.pdf> <b.pdf> … --out combined.pdf
xueluopdf-cli extract <in.pdf> --pages 1,3,5 --out out.pdf
xueluopdf-cli split   <in.pdf> (--every N | --before 3,7) [--out-dir DIR]
xueluopdf-cli check  <files or dirs…> [--timeout 20] [--dpi 36] [--json out.json]
xueluopdf-cli audit  <file.pdf> [--password PW]            find faux redactions (fails when found)
xueluopdf-cli tools                                       automation tools and their JSON Schemas
xueluopdf-cli run    <tool> [key=value …] [--root DIR] [--out image.png]
xueluopdf-cli run    --script steps.json [--root DIR]      [{\\"tool\\": \\"doc_open\\", \\"args\\": {…}}, …]
=======
                      (options run in order; page numbers refer to the document after the earlier options)
pdfcraft-cli combine <a.pdf> <b.pdf> … --out combined.pdf
pdfcraft-cli extract <in.pdf> --pages 1,3,5 --out out.pdf
pdfcraft-cli split   <in.pdf> (--every N | --before 3,7) [--out-dir DIR]
pdfcraft-cli check  <files or dirs…> [--timeout 20] [--dpi 36] [--json out.json]
pdfcraft-cli audit  <file.pdf> [--password PW]            find faux redactions (fails when found)
pdfcraft-cli batch <files or dirs...> --steps convert,ocr,optimize --out-dir DIR
                      [--recursive] [--root DIR] [--stop-on-error]
                      [--ppi 150] [--quality 60] [--dpi 300] [--language en] [--ocr-all-pages]
pdfcraft-cli tools                                       automation tools and their JSON Schemas
pdfcraft-cli run    <tool> [key=value …] [--root DIR] [--out image.png]
pdfcraft-cli run    --script steps.json [--root DIR]      [{\\"tool\\": \\"doc_open\\", \\"args\\": {…}}, …]
>>>>>>> main"""

CLI_USAGE_NEW = """                      (options run in order; page numbers refer to the document after the earlier options)
xueluopdf-cli combine <a.pdf> <b.pdf> … --out combined.pdf
xueluopdf-cli extract <in.pdf> --pages 1,3,5 --out out.pdf
xueluopdf-cli split   <in.pdf> (--every N | --before 3,7) [--out-dir DIR]
xueluopdf-cli check  <files or dirs…> [--timeout 20] [--dpi 36] [--json out.json]
xueluopdf-cli audit  <file.pdf> [--password PW]            find faux redactions (fails when found)
xueluopdf-cli batch <files or dirs...> --steps convert,ocr,optimize --out-dir DIR
                      [--recursive] [--root DIR] [--stop-on-error]
                      [--ppi 150] [--quality 60] [--dpi 300] [--language en] [--ocr-all-pages]
xueluopdf-cli tools                                       automation tools and their JSON Schemas
xueluopdf-cli run    <tool> [key=value …] [--root DIR] [--out image.png]
xueluopdf-cli run    --script steps.json [--root DIR]      [{\\"tool\\": \\"doc_open\\", \\"args\\": {…}}, …]"""

resolve("apps/pdfcraft-cli/src/main.rs", [
    (CLI_USAGE_OLD, CLI_USAGE_NEW),
    ("""<<<<<<< HEAD
    stdout_line(format_args!("xueluopdf-cli {}", env!("CARGO_PKG_VERSION")))?;
=======
    stdout_line(format_args!("pdfcraft-cli {}", pdfcraft_engine::build_info::version()))?;
    stdout_line(format_args!("Discord: {}  (help and feedback)", pdfcraft_engine::links::DISCORD))?;
>>>>>>> main""",
     """    stdout_line(format_args!("xueluopdf-cli {}", pdfcraft_engine::build_info::version()))?;"""),
])

resolve("crates/ui-egui/src/js_ui.rs", [
    ("""<<<<<<< HEAD
impl XueLuoPDFApp {
=======
/// What the user is told when a form's scripts were turned off: in a toast as it happens, then
/// on the notice bar for as long as the document is open.
pub(crate) fn scripts_off_notice() -> String {
    tl!("This form's scripts are turned off because one ran too long. Reopen the document to run them again.").to_string()
}

impl PdfCraftApp {
>>>>>>> main""",
     """/// What the user is told when a form's scripts were turned off: in a toast as it happens, then
/// on the notice bar for as long as the document is open.
pub(crate) fn scripts_off_notice() -> String {
    tl!("This form's scripts are turned off because one ran too long. Reopen the document to run them again.").to_string()
}

impl XueLuoPDFApp {"""),
])

resolve("crates/redact/src/lib.rs", [
    ("""<<<<<<< HEAD
    #[error("page {0} has vertical-writing text under a redaction mark, which XueLuoPDF cannot remove yet, so nothing was changed")]
=======
    #[error(
        "page {0} has vertical-writing text while a redaction mark is pending, and PdfCraft cannot tell whether that text lies under the mark yet, so nothing was changed"
    )]
>>>>>>> main""",
     """    #[error(
        "page {0} has vertical-writing text while a redaction mark is pending, and XueLuoPDF cannot tell whether that text lies under the mark yet, so nothing was changed"
    )]"""),
])

resolve("crates/create/src/extract.rs", [
    ("""<<<<<<< HEAD
//! transparency, are decoded and written as PNG with their soft mask, stencil mask or colour
//! key as alpha. Images XueLuoPDF can't decode yet (JPEG 2000, JBIG2, CCITT, separations) are
=======
//! transparency or with CMYK samples a viewer would read inverted, are decoded and written as PNG with their soft mask, stencil mask or colour
//! key as alpha. Images PdfCraft can't decode yet (JPEG 2000, JBIG2, CCITT, separations) are
>>>>>>> main""",
     """//! transparency or with CMYK samples a viewer would read inverted, are decoded and written as
//! PNG with their soft mask, stencil mask or colour key as alpha. Images XueLuoPDF can't decode
//! yet (JPEG 2000, JBIG2, CCITT, separations) are"""),
])

# README: the fork's Chinese rewrite wins over upstream's English text.
path = os.path.join(ROOT, "README.md")
with io.open(path, encoding="utf-8", newline="") as f:
    merged = f.read()
hs, lines = hunks(merged)
mine = git_show("HEAD:README.md").splitlines()
kept = None
for start, mid, end in hs:
    head = lines[start + 1:mid]
    # The HEAD side of the README conflict is a contiguous slice of my version.
    for i in range(len(mine) - len(head) + 1):
        if mine[i:i + len(head)] == head:
            kept = mine[i:i + len(head)]
            break
    if kept is None:
        raise SystemExit("could not locate the README HEAD side in HEAD:README.md")
    lines = lines[:start] + kept + lines[end + 1:]
with io.open(path, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines) + "\n")
print("resolved README.md (kept the fork's Chinese text)")
