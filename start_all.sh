#!/bin/bash
# Start all 5 Bell tools at once
# Usage: bash start_all.sh

BASE="/Users/nabilahazman/Documents/coding money project/Section 1_Project of the Week"

echo ""
echo "  The Bell — Starting all tools"
echo "  ─────────────────────────────────────────────"
echo ""

# Kill anything already running on these ports
for PORT in 5001 5002 5003 5004; do
  lsof -ti:$PORT | xargs kill -9 2>/dev/null
done

sleep 1

cd "$BASE/Week 1_Excel Formula Generator" && python3 app.py &
cd "$BASE/Week 2_Job Calculator" && python3 app.py &
cd "$BASE/Week 3_Summary Generator" && python3 app.py &
cd "$BASE/Week 4_CV Optimizer" && python3 app.py &

sleep 2

echo ""
echo "  All tools running:"
echo "  ─────────────────────────────────────────────"
echo "  Week 1 — Excel Formula Generator:  http://localhost:5001"
echo "  Week 2 — Job Calculator:           http://localhost:5002"
echo "  Week 3 — Summary Generator:        http://localhost:5003"
echo "  Week 4 — CV Optimizer:             http://localhost:5004"
echo ""
echo "  Tailscale:"
echo "  Week 1:  http://100.68.229.47:5001"
echo "  Week 2:  http://100.68.229.47:5002"
echo "  Week 3:  http://100.68.229.47:5003"
echo "  Week 4:  http://100.68.229.47:5004"
echo ""
echo "  Press Ctrl+C to stop all."
echo ""

wait
