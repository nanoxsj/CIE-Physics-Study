#!/bin/zsh
set -eu

# Q9 and Q10 contain vector diagrams. Extract their original embedded images
# rather than cropping a rendered page. This keeps the arrows and thin lines
# sharp and avoids including surrounding page text.

project_dir=${0:A:h:h}
target_dir="$project_dir/assets/questions/physical-quantities-and-units/mc-easy"
source_pdf="$project_dir/../PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Easy.pdf.pdf"
scratch_dir=$(mktemp -d)
mkdir -p "$target_dir"

cleanup() { rm -rf "$scratch_dir"; }
trap cleanup EXIT

pdfimages -j "$source_pdf" "$scratch_dir/image"

# Image 000 is Q9. Images 001–005 are Q10: R, then choices A–D.
for mapping in \
  '000:q09-vector-addition' \
  '001:q10-resultant-r' \
  '002:q10-option-a' \
  '003:q10-option-b' \
  '004:q10-option-c' \
  '005:q10-option-d'; do
  image_index=${mapping%%:*}
  image_name=${mapping##*:}
  sips -s format jpeg "$scratch_dir/image-${image_index}.ppm" \
    --out "$target_dir/$image_name.jpg" >/dev/null
done
