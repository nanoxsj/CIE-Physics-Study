from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/astronomy-cosmology"
OUTPUT = ROOT / "Physics_Study/assets/questions/astronomy-cosmology"

FIGURES = {
    "sadr-aljanah-emission-curves.webp": (
        "25.1-medium",
        "medium-000.png",
        "medium-001.png",
    ),
    "magnetar-intensity-energy.webp": (
        "25.1-hard",
        "hard-000.png",
        "hard-001.png",
    ),
    "hubble-recession-distance.webp": (
        "25.2-hard",
        "hard-000.png",
        "hard-001.png",
    ),
    "stellar-spectral-lines.webp": (
        "25.2-hard",
        "hard-002.png",
        "hard-003.png",
    ),
    "hubble-original-plot.webp": (
        "25.2-hard",
        "hard-004.png",
        "hard-005.png",
    ),
}


def composite_on_white(source: Path, image_name: str, mask_name: str, output: Path) -> None:
    image = Image.open(source / image_name).convert("RGB")
    mask = Image.open(source / mask_name).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Image and mask sizes differ: {image_name}")
    white = Image.new("RGB", image.size, "white")
    white.paste(image, mask=mask)
    white.save(output, "WEBP", lossless=True, method=6)


OUTPUT.mkdir(parents=True, exist_ok=True)
for filename, (folder, image_name, mask_name) in FIGURES.items():
    composite_on_white(BASE / folder / "objects", image_name, mask_name, OUTPUT / filename)
