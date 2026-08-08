"""Extract diagrams from Chapter 11 Particle Physics question PDFs.

The original ad-hoc extraction pulled every image object out of the PDFs with
``pdfimages`` and kept their numeric indices as the file names (``obj-000`` ...).
Because several questions contain more than one embedded image, the indices
drifted out of sync with the question order, so images ended up attached to the
wrong questions in the .qmd files.

This script instead renders only the question pages that contain diagrams and
crops the relevant region, so every output file is named after the question it
belongs to. Run it whenever the source PDFs are updated.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources/original-papers/particle-physics"
OUTPUT = ROOT / "assets/questions/particle-physics"

DPI = 200


def render_pages(pdf: Path, pages: list[int], scratch: Path) -> dict[int, Path]:
    first, last = min(pages), max(pages)
    prefix = scratch / pdf.stem.replace(" ", "_").replace(".", "")
    subprocess.run(
        [
            "pdftoppm",
            "-r",
            str(DPI),
            "-png",
            "-f",
            str(first),
            "-l",
            str(last),
            str(pdf),
            str(prefix),
        ],
        check=True,
        capture_output=True,
    )
    rendered: dict[int, Path] = {}
    for page in pages:
        candidate = prefix.with_name(f"{prefix.name}-{page:02d}.png")
        if not candidate.exists():
            candidate = prefix.with_name(f"{prefix.name}-{page}.png")
        rendered[page] = candidate
    return rendered


def crop_to_content(image: Image.Image, *, padding: int = 20) -> Image.Image:
    grayscale = image.convert("L")
    bbox = grayscale.point(lambda p: 0 if p >= 245 else 255).getbbox()
    if bbox is None:
        return image
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.width, bbox[2] + padding)
    bottom = min(image.height, bbox[3] + padding)
    return image.crop((left, top, right, bottom))


def save_webp(image: Image.Image, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(target, "WEBP", lossless=True, method=6)


# (page, (left, top, right, bottom) fractions, output filename)
FIGURES: dict[Path, list[tuple[int, tuple[float, float, float, float], str]]] = {
    SOURCE / "11.1 Atoms, Nuclei - Radiation - Choice - Medium.pdf.pdf": [
        (2, (0.04, 0.30, 0.99, 0.97), "11.1-c-medium-q01-decay-graphs.webp"),
        (5, (0.04, 0.27, 0.99, 0.97), "11.1-c-medium-q06-radiation-properties.webp"),
        (6, (0.04, 0.10, 0.99, 0.97), "11.1-c-medium-q07-nuclide-grid.webp"),
        (7, (0.45, 0.55, 0.99, 0.97), "11.1-c-medium-q09-alpha-deflection.webp"),
        (8, (0.04, 0.18, 0.99, 0.45), "11.1-c-medium-q10-decay-sequence.webp"),
        (9, (0.04, 0.18, 0.55, 0.97), "11.1-c-medium-q12-neutron-proton-graph.webp"),
        (10, (0.04, 0.10, 0.55, 0.97), "11.1-c-medium-q13-nucleon-proton-graph.webp"),
    ],
    SOURCE / "11.1 Atoms, Nuclei - Radiation - Choice - Hard.pdf.pdf": [
        (2, (0.04, 0.10, 0.55, 0.70), "11.1-c-hard-q01-scattering-apparatus.webp"),
        (2, (0.50, 0.55, 0.99, 0.95), "11.1-c-hard-q01-scattering-graphs.webp"),
        (3, (0.04, 0.10, 0.99, 0.55), "11.1-c-hard-q02-alpha-energy.webp"),
    ],
    SOURCE / "11.1 Atoms, Nuclei - Radiation - SQ - Medium.pdf.pdf": [
        (3, (0.04, 0.18, 0.99, 0.80), "11.1-sq-medium-q02-gold-foil-apparatus.webp"),
    ],
    SOURCE / "11.2 Fundamental Particles - Choice - Hard.pdf.pdf": [
       (3, (0.04, 0.30, 0.99, 0.85), "11.2-c-hard-q04-hadron-quark-diagrams.webp"),
       (4, (0.04, 0.18, 0.60, 0.97), "11.2-c-hard-q06-nucleon-proton-graph.webp"),
    ],
}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp)
        for pdf, crops in FIGURES.items():
            if not pdf.exists():
                print(f"  ! missing source PDF: {pdf.name}")
                continue
            pages = sorted({page for page, _, _ in crops})
            rendered = render_pages(pdf, pages, scratch)
            for page, frac, name in crops:
                image = Image.open(rendered[page])
                left = int(frac[0] * image.width)
                top = int(frac[1] * image.height)
                right = int(frac[2] * image.width)
                bottom = int(frac[3] * image.height)
                cropped = image.crop((left, top, right, bottom))
                cropped = crop_to_content(cropped)
                target = OUTPUT / name
                save_webp(cropped, target)
                print(f"  + {target.relative_to(ROOT)}  ({cropped.size[0]}x{cropped.size[1]})")


if __name__ == "__main__":
    main()
