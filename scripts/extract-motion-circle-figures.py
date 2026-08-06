from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/motion-circle/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/motion-in-a-circle"

FIGURES = {
    "children-rotation.webp": ("kin-000.png", "kin-001.png"),
    "children-rope-snaps.webp": ("kin-002.png", "kin-003.png"),
    "earth-field-lines.webp": ("easy-000.png", "easy-001.png"),
    "jupiter-moons.webp": ("easy-002.png", "easy-003.png"),
    "circular-track.webp": ("medium-000.png", "medium-001.png"),
    "skating-bowl.webp": ("medium-002.png", "medium-003.png"),
    "skateboarder-side-view.webp": ("medium-004.png", "medium-005.png"),
}


def composite_on_white(image_path: Path, mask_path: Path, output_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Image and mask sizes differ: {image_path.name}")

    white = Image.new("RGB", image.size, "white")
    white.paste(image, mask=mask)
    white.save(output_path, "WEBP", lossless=True, method=6)


OUTPUT.mkdir(parents=True, exist_ok=True)
for filename, (image_name, mask_name) in FIGURES.items():
    composite_on_white(SOURCE / image_name, SOURCE / mask_name, OUTPUT / filename)
