#!/usr/bin/env bash
# render.sh — HTML resume/cover-letter -> print-safe PDF + rasterized pages for the print-eval.
#
# A resume is a print deliverable. Page-count is NOT a pass — you must LOOK at the rendered pages.
# This renders the PDF with headless Chrome (respects @page margins + print CSS), then rasterizes
# each page to PNG so the agent can actually view them and check for orphans, widows, bad margins.
#
# Usage:  ./render.sh path/to/resume.html [output-basename]
# Output: <basename>.pdf  and  <basename>-page-1.png, -page-2.png, ...
# Deps:   Google Chrome (headless) + pdftoppm (poppler).  Fallbacks: chromium; magick/gs for raster.

set -euo pipefail
IN="${1:?usage: render.sh <input.html> [output-basename]}"
BASE="${2:-$(basename "${IN%.*}")}"
OUT="${BASE}.pdf"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="/Applications/Chromium.app/Contents/MacOS/Chromium"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -n "$CHROME" ] || { echo "no Chrome/Chromium found"; exit 1; }

ABS="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$ABS" 2>/dev/null
sleep 1

rm -f "${BASE}-page-"*.png
if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 110 "$OUT" "${BASE}-page" 2>/dev/null
elif command -v magick >/dev/null 2>&1; then
  magick -density 110 "$OUT" "${BASE}-page-%d.png"
elif command -v gs >/dev/null 2>&1; then
  gs -sDEVICE=png16m -r110 -o "${BASE}-page-%d.png" "$OUT" >/dev/null 2>&1
fi

PAGES=$(ls "${BASE}-page-"*.png 2>/dev/null | wc -l | tr -d ' ')
echo "PDF: $OUT  ($(du -h "$OUT" | cut -f1))  ·  pages: $PAGES"
echo "NOW LOOK AT: ${BASE}-page-*.png  — verify 1-2 pages, no orphan headers, no widows, clean margins, glass flattened."
