from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp/pdfs/nuclear-physics"
OUTPUT = ROOT / "Physics_Study/assets/questions/nuclear-physics"

FIGURES = {
    "binding-energy-regions-graph.webp": ("23.1-easy", "mass-easy-000.png", "mass-easy-001.png"),
    "binding-energy-reading-graph.webp": ("23.1-easy", "mass-easy-002.png", "mass-easy-003.png"),
    "blank-binding-energy-curve.webp": ("23.1-medium", "mass-medium-000.png", "mass-medium-001.png"),
    "labelled-binding-energy-curve.webp": ("23.1-medium", "mass-medium-002.png", "mass-medium-003.png"),
    "random-count-rate-graph.webp": ("23.2-easy", "decay-easy-000.png", "decay-easy-001.png"),
    "neptunium-decay-chart.webp": ("23.2-easy", "decay-easy-002.png", "decay-easy-003.png"),
    "apparatus-purpose-table.webp": ("23.2-easy", "decay-easy-004.png", "decay-easy-005.png"),
    "technetium-activity-time-graph.webp": ("23.2-easy", "decay-easy-006.png", "decay-easy-007.png"),
    "polonium-lead-decay-chart.webp": ("23.2-easy", "decay-easy-008.png", "decay-easy-009.png"),
    "technetium-nuclei-time-graph.webp": ("23.2-medium", "decay-medium-000.png", "decay-medium-001.png"),
    "blank-decay-nuclei-time-graph.webp": ("23.2-medium", "decay-medium-002.png", "decay-medium-003.png"),
    "blank-activity-nuclei-graph.webp": ("23.2-medium", "decay-medium-004.png", "decay-medium-005.png"),
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
