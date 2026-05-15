"""Build a candidates folder with short filenames.

Each JPG from tmp/raw is copied to tmp/candidates/cNNN.jpg with a manifest
written to tmp/candidates/manifest.tsv mapping short id -> original path
and (when available) the caption/source clue extracted from the original
filename.
"""
from pathlib import Path
import shutil
import re
import csv

BASE = Path(r"C:/Users/misst/fizzy-fix")
RAW = BASE / "tmp" / "raw"
OUT = BASE / "tmp" / "candidates"
OUT.mkdir(parents=True, exist_ok=True)


def caption_from_name(p: Path) -> str:
    """gallery-dl tiktok filenames embed the caption — extract it."""
    name = p.stem
    # tiktok format: '<id> <caption text> [<hash>]'
    m = re.match(r"^\d+(?:_\d+)?\s+(.*?)(?:\s+\[[^\]]+\])?$", name)
    if m:
        return m.group(1)[:140]
    return name[:140]


def main():
    jpgs = sorted([p for p in RAW.rglob("*.jpg")])
    rows = []
    for i, src in enumerate(jpgs, 1):
        short = f"c{i:03d}.jpg"
        dst = OUT / short
        if not dst.exists():
            try:
                # use \\?\ long-path prefix on Windows for unicode/long names
                src_str = "\\\\?\\" + str(src.resolve())
                with open(src_str, "rb") as fr, open(dst, "wb") as fw:
                    fw.write(fr.read())
            except Exception as e:
                print(f"  skip {src.name[:60]}: {e}")
                continue
        # source category — instagram folder name or 'tiktok'
        parts = src.parts
        if "instagram" in parts:
            ig_idx = parts.index("instagram")
            source = f"ig:{parts[ig_idx + 1]}" if ig_idx + 1 < len(parts) else "ig"
        elif "tiktok" in parts:
            source = "tiktok:fizzyfixaz"
        else:
            source = "?"
        cap = caption_from_name(src)
        rows.append((short, source, cap, str(src)))

    with open(OUT / "manifest.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["short", "source", "caption_or_clue", "original_path"])
        w.writerows(rows)

    # Also write a markdown digest grouped by source for human reading
    by_source = {}
    for r in rows:
        by_source.setdefault(r[1], []).append(r)
    with open(OUT / "manifest.md", "w", encoding="utf-8") as f:
        f.write("# Candidates manifest\n\n")
        for src, group in by_source.items():
            f.write(f"\n## {src} ({len(group)})\n\n")
            for r in group:
                f.write(f"- **{r[0]}** — {r[2]}\n")

    print(f"copied {len(rows)} files -> {OUT}")
    print(f"manifest: {OUT / 'manifest.md'}")


if __name__ == "__main__":
    main()
