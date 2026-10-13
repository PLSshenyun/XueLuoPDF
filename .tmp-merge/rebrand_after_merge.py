"""Re-apply the fork's branding to strings upstream's 0.7.1 brought back.

Each replacement is the exact upstream text; the fork's wording is the same text with its own
product name. Anything that is a `tl!` key is also updated in every catalogue, so the lookups
still resolve.
"""
import io
import os

ROOT = r"D:\sakura\sakura_homework\XueLuoPDF"

FILE_EDITS = {
    "apps/pdfcraft/src/decorations.rs": [
        ('"the Wayland compositor draws no window frames; PdfCraft draws its own title bar"',
         '"the Wayland compositor draws no window frames; XueLuoPDF draws its own title bar"'),
    ],
    "apps/pdfcraft/src/main.rs": [
        ('app.notify_tr("PdfCraft is drawing without a graphics processor, so it may be slow. Updating the graphics driver may help.");',
         'app.notify_tr("XueLuoPDF is drawing without a graphics processor, so it may be slow. Updating the graphics driver may help.");'),
    ],
    "crates/annot/src/lib.rs": [
        ('"PdfCraft can\'t redraw this comment: the standard fonts can\'t draw \\"{}\\" (U+{:04X}) in {what}, which would then show as ? (the comment was left as it is)"',
         '"XueLuoPDF can\'t redraw this comment: the standard fonts can\'t draw \\"{}\\" (U+{:04X}) in {what}, which would then show as ? (the comment was left as it is)"'),
    ],
    "crates/ui-egui/src/image_pick.rs": [
        ('"files PdfCraft didn\'t write are kept"', '"files this app didn\'t write are kept"'),
    ],
}

for rel, pairs in FILE_EDITS.items():
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    for old, new in pairs:
        if old not in text:
            print(f"!! not found in {rel}: {old[:70]!r}")
            continue
        text = text.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("branded", rel)

# Every `tl!` key that names the product must be renamed in the code and in the catalogues.
I18N = os.path.join(ROOT, "crates", "ui-egui", "src", "i18n")
codes = sorted(f[:-4] for f in os.listdir(I18N) if f.endswith(".tsv"))
substitutions = 0
for code in codes:
    path = os.path.join(I18N, f"{code}.tsv")
    with io.open(path, encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    changed = 0
    out = []
    for line in lines:
        if line.startswith("#") or line.count("\t") != 2:
            out.append(line)
            continue
        cols = line.split("\t")
        if "PdfCraft" in cols[1] or "PdfCraft" in cols[2]:
            cols[1] = cols[1].replace("PdfCraft", "XueLuoPDF")
            cols[2] = cols[2].replace("PdfCraft", "XueLuoPDF")
            changed += 1
        out.append("\t".join(cols))
    if changed:
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(out))
        substitutions += changed
        print(f"{code}: {changed} rows rebranded")
print("catalogue rows rewritten:", substitutions)

# The code side of those keys: any `tl!("...PdfCraft...")` or plain string the UI shows.
code_files = [
    "crates/ui-egui/src/i18n/mod.rs",
    "crates/ui-egui/src/content_ui.rs",
    "crates/ui-egui/src/canvas.rs",
    "crates/ui-egui/src/dialogs.rs",
    "crates/ui-egui/src/home.rs",
    "crates/ui-egui/src/updates.rs",
    "crates/ui-egui/src/ocr_ui.rs",
    "crates/ui-egui/src/sign_ui.rs",
    "crates/ui-egui/src/js_ui.rs",
    "crates/ui-egui/src/image_pick.rs",
]
for rel in code_files:
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        continue
    with io.open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    if "PdfCraft" not in text:
        continue
    before = text
    text = text.replace("PdfCraft", "XueLuoPDF")
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"rebranded {rel}: {before.count('PdfCraft')} occurrences")
