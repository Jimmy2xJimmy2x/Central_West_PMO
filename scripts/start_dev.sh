#!/bin/bash
# Start both Flask and Vite dev servers

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Starting Central West PMO dev servers..."

# Start Flask in background
echo "Starting Flask API server on port 5000..."
cd "$PROJECT_ROOT"
source venv/bin/activate
python3 -m api.app &
FLASK_PID=$!

# Start Vite dev server
echo "Starting Vite dev server..."
cd "$PROJECT_ROOT/web"
npm run dev &
VITE_PID=$!

echo ""
echo "✓ Flask API: http://localhost:5000"
echo "✓ React app: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $FLASK_PID $VITE_PID 2>/dev/null; exit" INT
wait
