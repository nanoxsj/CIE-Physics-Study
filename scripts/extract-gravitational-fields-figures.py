from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/gravitational-fields/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/gravitational-fields"

MASKED_FIGURES = {
    "saturn-field-blank.webp": ("u-easy-000.png", "u-easy-001.png"),
    "earth-person-ball-satellite.webp": ("p-easy-000.png", "p-easy-001.png"),
    "moon-two-satellites.webp": ("p-easy-002.png", "p-easy-003.png"),
    "mars-orbits-x-y.webp": ("p-easy-004.png", "p-easy-005.png"),
    "mars-potential-graph.webp": ("p-medium-000.png", "p-medium-001.png"),
    "mars-moons.webp": ("p-medium-002.png", "p-medium-003.png"),
    "rocket-planet-distances.webp": ("p-hard-000.png", "p-hard-001.png"),
    "planet-moon-potential-axes.webp": ("p-hard-002.png", "p-hard-003.png"),
}

OPAQUE_FIGURES = {
    "earth-moon-orbit.webp": "u-medium-000.png",
}


def save_webp(image: Image.Image, output_path: Path) -> None:
    image.convert("RGB").save(output_path, "WEBP", lossless=True, method=6)


def composite_on_white(image_path: Path, mask_path: Path, output_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Image and mask sizes differ: {image_path.name}")

    white = Image.new("RGB", image.size, "white")
    white.paste(image, mask=mask)
    save_webp(white, output_path)


OUTPUT.mkdir(parents=True, exist_ok=True)
for filename, (image_name, mask_name) in MASKED_FIGURES.items():
    composite_on_white(SOURCE / image_name, SOURCE / mask_name, OUTPUT / filename)

for filename, image_name in OPAQUE_FIGURES.items():
    save_webp(Image.open(SOURCE / image_name), OUTPUT / filename)
