from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/thermodynamics/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/thermodynamics"

FIGURES = {
    "cycle-abc.webp": ("thermo-000.png", "thermo-001.png"),
    "pressure-volume-cycle-xyz.webp": ("thermo-002.png", "thermo-003.png"),
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
