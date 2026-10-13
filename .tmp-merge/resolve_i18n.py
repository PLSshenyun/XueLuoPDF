"""Resolve the i18n catalogues: take upstream's catalogue, re-apply this fork's branding.

Every entry the fork added (its two own strings), removed (the ArtCraft rows) or renamed
(PdfCraft -> XueLuoPDF in the source key and the translation) is reproduced explicitly, so
nothing of upstream's 0.7.1 additions is lost and no ArtCraft row comes back.
"""
import io
import os
import subprocess

ROOT = r"D:\sakura\sakura_homework\XueLuoPDF"
I18N = os.path.join(ROOT, "crates", "ui-egui", "src", "i18n")

FORK_ADDED = {
    "Join the XueLuoPDF community": {
        "ar": "انضم إلى مجتمع XueLuoPDF", "bg": "Присъедини се към общността на XueLuoPDF",
        "cs": "Připojte se ke komunitě XueLuoPDF", "de": "Tritt der XueLuoPDF-Community bei",
        "el": "Γίνετε μέλος της κοινότητας XueLuoPDF", "es": "Únete a la comunidad de XueLuoPDF",
        "fr": "Rejoindre la communauté XueLuoPDF", "hu": "Csatlakozz a XueLuoPDF közösséghez",
        "it": "Unisciti alla community di XueLuoPDF", "ja": "XueLuoPDF コミュニティに参加",
        "kk": "XueLuoPDF қауымдастығына қосылыңыз", "pl": "Dołącz do społeczności XueLuoPDF",
        "pt-br": "Entrar na comunidade XueLuoPDF", "ru": "Присоединяйтесь к сообществу XueLuoPDF",
        "sl": "Pridružite se skupnosti XueLuoPDF", "te": "XueLuoPDF కమ్యూనిటీలో చేరండి",
        "tr": "XueLuoPDF topluluğuna katılın", "uk": "Приєднайтеся до спільноти XueLuoPDF",
        "zh-hans": "加入 XueLuoPDF 社区", "zh-hant": "加入 XueLuoPDF 社群",
        # 0.7.1 added Lithuanian; these two rows are this fork's own.
        "lt": "Prisijunkite prie „XueLuoPDF“ bendruomenės",
    },
    "XueLuoPDF icon": {
        "ar": "أيقونة XueLuoPDF", "bg": "Икона на XueLuoPDF", "cs": "Ikona XueLuoPDF",
        "de": "XueLuoPDF-Symbol", "el": "Εικονίδιο XueLuoPDF", "es": "Icono de XueLuoPDF",
        "fr": "Icône XueLuoPDF", "hu": "XueLuoPDF ikon", "it": "Icona di XueLuoPDF",
        "ja": "XueLuoPDF のアイコン", "kk": "XueLuoPDF белгішесі", "pl": "Ikona XueLuoPDF",
        "pt-br": "Ícone do XueLuoPDF", "ru": "Значок XueLuoPDF", "sl": "Ikona XueLuoPDF",
        "te": "XueLuoPDF చిహ్నం", "tr": "XueLuoPDF simgesi", "uk": "Піктограма XueLuoPDF",
        "zh-hans": "XueLuoPDF 图标", "zh-hant": "XueLuoPDF 圖示",
        # 0.7.1 added Lithuanian; these two rows are this fork's own.
        "lt": "XueLuoPDF piktograma",
    },
}
FORK_REMOVED = {
    "Join the ArtCraft community", "Join the ArtCraft Discord", "ArtCraft website",
    "Get help, share feedback and follow development on Discord.", "Part of",
}

codes = sorted(f[:-4] for f in os.listdir(I18N) if f.endswith(".tsv"))
report = []
for code in codes:
    rel = f"crates/ui-egui/src/i18n/{code}.tsv"
    blob = subprocess.run(["git", "show", f"MERGE_HEAD:{rel}"], cwd=ROOT, capture_output=True)
    if blob.returncode != 0:
        raise SystemExit(f"upstream has no {rel}")
    text = blob.stdout.decode("utf-8")
    if not text.endswith("\n"):
        text += "\n"
    lines = text[:-1].split("\n")

    kept, dropped, keys, last_row = [], 0, set(), None
    for line in lines:
        stripped = line.strip()
        if not stripped or line.startswith("#"):
            kept.append(line)
            continue
        cols = line.split("\t")
        if len(cols) != 3:
            kept.append(line)
            continue
        context, source, translation = cols
        if source in FORK_REMOVED:
            dropped += 1
            continue
        source = source.replace("PdfCraft", "XueLuoPDF")
        translation = translation.replace("PdfCraft", "XueLuoPDF")
        keys.add((context, source))
        kept.append("\t".join([context, source, translation]))
        last_row = len(kept) - 1
    added = []
    for key, table in FORK_ADDED.items():
        if ("", key) in keys:
            continue
        added.append(f"\t{key}\t{table[code]}")
    if last_row is None:
        raise SystemExit(f"{code}: the catalogue has no entries")
    kept[last_row + 1:last_row + 1] = added

    while kept and kept[-1] == "":
        kept.pop()
    with io.open(os.path.join(I18N, f"{code}.tsv"), "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(kept) + "\n")
    report.append((code, sum(1 for l in kept if l.startswith("\t")), dropped, len(added)))

for code, rows, dropped, added in report:
    print(f"{code:8s} rows={rows:5d}  artcraft-dropped={dropped}  fork-added={added}")
