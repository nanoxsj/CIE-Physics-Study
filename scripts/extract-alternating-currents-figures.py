from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/alternating-currents"
OUTPUT = ROOT / "Physics_Study/assets/questions/alternating-currents"

FIGURES = {
    "generator-coil.webp": ("easy", "easy-000.png", "easy-001.png"),
    "generator-output-voltage.webp": ("easy", "easy-002.png", "easy-003.png"),
    "alternating-input-waveform.webp": ("easy", "easy-004.png", "easy-005.png"),
    "blank-half-wave-graph.webp": ("easy", "easy-006.png", "easy-007.png"),
    "blank-full-wave-graph.webp": ("easy", "easy-008.png", "easy-009.png"),
    "smoothed-ripple.webp": ("easy", "easy-010.png", "easy-011.png"),
    "diode-bridge-labelled.webp": ("easy", "easy-012.png", "easy-013.png"),
    "diode-bridge-path-one.webp": ("easy", "easy-014.png", "easy-015.png"),
    "diode-bridge-path-two.webp": ("easy", "easy-016.png", "easy-017.png"),
    "incomplete-bridge-rectifier.webp": ("medium", "medium-000.png", "medium-001.png"),
    "sinusoidal-voltage-time.webp": ("medium", "medium-002.png", "medium-003.png"),
    "full-wave-rectifier-load.webp": ("medium", "medium-004.png", "medium-005.png"),
    "blank-rectified-output.webp": ("medium", "medium-006.png", "medium-007.png"),
    "blank-power-time-graph.webp": ("medium", "medium-008.png", "medium-009.png"),
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
for filename, (folder, image_name, mask_name) in FIGURES.items():
    composite(BASE / folder / "objects", image_name, mask_name, OUTPUT / filename)
