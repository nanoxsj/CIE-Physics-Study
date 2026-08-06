from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/magnetic-fields"
OUTPUT = ROOT / "Physics_Study/assets/questions/magnetic-fields"

MASKED = {
    "wire-through-card.webp": ("mf-easy", "mf-easy-000.png", "mf-easy-001.png"),
    "blank-field-around-wire.webp": ("mf-easy", "mf-easy-002.png", "mf-easy-003.png"),
    "blank-field-around-two-wires.webp": ("mf-easy", "mf-easy-004.png", "mf-easy-005.png"),
    "fleming-left-hand-rule.webp": ("mf-easy", "mf-easy-006.png", "mf-easy-007.png"),
    "field-into-page.webp": ("mf-easy", "mf-easy-008.png", "mf-easy-009.png"),
    "electron-in-magnetic-field.webp": ("mf-easy", "mf-easy-010.png", "mf-easy-011.png"),
    "magnetic-directions-table.webp": ("mf-easy", "mf-easy-012.png", "mf-easy-013.png"),
    "rectangular-current-loop.webp": ("mf-easy", "mf-easy-014.png", "mf-easy-015.png"),
    "solenoid-field-points.webp": ("mf-medium", "mf-medium-002.png", "mf-medium-003.png"),
    "coil-near-solenoid.webp": ("ei-easy", "ei-easy-000.png", "ei-easy-001.png"),
    "rotating-coil-in-field.webp": ("ei-easy", "ei-easy-002.png", "ei-easy-003.png"),
    "magnet-coil-voltmeter.webp": ("ei-easy", "ei-easy-004.png", "ei-easy-005.png"),
    "voltmeter-deflection.webp": ("ei-easy", "ei-easy-006.png", "ei-easy-007.png"),
    "blank-voltmeter-observations.webp": ("ei-easy", "ei-easy-008.png", "ei-easy-009.png"),
    "nested-solenoids.webp": ("ei-medium", "ei-medium-001.png", "ei-medium-002.png"),
    "square-coil-in-field.webp": ("ei-medium", "ei-medium-003.png", "ei-medium-004.png"),
    "flux-density-time-graph.webp": ("ei-medium", "ei-medium-005.png", "ei-medium-006.png"),
}

OPAQUE = {
    "two-coils-separation.webp": ("mf-medium", "mf-medium-000.png"),
    "hall-slice.webp": ("mf-medium", "mf-medium-001.png"),
    "induced-voltage-time-graph.webp": ("ei-easy", "ei-easy-010.png"),
    "coil-c-around-solenoid.webp": ("ei-medium", "ei-medium-000.png"),
}


def composite(source: Path, image_name: str, mask_name: str, output: Path) -> None:
    image = Image.open(source / image_name).convert("RGB")
    mask = Image.open(source / mask_name).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Image and mask sizes differ: {image_name}")
    white = Image.new("RGB", image.size, "white")
    white.paste(image, mask=mask)
    white.save(output, "WEBP", lossless=True, method=6)


OUTPUT.mkdir(parents=True, exist_ok=True)
for filename, (folder, image_name, mask_name) in MASKED.items():
    composite(BASE / folder / "objects", image_name, mask_name, OUTPUT / filename)

for filename, (folder, image_name) in OPAQUE.items():
    image = Image.open(BASE / folder / "objects" / image_name).convert("RGB")
    image.save(OUTPUT / filename, "WEBP", lossless=True, method=6)
