"""Resolve ATTRIBUTION.toml (every hunk is a stale hash: take upstream's side) and then recompute
every entry's SHA-256 from the file on disk. ATTRIBUTION.md is generated afterwards by
`cargo xtask assets --write`.
"""
import hashlib
import io
import os
import re

ROOT = r"D:\sakura\sakura_homework\XueLuoPDF"
PATH = os.path.join(ROOT, "ATTRIBUTION.toml")


def resolve(text):
    lines = text.split("\n")
    out, i, taken, dropped = [], 0, 0, 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<<<<<<"):
            j = i + 1
            mid = end = None
            while j < len(lines):
                if lines[j].startswith("=======") and mid is None:
                    mid = j
                elif lines[j].startswith(">>>>>>>"):
                    end = j
                    break
                j += 1
            ours = lines[i + 1:mid]
            theirs = lines[mid + 1:end]
            # Every conflict here is one sha256 line against another: upstream's is the one that
            # describes the upstream file, and the fork's own entries have no counterpart.
            pick = theirs if theirs and theirs[0].startswith("sha256") else ours
            if pick is theirs:
                taken += 1
            else:
                dropped += 1
            out.extend(pick)
            i = end + 1
        else:
            out.append(line)
            i += 1
    return "\n".join(out), taken, dropped


with io.open(PATH, encoding="utf-8", newline="") as f:
    text = f.read()
text, taken, kept = resolve(text)
print(f"hunks: upstream={taken} fork={kept}")

blocks = text.split("[[asset]]")
fixed = missing = 0
for i, block in enumerate(blocks):
    m = re.search(r'path = "([^"]+)"', block)
    if not m:
        continue
    full = os.path.join(ROOT, m.group(1))
    if not os.path.isfile(full):
        missing += 1
        continue
    sha = hashlib.sha256(open(full, "rb").read()).hexdigest()
    new_block, n = re.subn(r'sha256 = "[0-9a-f]{64}"', f'sha256 = "{sha}"', block, count=1)
    if n and new_block != block:
        blocks[i] = new_block
        fixed += 1
text = "[[asset]]".join(blocks)

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print(f"recomputed hashes: {fixed}; entries whose file is absent: {missing}")
print("markers left:", text.count("\n<<<<<<< "))
