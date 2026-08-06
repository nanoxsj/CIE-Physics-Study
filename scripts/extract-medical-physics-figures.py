from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/medical-physics"
OUTPUT = ROOT / "Physics_Study/assets/questions/medical-physics"

FIGURES = {
    "xray-tube-diagram.webp": ("24.1-easy", "easy-002.png", "easy-003.png"),
    "piezoelectric-transducer.webp": ("24.1-medium", "medium-000.png", "medium-001.png"),
    "bone-muscle-xray-path.webp": ("24.1-medium", "medium-002.png", "medium-003.png"),
    "pzt-molecular-structure.webp": ("24.1-hard", "hard-000.png", "hard-001.png"),
    "eye-a-scan-position.webp": ("24.1-hard", "hard-002.png", "hard-003.png"),
    "eye-a-scan-trace.webp": ("24.1-hard", "hard-004.png", "hard-005.png"),
    "eye-ultrasound-attenuation.webp": ("24.1-hard", "hard-006.png", "hard-007.png"),
    "muscle-attenuation-energy-graph.webp": ("24.1-hard", "hard-008.png", "hard-009.png"),
    "bone-muscle-sample.webp": ("24.1-hard", "hard-010.png", "hard-011.png"),
    "pet-detector-ring-head.webp": ("24.2-easy", "pet-easy-002.png", "pet-easy-003.png"),
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
