"""Build /public/images/logo.png + mascot-cup.png + favicons from c031 (the
official Fizzy Fix wordmark + mascot lockup scraped from TikTok)."""
from pathlib import Path
from PIL import Image

BASE = Path(r"C:/Users/misst/fizzy-fix")
SRC = BASE / "tmp" / "candidates" / "c031.jpg"
OUT = BASE / "public" / "images"
OUT.mkdir(parents=True, exist_ok=True)


def key_cream(img: Image.Image) -> Image.Image:
    """Replace cream/off-white pixels with transparency."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # cream-ish: warm light, all channels high, slightly warm
            if r > 235 and g > 225 and b > 210 and abs(r - g) < 30 and abs(g - b) < 40:
                px[x, y] = (r, g, b, 0)
    return img


def trim(img: Image.Image, padding: int = 8) -> Image.Image:
    """Trim transparent border, leave a small pad."""
    bbox = img.getbbox()
    if bbox is None:
        return img
    l, t, r, b = bbox
    l = max(0, l - padding)
    t = max(0, t - padding)
    r = min(img.width, r + padding)
    b = min(img.height, b + padding)
    return img.crop((l, t, r, b))


def main():
    src = Image.open(SRC)
    print(f"loaded {SRC.name} {src.size}")

    # ---- Full lockup -> logo.png ----
    logo = key_cream(src.copy())
    logo = trim(logo, padding=12)
    # Cap longest side to 1200 for sharpness without bloat
    max_side = 1200
    lw, lh = logo.size
    if max(lw, lh) > max_side:
        scale = max_side / max(lw, lh)
        logo = logo.resize((int(lw * scale), int(lh * scale)), Image.LANCZOS)
    logo.save(OUT / "logo.png", "PNG", optimize=True)
    print(f"  wrote logo.png {logo.size}")

    # ---- Mascot only -> mascot-cup.png ----
    iw, ih = src.size
    # The walking soda-cup character occupies roughly columns 0.13..0.37, rows 0.50..0.96
    box = (int(0.13 * iw), int(0.50 * ih), int(0.37 * iw), int(0.96 * ih))
    mascot = src.crop(box)
    mascot = key_cream(mascot)
    mascot = trim(mascot, padding=4)
    mw, mh = mascot.size
    if mw > 400:
        scale = 400 / mw
        mascot = mascot.resize((400, int(mh * scale)), Image.LANCZOS)
    mascot.save(OUT / "mascot-cup.png", "PNG", optimize=True)
    print(f"  wrote mascot-cup.png {mascot.size}")

    # ---- Favicons ----
    favicon_src = logo  # already trimmed + transparent
    for size, name in [(16, "favicon-16.png"), (32, "favicon-32.png"), (180, "apple-touch-icon.png")]:
        # Pad to a square with the logo centered
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        fw, fh = favicon_src.size
        scale = size / max(fw, fh)
        new_w = max(1, int(fw * scale))
        new_h = max(1, int(fh * scale))
        scaled = favicon_src.resize((new_w, new_h), Image.LANCZOS)
        canvas.paste(scaled, ((size - new_w) // 2, (size - new_h) // 2), scaled)
        canvas.save(OUT / name, "PNG", optimize=True)
        print(f"  wrote {name} {canvas.size}")

    # Standard favicon.ico bundling 16+32
    ico_src_16 = Image.open(OUT / "favicon-16.png")
    ico_src_32 = Image.open(OUT / "favicon-32.png")
    ico_src_32.save(OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)])
    print("  wrote favicon.ico")


if __name__ == "__main__":
    main()
