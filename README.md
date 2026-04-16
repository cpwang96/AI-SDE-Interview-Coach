# AI SDE Interview Coach

An AI-powered interview preparation tool that provides personalized coding and system design practice with real-time coaching from Claude.

## Why This Exists

Leetcode Premium isn't customized enough. This tool adapts to **your** skill level, gives Socratic hints instead of answers, and builds a personalized study plan — like having a senior engineer mock-interview you on demand.

## Features

### Current (MVP)
- **Skill Assessment** — On first run, Claude tests your coding ability across topics and difficulty levels to establish a baseline
- **Coding Questions** — Monaco editor (VS Code engine) with syntax highlighting, code execution, and AI coaching
- **System Design** — Interactive design discussions with follow-up questions and feedback
- **User Profiles** — Resume/LinkedIn-based profile so Claude understands your background
- **Problem Persistence** — All generated problems and daily study plans saved locally for review
- **AI Coach** — Socratic method hints, complexity analysis, approach review, follow-up questions

### Planned
- Behavioral question practice (STAR method coaching)
- Resume deep-dive simulation
- Company-specific preparation
- Progress tracking and analytics
- Spaced repetition for weak topics

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + TypeScript |
| Code Editor | Monaco Editor |
| Backend | FastAPI (Python) |
| AI | Claude API (Anthropic) |
| Code Execution | Local subprocess (Python, JavaScript) |
| Storage | Local JSON files (MVP) → PostgreSQL (later) |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/cpwang96/AI-SDE-Interview-Coach.git
cd AI-SDE-Interview-Coach

# 2. Set up your API key
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# 3. Run everything
./start.sh
```

### Manual Start

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Project Structure

```
├── AGENT.md                    # Claude context for development
├── ARCHITECTURE.md             # System design and architecture
├── start.sh                    # One-command startup
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── data/
│   │   ├── coding_questions.json   # Question bank
│   │   ├── users/              # User profiles
│   │   └── sessions/           # Persisted study sessions
│   ├── models/                 # Pydantic schemas
│   ├── routers/                # API endpoints
│   └── services/               # Business logic + AI
└── frontend/
    └── src/
        ├── pages/              # Home, Coding, SystemDesign
        ├── components/         # Editor, Chat, etc.
        └── api/                # API client
```

## License

MIT
