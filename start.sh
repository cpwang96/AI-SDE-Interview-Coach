#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== AI SDE Interview Coach ===${NC}"
echo ""

# --- Check prerequisites ---
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi
echo "  python3: $(python3 --version)"

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}node not found. Please install Node.js (brew install node)${NC}"
    exit 1
fi
echo "  node: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm not found. Please install Node.js${NC}"
    exit 1
fi
echo "  npm: $(npm --version)"

# --- Check .env ---
if [ ! -f "$BACKEND_DIR/.env" ]; then
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        echo ""
        echo -e "${RED}Created backend/.env from .env.example${NC}"
        echo -e "${RED}Please edit backend/.env and add your ANTHROPIC_API_KEY${NC}"
        echo -e "${RED}Then run this script again.${NC}"
        exit 1
    fi
fi

# --- Setup backend ---
echo ""
echo -e "${YELLOW}Setting up backend...${NC}"

if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"

echo "  Installing dependencies..."
pip install -q -r "$BACKEND_DIR/requirements.txt" 2>/dev/null

# --- Setup frontend ---
echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "  Installing npm packages..."
    cd "$FRONTEND_DIR" && npm install --silent 2>/dev/null
fi

# --- Start services ---
echo ""
echo -e "${GREEN}Starting services...${NC}"

# Start backend in background
echo "  Starting backend on http://localhost:8000..."
cd "$BACKEND_DIR"
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend in background
echo "  Starting frontend on http://localhost:5173..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

# Trap to kill both on exit
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
echo -e "${GREEN}  Frontend: http://localhost:5173${NC}"
echo -e "${GREEN}  Backend:  http://localhost:8000${NC}"
echo -e "${GREEN}  API docs: http://localhost:8000/docs${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "Press Ctrl+C to stop"

# Wait for both
wait
