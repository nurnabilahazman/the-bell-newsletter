#!/bin/bash
# Serve the LinkedIn research brief — one link, works on WiFi and mobile data.
# Same setup as Bell Assistant. Tailscale must be open on iPhone to access remotely.
#
# Usage: bash serve_brief.sh

PORT=8083
BRIEF_FILE="linkedin_research_brief.html"
TMP_DIR=".tmp"
TAILSCALE_IP="100.68.229.47"

# Kill anything already on PORT
lsof -ti:"${PORT}" | xargs kill -9 2>/dev/null
sleep 0.3

# Start HTTP server on all interfaces (so Tailscale can reach it)
cd "${TMP_DIR}" && python3 -m http.server "${PORT}" --bind 0.0.0.0 > /dev/null 2>&1 &
SERVER_PID=$!
cd ..
sleep 0.8

if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
  echo "ERROR: Server failed to start on port ${PORT}."
  exit 1
fi

# Check Tailscale status
if /Applications/Tailscale.app/Contents/MacOS/Tailscale status &>/dev/null; then
  TS_STATUS="connected ✓"
else
  TS_STATUS="not connected — open Tailscale on Mac first"
fi

LINK="http://${TAILSCALE_IP}:${PORT}/${BRIEF_FILE}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  THE BELL — Research Brief"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  → ${LINK}"
echo ""
echo "  Tailscale: ${TS_STATUS}"
echo "  Open Tailscale on iPhone, then open the link above."
echo "  Works on WiFi and mobile data."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Press Ctrl+C to stop."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

open "http://localhost:${PORT}/${BRIEF_FILE}" 2>/dev/null

trap "kill ${SERVER_PID} 2>/dev/null; echo ''; echo 'Server stopped.'; exit 0" INT TERM
wait "${SERVER_PID}"
