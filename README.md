# AI SDE Interview Coach

An AI-powered interview preparation tool that provides personalized coding and system design practice with real-time coaching from Claude.

## Why This Exists

Leetcode Premium isn't customized enough. This tool adapts to **your** skill level, gives Socratic hints instead of answers, and builds a personalized study plan — like having a senior engineer mock-interview you on demand.

## Features

### Coding Practice
- **79 Blind75 problems** (complete set + 4 bonus) across easy/medium/hard
- **Monaco editor** (VS Code engine) with Python, JavaScript, and Java support
- **Submit = run against test cases** — PASS/FAIL per test with input/expected/got output
- **Always-visible output panel** shows run results and submission status inline
- **AI Coach** — open on demand, ask for hints (Socratic method), discuss approach, get code reviews
- **Dynamic question generation** — Claude generates new problems based on your weak topics
- **Filter by** category (Array, Tree, DP, Graph…), difficulty, company, and frequency

### Study Plans
- **Blind 75 — 4 Week Sprint** (46 problems, 2/day)
- **Algorithm Patterns — 6 Week Deep Dive** (47 problems, pattern-focused)
- **Quick Start — 2 Week Crash Course** (34 problems, 3/day)
- Daily topic-focused practice with progress tracking and checkboxes

### Progress Tracking
- Submission history persisted (code, language, pass/fail, timestamp)
- Green checkmark on homepage for solved questions
- Last submitted code reloads when reopening a question
- Study plan progress with per-week completion tracking

### System Design
- Interactive mock interviews with Claude as the interviewer
- 10 design topics (URL Shortener, Chat App, News Feed, etc.)

### Assessment & Profiles
- 6-problem skill diagnostic, Claude scores and generates study plan
- User profiles with resume/LinkedIn for personalized coaching

## Prerequisites

- **Python 3.9+** — `python3 --version`
- **Node.js 18+** — `node --version` (install: `brew install node`)
- **Anthropic API key** — [Get one here](https://console.anthropic.com/) (app works without credits for coding/submit, but AI coaching requires credits)
- **Java JDK** (optional, for Java execution) — `brew install openjdk@21`

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

1. **Pick a study plan** or browse questions from the homepage
2. **Filter** by company, algorithm, difficulty, or frequency
3. **Write your solution** in the Monaco editor (Python, JavaScript, or Java)
4. **Run** to test with sample inputs, **Submit** to run against all test cases
5. **Ask the coach** for hints, discuss your approach, or get unstuck
6. Track your progress with solved checkmarks and study plan completion

## Project Structure

```
├── start.sh                        # One-command startup
├── backend/
│   ├── main.py                     # FastAPI entry point
│   ├── data/
│   │   ├── coding_questions.json   # 79 Blind75 problems with test cases
│   │   ├── study_plans.json        # 3 structured study plans
│   │   ├── generated/              # AI-generated questions
│   │   ├── submissions/            # Submission history per user
│   │   ├── progress/               # Study plan progress per user
│   │   ├── users/                  # User profiles (JSON)
│   │   ├── sessions/               # Saved coding sessions
│   │   └── assessments/            # Skill assessment results
│   ├── routers/
│   │   ├── coding.py               # Questions, submit, chat, filters
│   │   ├── study_plans.py          # Study plan CRUD + progress
│   │   ├── system_design.py        # System design sessions
│   │   ├── execute.py              # Code execution endpoint
│   │   ├── users.py                # User profiles
│   │   └── assessment.py           # Skill assessment
│   └── services/
│       ├── ai_coach.py             # Claude API + coaching prompts
│       ├── code_runner.py          # Subprocess execution (Python/JS/Java)
│       ├── question_bank.py        # Question loading/filtering
│       ├── question_generator.py   # Claude-powered question generation
│       └── submission_store.py     # Submission history persistence
└── frontend/
    └── src/
        ├── api/client.ts           # All API functions
        ├── pages/
        │   ├── Home.tsx            # Question browser + filters + solved status
        │   ├── CodingSession.tsx   # Editor + submit + coach chat
        │   ├── StudyPlan.tsx       # Study plan selection + daily progress
        │   ├── Assessment.tsx      # Skill diagnostic
        │   ├── SystemDesignSession.tsx
        │   └── Onboarding.tsx      # Profile setup
        └── components/
            ├── CodeEditor.tsx      # Monaco wrapper + language switching
            └── ChatPanel.tsx       # Chat with markdown rendering
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React + Vite + TypeScript | Fast dev, type safety |
| Code Editor | Monaco Editor | Same engine as VS Code |
| Backend | FastAPI (Python 3.9) | Async, auto-docs at /docs |
| AI | Claude API (Anthropic) | Best reasoning for code review |
| Code Execution | subprocess + timeout | Python, JS, Java — no Docker needed |
| Storage | Local JSON files | Easy to inspect, zero setup |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/coding/questions` | List questions (filterable) |
| GET | `/api/coding/filters` | Get filter options |
| GET | `/api/coding/solved` | Get solved question IDs |
| POST | `/api/coding/start` | Start coding session |
| POST | `/api/coding/submit` | Submit + run test cases |
| POST | `/api/coding/chat` | Chat with AI coach |
| POST | `/api/coding/generate` | Generate new question via AI |
| GET | `/api/study/plans` | List study plans |
| GET | `/api/study/plans/{id}` | Get plan with schedule |
| POST | `/api/study/plans/{id}/complete` | Mark question done |
| POST | `/api/execute/run` | Run code (no test cases) |

## License

MIT
