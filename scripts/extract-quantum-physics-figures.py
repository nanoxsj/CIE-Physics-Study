from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/quantum-physics"
OUTPUT = ROOT / "Physics_Study/assets/questions/quantum-physics"

MASKED_FIGURES = {
    "photoelectric-energy-frequency-graph.webp": (
        "22.1-photoelectric/objects/photoelectric-001.png",
        "22.1-photoelectric/objects/photoelectric-002.png",
    ),
    "electron-diffraction-pattern-one.webp": (
        "22.2-duality/objects/duality-000.png",
        "22.2-duality/objects/duality-001.png",
    ),
    "electron-diffraction-pattern-two.webp": (
        "22.2-duality/objects/duality-002.png",
        "22.2-duality/objects/duality-003.png",
    ),
    "de-broglie-blank-graph.webp": (
        "22.2-duality/objects/duality-004.png",
        "22.2-duality/objects/duality-005.png",
    ),
    "photon-electron-scattering.webp": (
        "22.2-duality/objects/duality-006.png",
        "22.2-duality/objects/duality-007.png",
    ),
    "hydrogen-energy-levels.webp": (
        "22.3-quantisation/objects/quantisation-000.png",
        "22.3-quantisation/objects/quantisation-001.png",
    ),
    "hydrogen-lowest-energy-levels.webp": (
        "22.3-quantisation/objects/quantisation-002.png",
        "22.3-quantisation/objects/quantisation-003.png",
    ),
    "hydrogen-transition-regions.webp": (
        "22.3-quantisation/objects/quantisation-004.png",
        "22.3-quantisation/objects/quantisation-005.png",
    ),
    "atomic-emission-spectrum.webp": (
        "22.3-quantisation/objects/quantisation-006.png",
        "22.3-quantisation/objects/quantisation-007.png",
    ),
}

OPAQUE_FIGURES = {
    "photoelectric-reciprocal-wavelength-graph.webp": (
        "22.1-photoelectric/objects/photoelectric-000.png"
    ),
}


def composite_on_white(image_path: Path, mask_path: Path, output: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Image and mask sizes differ: {image_path.name}")
    white = Image.new("RGB", image.size, "white")
    white.paste(image, mask=mask)
    white.save(output, "WEBP", lossless=True, method=6)


OUTPUT.mkdir(parents=True, exist_ok=True)

for filename, (image_name, mask_name) in MASKED_FIGURES.items():
    composite_on_white(BASE / image_name, BASE / mask_name, OUTPUT / filename)

for filename, image_name in OPAQUE_FIGURES.items():
    Image.open(BASE / image_name).convert("RGB").save(
        OUTPUT / filename, "WEBP", lossless=True, method=6
    )
