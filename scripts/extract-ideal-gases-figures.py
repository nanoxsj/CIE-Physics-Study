from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/ideal-gases/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/ideal-gases"

FIGURES = {
    "gas-cylinder-dimensions.webp": ("igl-medium-000.png", "igl-medium-001.png"),
    "pressure-temperature-axes.webp": ("igl-medium-002.png", "igl-medium-003.png"),
    "particle-in-cube-labels.webp": ("kt-easy-000.png", "kt-easy-001.png"),
    "nitrogen-piston.webp": ("kt-medium-000.png", "kt-medium-001.png"),
    "pressure-rms-speed-axes.webp": ("kt-medium-002.png", "kt-medium-003.png"),
    "molecule-in-cube.webp": ("kt-medium-004.png", "kt-medium-005.png"),
    "gas-collimator.webp": ("kt-hard-002.png", "kt-hard-003.png"),
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
