from pathlib import Path
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE = BASE_DIR / "assets" / "nib" / "nib_icon.png"
OUTPUT = BASE_DIR / "assets" / "icons" / "app.ico"


def main():
    image = Image.open(SOURCE).convert("RGBA")

    icon_sizes = [
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    image.save(
        OUTPUT,
        format="ICO",
        sizes=icon_sizes,
    )

    print(f"Created icon: {OUTPUT}")


if __name__ == "__main__":
    main()