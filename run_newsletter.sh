#!/bin/bash
# The Bell — Weekly Newsletter Pipeline
# Runs every Monday at 1 AM (Malaysia time, Asia/Kuala_Lumpur)
# To run manually: bash run_newsletter.sh
# To test without sending: bash run_newsletter.sh --dry-run

set -e  # stop on first error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_DIR="$SCRIPT_DIR/.tmp/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/run_$(date +%Y-%m-%d_%H-%M).log"

DRY_RUN=""
if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "[DRY RUN MODE — email will not be sent]"
fi

{
  echo "================================================"
  echo "The Bell — Newsletter Run: $(date)"
  echo "================================================"

  echo ""
  echo "[1/6] Researching products (Tavily)..."
  python3 tools/research_products.py

  echo ""
  echo "[2/6] Drafting newsletter (Groq)..."
  python3 tools/draft_newsletter.py

  echo ""
  echo "[3/6] Formatting HTML email..."
  python3 tools/format_email.py

  echo ""
  echo "[4/6] Sending email..."
  python3 tools/send_email.py $DRY_RUN

  echo ""
  echo "[5/6] Logging to Google Sheets..."
  python3 tools/log_to_sheets.py

  if [[ -z "$DRY_RUN" ]]; then
    echo ""
    echo "[6/6] Advancing week counter..."
    python3 tools/advance_week.py
  else
    echo ""
    echo "[6/6] Skipping week advance (dry run)"
  fi

  echo ""
  echo "================================================"
  echo "DONE: $(date)"
  echo "================================================"

} 2>&1 | tee "$LOG_FILE"
