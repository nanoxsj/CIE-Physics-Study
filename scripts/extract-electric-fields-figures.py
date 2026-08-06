from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/electric-fields/objects"
POTENTIAL_SOURCE = ROOT / "tmp/pdfs/electric-fields/potential/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/electric-fields"

FIGURES = {
    "opposite-point-charges.webp": ("electric-000.png", "electric-001.png"),
    "positron-between-charges.webp": ("electric-002.png", "electric-003.png"),
    "parallel-plates-field-lines.webp": ("electric-004.png", "electric-005.png"),
    "electron-between-parallel-plates.webp": ("electric-006.png", "electric-007.png"),
}

POTENTIAL_FIGURES = {
    "sphere-potential-distance.webp": ("potential-002.png", "potential-003.png"),
    "opposite-charges-potential-axis.webp": ("potential-004.png", "potential-005.png"),
    "blank-potential-distance-graph.webp": ("potential-006.png", "potential-007.png"),
}

POTENTIAL_OPAQUE_FIGURES = {
    "two-spheres-and-point-p.webp": "potential-000.png",
    "electric-field-between-spheres.webp": "potential-001.png",
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

for filename, (image_name, mask_name) in POTENTIAL_FIGURES.items():
    composite_on_white(
        POTENTIAL_SOURCE / image_name,
        POTENTIAL_SOURCE / mask_name,
        OUTPUT / filename,
    )

for filename, image_name in POTENTIAL_OPAQUE_FIGURES.items():
    image = Image.open(POTENTIAL_SOURCE / image_name).convert("RGB")
    image.save(OUTPUT / filename, "WEBP", lossless=True, method=6)
