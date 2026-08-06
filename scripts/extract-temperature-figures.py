from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/temperature/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/temperature"

FIGURES = {
    "energy-flow-regions.webp": ("mt-easy-000.png", "mt-easy-001.png"),
    "thermistor-graph-axes.webp": ("mt-easy-002.png", "mt-easy-003.png"),
    "thermocouple-unlabelled.webp": ("mt-easy-004.png", "mt-easy-005.png"),
    "thermocouple-emf-axes.webp": ("mt-easy-006.png", "mt-easy-007.png"),
    "coffee-cooling-curve.webp": ("mt-medium-000.png", "mt-medium-001.png"),
    "thermocouple-calibration-curve.webp": ("mt-medium-002.png", "mt-medium-003.png"),
    "steel-manufacturing-process.webp": ("mt-hard-000.png", "mt-hard-001.png"),
    "temperature-sensor-comparison.webp": ("mt-hard-002.png", "mt-hard-003.png"),
    "thermistor-multimeter.webp": ("mt-hard-004.png", "mt-hard-005.png"),
    "thermistor-plot-axes.webp": ("mt-hard-006.png", "mt-hard-007.png"),
    "changes-of-state-unlabelled.webp": ("pc-easy-000.png", "pc-easy-001.png"),
    "heating-curve-unlabelled.webp": ("pc-easy-002.png", "pc-easy-003.png"),
    "substance-heating-curve.webp": ("pc-medium-000.png", "pc-medium-001.png"),
    "ice-temperature-axes.webp": ("pc-hard-000.png", "pc-hard-001.png"),
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
