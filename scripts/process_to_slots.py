"""Process candidate images into /public/images/ at exact slot specs.

Center-crop unless a custom focal box is provided. JPGs are saved at q=85.
mascot-cup.png is saved as a transparent PNG (cream pixels keyed out).
"""
from pathlib import Path
from PIL import Image
import shutil

BASE = Path(r"C:/Users/misst/fizzy-fix")
CAND = BASE / "tmp" / "candidates"
OUT = BASE / "public" / "images"
EXTRAS = OUT / "extras"
OUT.mkdir(parents=True, exist_ok=True)
EXTRAS.mkdir(parents=True, exist_ok=True)

# (slot_filename, source_candidate, target_w, target_h, crop_box=None)
# crop_box is (left_frac, top_frac, right_frac, bottom_frac) of the source image.
# When crop_box is None, do a center-crop to the target aspect ratio.
JOBS = [
    ("hero-trailer.jpg",     "c012.jpg", 1200, 800,  None),
    ("shara-counter.jpg",    "c046.jpg",  600, 800,  None),
    ("shara-portrait.jpg",   "c036.jpg",  600, 800,  (0.10, 0.00, 0.62, 1.00)),  # crop out right-side text
    ("drink-spice.jpg",      "c041.jpg",  400, 500,  None),
    ("drink-caramel.jpg",    "c043.jpg",  400, 500,  (0.55, 0.40, 1.00, 1.00)),  # rightmost cup w/ apple slices
    ("drink-cupid.jpg",      "c009.jpg",  400, 500,  (0.30, 0.18, 0.78, 0.78)),  # center heart cup
    ("drink-callmemaybe.jpg","c009.jpg",  400, 500,  (0.00, 0.30, 0.45, 0.85)),  # left cup w/ strawberries
    ("drink-xoxo.jpg",       "c009.jpg",  400, 500,  (0.45, 0.55, 0.95, 1.00)),  # bottom-right red cup
    ("valleygirl-tempe.jpg", "c008.jpg",  800, 600,  None),
]

# Mascot crop comes out of c031 — left side of the brand-logo lockup.
MASCOT_SRC = "c031.jpg"
MASCOT_BOX = (0.13, 0.50, 0.37, 0.96)  # the walking soda-cup character


def center_crop_to_aspect(img: Image.Image, w: int, h: int) -> Image.Image:
    target = w / h
    iw, ih = img.size
    actual = iw / ih
    if actual > target:
        # too wide — crop horizontally
        new_w = int(ih * target)
        left = (iw - new_w) // 2
        box = (left, 0, left + new_w, ih)
    else:
        # too tall — crop vertically
        new_h = int(iw / target)
        top = (ih - new_h) // 2
        box = (0, top, iw, top + new_h)
    return img.crop(box)


def process_jpg(slot, src, w, h, crop_box):
    src_path = CAND / src
    if not src_path.exists():
        print(f"  MISS source: {src} for {slot}")
        return False
    img = Image.open(src_path).convert("RGB")
    if crop_box is not None:
        iw, ih = img.size
        l, t, r, b = crop_box
        img = img.crop((int(l * iw), int(t * ih), int(r * iw), int(b * ih)))
    img = center_crop_to_aspect(img, w, h)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(OUT / slot, "JPEG", quality=85, optimize=True)
    print(f"  ok  {slot:28s} <- {src}")
    return True


def process_mascot():
    src_path = CAND / MASCOT_SRC
    if not src_path.exists():
        print(f"  MISS mascot source: {MASCOT_SRC}")
        return False
    img = Image.open(src_path).convert("RGBA")
    iw, ih = img.size
    l, t, r, b = MASCOT_BOX
    img = img.crop((int(l * iw), int(t * ih), int(r * iw), int(b * ih)))
    # Resize to max-width 400 keeping aspect
    cw, ch = img.size
    if cw > 400:
        new_h = int(ch * (400 / cw))
        img = img.resize((400, new_h), Image.LANCZOS)
    # Key out cream-colored background. Source cream is around #FBF3E5.
    px = img.load()
    cw, ch = img.size
    for y in range(ch):
        for x in range(cw):
            r_, g_, b_, a_ = px[x, y]
            # cream-ish: high R/G/B, all close to each other, slightly warm
            if r_ > 235 and g_ > 225 and b_ > 210 and abs(r_ - g_) < 30 and abs(g_ - b_) < 40:
                px[x, y] = (r_, g_, b_, 0)
    img.save(OUT / "mascot-cup.png", "PNG")
    print(f"  ok  mascot-cup.png            <- {MASCOT_SRC} (transparent)")
    return True


def main():
    print("Processing slot images...")
    success = []
    for slot, src, w, h, box in JOBS:
        if process_jpg(slot, src, w, h, box):
            success.append(slot)
    if process_mascot():
        success.append("mascot-cup.png")

    print(f"\nMatched {len(success)} slots.")

    # Move every untouched candidate to extras/
    used_sources = {src for _, src, *_ in JOBS} | {MASCOT_SRC}
    moved = 0
    for cand in sorted(CAND.glob("c*.jpg")):
        dst = EXTRAS / cand.name
        if not dst.exists():
            shutil.copy2(cand, dst)
            moved += 1
    print(f"Copied {moved} candidates to extras/.")

    # Audit
    expected = [
        ("hero-trailer.jpg", "Pink trailer exterior, daytime"),
        ("shara-counter.jpg", "Founder behind counter, candid"),
        ("shara-portrait.jpg", "Founder solo, styled, smiling"),
        ("mascot-cup.png", "Soda-cup mascot illustration, transparent PNG"),
        ("drink-spice.jpg", "Iced drink with cinnamon sugar rim"),
        ("drink-caramel.jpg", "Drink with caramel drizzle / whipped topping"),
        ("drink-cider.jpg", "Apple cider drink with cinnamon sticks"),
        ("drink-cupid.jpg", "Heart-shaped cup, pink drink, sprinkles"),
        ("drink-callmemaybe.jpg", "Orange/peach drink with green Fizzy Fix sticker"),
        ("drink-xoxo.jpg", "Strawberry/coconut drink with Valentine styling"),
        ("wedding-gilbert.jpg", "White lace dress closeup with cup, or trailer at outdoor wedding"),
        ("suns-phoenix.jpg", "Phoenix Suns branding, court, or stadium"),
        ("dmc-scottsdale.jpg", "Desert Moms Club kickoff group photo or graphic"),
        ("sweet16-mesa.jpg", "Birthday balloons, sweet 16 vibe"),
        ("valleygirl-tempe.jpg", "Pink Valley Girl event poster"),
        ("polar-chandler.jpg", "Christmas balloons or kids holiday party setup"),
        ("corporate-phoenix.jpg", "Outdoor evening event with adults, brand activation feel"),
        ("babyshower-qc.jpg", "Maternity bump or baby shower setup"),
    ]
    needs = []
    for fname, desc in expected:
        if not (OUT / fname).exists():
            needs.append((fname, desc))
            print(f"  NEEDS PHOTO: {fname}, {desc}")
    print(f"\n{len(expected) - len(needs)} of {len(expected)} slots filled.")
    print(f"{len(needs)} slot(s) still need a photo.")


if __name__ == "__main__":
    main()
