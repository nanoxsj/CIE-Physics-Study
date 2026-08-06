from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
CAPACITORS_SOURCE = ROOT / "tmp/pdfs/capacitance/capacitors/objects"
CHARGING_SOURCE = ROOT / "tmp/pdfs/capacitance/charging/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/capacitance"

CAPACITOR_FIGURES = {
    "parallel-capacitors-derivation.webp": ("capacitors-000.png", "capacitors-001.png"),
    "two-capacitors-switch-circuit.webp": ("capacitors-002.png", "capacitors-003.png"),
    "three-capacitor-network.webp": ("capacitors-004.png", "capacitors-005.png"),
    "capacitor-construction.webp": ("capacitors-006.png", "capacitors-007.png"),
    "charge-voltage-graph.webp": ("capacitors-008.png", "capacitors-009.png"),
    "three-parallel-capacitors.webp": ("capacitors-010.png", "capacitors-011.png"),
}

CHARGING_FIGURES = {
    "charge-voltage-and-discharge-circuit.webp": ("charging-002.png", "charging-003.png"),
    "discharge-switch-circuit.webp": ("charging-004.png", "charging-005.png"),
    "coupled-wire-discharge-circuit.webp": ("charging-006.png", "charging-007.png"),
    "blank-discharge-current-graph.webp": ("charging-008.png", "charging-009.png"),
    "blank-induced-voltage-graph.webp": ("charging-010.png", "charging-011.png"),
}

CHARGING_OPAQUE_FIGURES = {
    "half-wave-rectified-voltage.webp": "charging-000.png",
    "smoothing-circuit.webp": "charging-001.png",
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

for filename, (image_name, mask_name) in CAPACITOR_FIGURES.items():
    composite_on_white(CAPACITORS_SOURCE, image_name, mask_name, OUTPUT / filename)

for filename, (image_name, mask_name) in CHARGING_FIGURES.items():
    composite_on_white(CHARGING_SOURCE, image_name, mask_name, OUTPUT / filename)

for filename, image_name in CHARGING_OPAQUE_FIGURES.items():
    image = Image.open(CHARGING_SOURCE / image_name).convert("RGB")
    image.save(OUTPUT / filename, "WEBP", lossless=True, method=6)
