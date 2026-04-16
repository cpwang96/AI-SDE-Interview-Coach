#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Ensure homebrew binaries are in PATH (macOS)
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== AI SDE Interview Coach ===${NC}"
echo ""

# --- Check prerequisites ---
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi
echo "  python3: $(python3 --version)"

if ! command -v node &> /dev/null; then
    echo -e "${RED}node not found. Install with: brew install node${NC}"
    exit 1
fi
echo "  node:    $(node --version)"
echo "  npm:     $(npm --version)"

# --- Check .env ---
if [ ! -f "$BACKEND_DIR/.env" ]; then
    cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    echo ""
    echo -e "${RED}Created backend/.env — please add your ANTHROPIC_API_KEY:${NC}"
    echo -e "${RED}  Edit: $BACKEND_DIR/.env${NC}"
    echo ""
    exit 1
fi

if grep -q "your-api-key-here" "$BACKEND_DIR/.env" 2>/dev/null; then
    echo ""
    echo -e "${RED}ANTHROPIC_API_KEY not set in backend/.env${NC}"
    echo -e "${RED}  Edit: $BACKEND_DIR/.env${NC}"
    echo ""
    exit 1
fi

# --- Setup backend ---
echo ""
echo -e "${YELLOW}Setting up backend...${NC}"

if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"
pip install -q -r "$BACKEND_DIR/requirements.txt" 2>/dev/null
echo "  Backend ready."

# --- Setup frontend ---
echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "  Installing npm packages (first run)..."
    cd "$FRONTEND_DIR" && npm install --silent 2>/dev/null
fi
echo "  Frontend ready."

# --- Start services ---
echo ""
echo -e "${GREEN}Starting services...${NC}"

cd "$BACKEND_DIR"
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd "$FRONTEND_DIR"
npx vite --port 5173 &
FRONTEND_PID=$!

cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}  Interview Coach is running!${NC}"
echo -e "${GREEN}  App:      http://localhost:5173${NC}"
echo -e "${GREEN}  API docs: http://localhost:8000/docs${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "Press Ctrl+C to stop"

wait
