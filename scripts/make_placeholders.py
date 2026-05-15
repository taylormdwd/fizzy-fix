"""Generate brand-tinted placeholder images for Fizzy Fix."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent.parent / "public" / "images"
OUT.mkdir(parents=True, exist_ok=True)

BLUSH = (245, 200, 200)
BLUSH_SOFT = (249, 221, 216)
CREAM = (251, 243, 229)
CREAM_WARM = (248, 232, 200)
GREEN_DEEP = (47, 93, 58)
GREEN_LEAF = (74, 115, 64)
CORAL = (229, 117, 127)
RED_SODA = (199, 62, 62)
WHITE = (255, 255, 255)
CHARCOAL = (42, 42, 42)


def font(size: int):
    for name in [
        "C:/Windows/Fonts/Georgia.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Verdana.ttf",
    ]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw, txt, fnt):
    box = draw.textbbox((0, 0), txt, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def checkerboard(img, draw, color_a, color_b, square=24):
    w, h = img.size
    for y in range(0, h, square):
        for x in range(0, w, square):
            color = color_a if (x // square + y // square) % 2 == 0 else color_b
            draw.rectangle([x, y, x + square, y + square], fill=color)


def label(draw, w, h, filename, dims, fnt_lg, fnt_sm, fg=GREEN_DEEP):
    line1 = filename
    line2 = f"{dims[0]} x {dims[1]}"
    tw, th = text_size(draw, line1, fnt_lg)
    draw.text(((w - tw) / 2, h / 2 - th - 6), line1, fill=fg, font=fnt_lg)
    tw, th = text_size(draw, line2, fnt_sm)
    draw.text(((w - tw) / 2, h / 2 + 8), line2, fill=fg, font=fnt_sm)


def make_image(filename, w, h, bg, accent=None, save_format=None):
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    # subtle checker corner for visual interest
    if accent:
        for sq_y in range(0, 80, 20):
            for sq_x in range(0, 80, 20):
                if (sq_x // 20 + sq_y // 20) % 2 == 0:
                    draw.rectangle([sq_x, sq_y, sq_x + 20, sq_y + 20], fill=accent)
    # frame
    draw.rectangle([0, 0, w - 1, h - 1], outline=GREEN_DEEP, width=4)
    fnt_lg = font(max(18, min(w, h) // 14))
    fnt_sm = font(max(13, min(w, h) // 22))
    label(draw, w, h, filename, (w, h), fnt_lg, fnt_sm)
    out_path = OUT / filename
    fmt = save_format or ("PNG" if filename.lower().endswith(".png") else "JPEG")
    img.save(out_path, fmt, quality=88)
    print(f"wrote {out_path}")


def make_mascot():
    """Cute soda-cup mascot placeholder. Transparent PNG, 80x80 logical (240x240 retina)."""
    w = h = 240
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # cup body (trapezoid-ish)
    cup = [(50, 70), (190, 70), (175, 220), (65, 220)]
    draw.polygon(cup, fill=BLUSH, outline=GREEN_DEEP)
    # vertical stripes (checkerboard pinstripes)
    for x in range(60, 180, 12):
        draw.line([(x, 75), (x - 8, 215)], fill=WHITE, width=2)
    # lid
    draw.rectangle([45, 60, 195, 80], fill=GREEN_DEEP)
    draw.rectangle([55, 50, 185, 65], fill=CORAL)
    # straw
    draw.rectangle([110, 10, 130, 60], fill=RED_SODA)
    # face (eyes + smile)
    draw.ellipse([90, 110, 110, 130], fill=CHARCOAL)
    draw.ellipse([130, 110, 150, 130], fill=CHARCOAL)
    # rosy cheeks
    draw.ellipse([80, 140, 100, 160], fill=CORAL)
    draw.ellipse([140, 140, 160, 160], fill=CORAL)
    # smile arc
    draw.arc([100, 140, 140, 180], start=0, end=180, fill=CHARCOAL, width=4)
    img.save(OUT / "mascot-cup.png", "PNG")
    print(f"wrote {OUT / 'mascot-cup.png'}")


def main():
    # Hero
    make_image("hero-trailer.jpg", 1200, 800, BLUSH, accent=WHITE)
    # Mascot (custom drawing)
    make_mascot()
    # Owner
    make_image("shara-counter.jpg", 600, 800, BLUSH_SOFT, accent=CREAM)
    # Drinks (400x500)
    drinks = [
        ("drink-spice.jpg", BLUSH),
        ("drink-caramel.jpg", CREAM_WARM),
        ("drink-cider.jpg", BLUSH_SOFT),
        ("drink-cupid.jpg", BLUSH),
        ("drink-callmemaybe.jpg", CREAM_WARM),
        ("drink-xoxo.jpg", BLUSH_SOFT),
    ]
    for name, color in drinks:
        make_image(name, 400, 500, color, accent=WHITE)
    # Past events (4:3 portrait-ish 800x600)
    events = [
        ("wedding-gilbert.jpg", BLUSH),
        ("suns-phoenix.jpg", CREAM_WARM),
        ("dmc-scottsdale.jpg", BLUSH_SOFT),
        ("sweet16-mesa.jpg", BLUSH),
        ("valleygirl-tempe.jpg", CREAM),
        ("polar-chandler.jpg", BLUSH_SOFT),
        ("corporate-phoenix.jpg", CREAM_WARM),
        ("babyshower-qc.jpg", BLUSH),
    ]
    for name, color in events:
        make_image(name, 800, 600, color, accent=WHITE)


if __name__ == "__main__":
    main()
