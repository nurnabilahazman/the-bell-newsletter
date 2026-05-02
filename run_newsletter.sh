#!/bin/bash
# The Bell — Weekly Newsletter Pipeline
# Runs every Monday at 1 AM (Malaysia time, Asia/Kuala_Lumpur)
# To run manually: bash run_newsletter.sh
# To test without sending: bash run_newsletter.sh --dry-run

set -e  # stop on first error

# Ensure python3 is findable when run by cron (no normal shell PATH)
export PATH="/usr/local/bin:/usr/bin:/bin:/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin:$PATH"

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
  echo "[1/7] Generating this week's product briefs..."
  python3 tools/children_brief_generator.py
  python3 tools/productivity_brief_generator.py

  echo ""
  echo "[2/7] Researching products (Tavily)..."
  python3 tools/research_products.py

  echo ""
  echo "[3/7] Drafting newsletter (Groq)..."
  python3 tools/draft_newsletter.py

  echo ""
  echo "[4/7] Formatting HTML email..."
  python3 tools/format_email.py

  echo ""
  echo "[5/7] Sending email..."
  python3 tools/send_email.py $DRY_RUN

  echo ""
  echo "[6/7] Logging to Google Sheets..."
  python3 tools/log_to_sheets.py

  if [[ -z "$DRY_RUN" ]]; then
    echo ""
    echo "[7/7] Advancing week counter..."
    python3 tools/advance_week.py
  else
    echo ""
    echo "[7/7] Skipping week advance (dry run)"
  fi

  echo ""
  echo "================================================"
  echo "DONE: $(date)"
  echo "================================================"

} 2>&1 | tee "$LOG_FILE"

# On dry-run, open previews directly in the browser so you can review without clicking links
if [[ -n "$DRY_RUN" ]] && command -v open &>/dev/null; then
  open "$SCRIPT_DIR/docs/current_brief.html"
  open "$SCRIPT_DIR/docs/current_productivity_brief.html"
  open "$SCRIPT_DIR/.tmp/formatted_email.html"
fi
