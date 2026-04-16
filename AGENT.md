# AGENT.md — Claude Development Context

## Project: AI SDE Interview Coach
**Repo**: https://github.com/cpwang96/AI-SDE-Interview-Coach
**Owner**: chuping (cpwang96)

## Current Status
- **Phase**: MVP Development
- **Backend**: FastAPI — running, routes for coding/system-design/execute/users/assessment
- **Frontend**: React + Vite + TypeScript — scaffolded, needs `npm install` after Node.js setup
- **Code Execution**: Local subprocess (Python, JS) — no Docker needed yet
- **Data Storage**: Local JSON files under `backend/data/`
- **AI Model**: Claude Sonnet for coaching sessions

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for full system design.

Key files:
- `backend/main.py` — FastAPI app entry
- `backend/services/ai_coach.py` — Claude API integration, system prompts
- `backend/services/code_runner.py` — Subprocess code execution
- `backend/services/question_bank.py` — Question loading/filtering
- `backend/services/user_service.py` — User profile management
- `backend/services/assessment.py` — Skill assessment logic
- `backend/services/session_store.py` — Session persistence
- `frontend/src/pages/` — Main page components
- `frontend/src/components/` — Reusable UI components

## Development Commands
```bash
# Start everything
./start.sh

# Backend only
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Frontend only
cd frontend && npm run dev
```

## What's Done
- [x] FastAPI backend with CORS, routing
- [x] Claude API integration with coaching prompts (coding + system design)
- [x] Local code execution (Python/JS with timeout)
- [x] Question bank (6 problems: easy/medium/hard)
- [x] React frontend with Monaco editor, chat panel, routing
- [x] User profile system (create, resume upload, LinkedIn)
- [x] Skill assessment flow (test → evaluate → study plan)
- [x] Session persistence (saves all coding sessions locally)
- [x] Startup script

## What's Next
- [ ] Install Node.js and test frontend end-to-end
- [ ] Add more questions to the bank
- [ ] Streaming AI responses (WebSocket)
- [ ] Behavioral question module
- [ ] Resume deep-dive simulation
- [ ] Progress tracking dashboard
- [ ] Excalidraw for system design diagrams
- [ ] Company-specific question sets

## Conventions
- Backend: Python 3.9+, FastAPI, Pydantic models
- Frontend: React 18, TypeScript, inline styles (no CSS framework yet)
- Data: JSON files under `backend/data/` — inspect directly for debugging
- AI prompts: Defined in `backend/services/ai_coach.py`
