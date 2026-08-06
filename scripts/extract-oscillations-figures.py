from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp/pdfs/oscillations/objects"
OUTPUT = ROOT / "Physics_Study/assets/questions/oscillations"

MASKED_FIGURES = {
    "easy-pendulum-labels.webp": ("shm-easy-000.png", "shm-easy-001.png"),
    "easy-acceleration-displacement.webp": ("shm-easy-002.png", "shm-easy-003.png"),
    "easy-starting-position-graphs.webp": ("shm-easy-004.png", "shm-easy-005.png"),
    "easy-energy-displacement.webp": ("shm-easy-006.png", "shm-easy-007.png"),
    "pendulum-arrangement.webp": ("shm-medium-000.png", "shm-medium-001.png"),
    "pendulum-acceleration-displacement.webp": ("shm-medium-002.png", "shm-medium-003.png"),
    "spring-oscillator.webp": ("shm-medium-004.png", "shm-medium-005.png"),
    "spring-velocity-displacement.webp": ("shm-medium-006.png", "shm-medium-007.png"),
    "coupled-pendulums.webp": ("damped-medium-002.png", "damped-medium-003.png"),
    "coupled-pendulum-displacements.webp": ("damped-medium-004.png", "damped-medium-005.png"),
}

OPAQUE_FIGURES = {
    "magnet-coil-arrangement.webp": "damped-medium-000.png",
    "damped-magnet-displacement.webp": "damped-medium-001.png",
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

for filename, (image_name, mask_name) in MASKED_FIGURES.items():
    composite_on_white(SOURCE / image_name, SOURCE / mask_name, OUTPUT / filename)

for filename, image_name in OPAQUE_FIGURES.items():
    image = Image.open(SOURCE / image_name).convert("RGB")
    image.save(OUTPUT / filename, "WEBP", lossless=True, method=6)
