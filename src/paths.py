from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
NIB_DIR = ASSETS_DIR / "nib"
ICONS_DIR = ASSETS_DIR / "icons"

APP_ICON = ICONS_DIR / "app.ico"
NIB_HAPPY = NIB_DIR / "nib_happy.png"