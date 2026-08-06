#!/bin/zsh
set -eu

# Extract original diagrams for MC cards. The PDFs contain these as individual
# images, which is cleaner and more reliable than cropping rendered pages.

project_dir=${0:A:h:h}
source_root="$project_dir/.."
target_root="$project_dir/assets/questions/physical-quantities-and-units"
scratch_dir=$(mktemp -d)
mkdir -p "$target_root/mc-medium" "$target_root/mc-hard"

cleanup() { rm -rf "$scratch_dir"; }
trap cleanup EXIT

extract_pack() {
  local pack=$1
  local source_pdf=$2
  pdfimages -j "$source_root/$source_pdf" "$scratch_dir/$pack"
}

convert_image() {
  local pack=$1
  local index=$2
  local target=$3
  sips -s format jpeg "$scratch_dir/$pack-${index}.ppm" \
    --out "$target_root/$pack/$target.jpg" >/dev/null
}

extract_pack mc-medium 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Medium.pdf.pdf'
convert_image mc-medium 000 q04-vectors-p-q
convert_image mc-medium 001 q04-option-a
convert_image mc-medium 002 q04-option-b
convert_image mc-medium 003 q04-option-c
convert_image mc-medium 004 q04-option-d
convert_image mc-medium 005 q08-components

extract_pack mc-hard 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Hard.pdf.pdf'
convert_image mc-hard 000 q07-forces
convert_image mc-hard 001 q09-option-a
convert_image mc-hard 002 q09-option-b
convert_image mc-hard 003 q09-option-c
convert_image mc-hard 004 q09-option-d
convert_image mc-hard 005 q10-glider
convert_image mc-hard 006 q10-option-a
convert_image mc-hard 007 q10-option-b
convert_image mc-hard 008 q10-option-c
convert_image mc-hard 009 q10-option-d
