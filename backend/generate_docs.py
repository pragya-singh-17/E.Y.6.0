from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DATA_DIR = Path(__file__).resolve().parent / "data" / "docs"


TEXT_TEMPLATES = {
    "P001": "License: LIC-ROHAN-1\nName: Dr. Rohan Verma\nExpiry: 2026-06-30",
    "P002": "License: LIC-MEERA-1\nName: Dr. Meera Patel\nExpiry: 2024-12-31",
    "P010": "License: LIC-SNEHA-1\nName: Dr. Sneha Kulkarni\nExpiry: 2025-02-14",
    "P101": "License: LIC-DEMO-1\nName: Dr. Test One\nExpiry: 2025-12-31",
    "P102": "License: LIC-DEMO-2\nName: Dr. Test Two\nExpiry: 2025-06-30",
}


def make_image(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.multiline_text((40, 40), text, fill="black", font=font, spacing=8)
    img.save(path)


def main() -> None:
    for provider_id, text in TEXT_TEMPLATES.items():
        out = DATA_DIR / f"{provider_id}.png"
        make_image(text, out)
        print(f"Generated {out}")


if __name__ == "__main__":
    main()
