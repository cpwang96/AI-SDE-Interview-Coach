# AI SDE Interview Coach

An AI-powered interview preparation tool that provides personalized coding and system design practice with real-time coaching from Claude.

## Why This Exists

Leetcode Premium isn't customized enough. This tool adapts to **your** skill level, gives Socratic hints instead of answers, and builds a personalized study plan — like having a senior engineer mock-interview you on demand.

## Features

### Working Now
- **Coding Questions** — Monaco editor (VS Code engine) with syntax highlighting, code execution, and AI coaching
  - 11 problems across easy/medium/hard (arrays, strings, linked lists, graphs, DP, etc.)
  - Run code directly in the browser (Python & JavaScript)
  - "Submit to Coach" — Claude reviews your code for correctness, complexity, edge cases
  - Chat with the AI coach — ask for hints (Socratic method), discuss approach, get follow-ups
- **System Design** — Interactive mock interviews with Claude as the interviewer
- **Skill Assessment** — 6-problem diagnostic test, Claude scores each solution and generates a 2-week study plan
- **User Profiles** — Optional resume/LinkedIn for personalized coaching

### Planned
- Behavioral question practice (STAR method coaching)
- Resume deep-dive simulation
- Company-specific preparation
- Progress tracking and analytics

## Prerequisites

- **Python 3.9+** — `python3 --version`
- **Node.js 18+** — `node --version` (install: `brew install node`)
- **Anthropic API key** — [Get one here](https://console.anthropic.com/)

## Quick Start

```bash
# 1. Clone
git clone https://github.com/cpwang96/AI-SDE-Interview-Coach.git
cd AI-SDE-Interview-Coach

# 2. Set your API key
cp backend/.env.example backend/.env
# Edit backend/.env → set ANTHROPIC_API_KEY=sk-ant-...

# 3. Run
./start.sh
```

The script installs all dependencies on first run, then starts both servers.
Open **http://localhost:5173** when you see "Interview Coach is running!"

### Manual Start (two terminals)

```bash
# Terminal 1 — Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

## How It Works

1. **Pick a problem** from the home page (or click "Random Question")
2. **Write your solution** in the Monaco editor — supports Python and JavaScript
3. **Run your code** to test against sample inputs
4. **Ask the coach** for hints, discuss your approach, or get unstuck
5. **Submit to Coach** for a full code review with complexity analysis

The AI coach uses the Socratic method — it nudges you toward the answer rather than giving it away, just like a real interviewer.

## Project Structure

```
├── start.sh                        # One-command startup
├── backend/
│   ├── main.py                     # FastAPI entry point
│   ├── data/
│   │   ├── coding_questions.json   # 11 problems with test cases
│   │   ├── users/                  # User profiles (JSON)
│   │   ├── sessions/               # Saved coding sessions
│   │   └── assessments/            # Skill assessment results
│   ├── routers/                    # API endpoints
│   └── services/
│       ├── ai_coach.py             # Claude API + coaching prompts
│       ├── code_runner.py          # Sandboxed code execution
│       └── question_bank.py        # Question loading/filtering
└── frontend/
    └── src/
        ├── pages/
        │   ├── Home.tsx            # Question picker + dashboard
        │   ├── CodingSession.tsx   # Editor + coach chat
        │   ├── Assessment.tsx      # Skill diagnostic
        │   └── Onboarding.tsx      # Profile setup
        └── components/
            ├── CodeEditor.tsx      # Monaco wrapper
            └── ChatPanel.tsx       # Chat with markdown
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React + Vite + TypeScript | Fast dev, type safety |
| Code Editor | Monaco Editor | Same engine as VS Code |
| Backend | FastAPI (Python) | Async, auto-docs at /docs |
| AI | Claude API | Best reasoning for code review |
| Code Execution | subprocess + timeout | Simple, no Docker needed |
| Storage | Local JSON | Easy to inspect, zero setup |

## License

MIT
