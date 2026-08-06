#!/bin/zsh
set -eu

# Render original topical-question pages and their answer pages separately.
# Keeping a whole rendered page preserves English wording, diagrams, tables and
# answer layouts exactly as supplied in the source PDFs.

project_dir=${0:A:h:h}
source_root="$project_dir/.."
output_root="$project_dir/assets/topical/physical-quantities-and-units"
mkdir -p "$output_root"

render_pack() {
  local slug=$1
  local source_file=$2
  local answer_first=$3
  local total_pages=$4
  local question_last=$((answer_first - 1))
  local target="$output_root/$slug"
  mkdir -p "$target"

  pdftoppm -jpeg -jpegopt quality=92 -r 150 -f 2 -l "$question_last" \
    "$source_root/$source_file" "$target/question" >/dev/null 2>&1
  pdftoppm -jpeg -jpegopt quality=92 -r 150 -f "$answer_first" -l "$total_pages" \
    "$source_root/$source_file" "$target/answer" >/dev/null 2>&1
}

render_pack mc-easy 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Easy.pdf.pdf' 8 11
render_pack mc-medium 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Medium.pdf.pdf' 10 15
render_pack mc-hard 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - C - Hard.pdf.pdf' 10 19
render_pack sq-easy 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - SQ - Easy.pdf.pdf' 10 20
render_pack sq-medium 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - SQ - Medium.pdf.pdf' 14 34
render_pack sq-hard 'PastPaper/Topical Past Papers/AS/1.1 Physical Quantities - Units - SQ - Hard.pdf.pdf' 10 25

print "Rendered $(find "$output_root" -type f -name '*.jpg' | wc -l | tr -d '[:space:]') topical pages."
