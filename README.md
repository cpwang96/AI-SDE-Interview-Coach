# AI SDE Interview Coach

An AI-powered interview preparation tool that provides personalized coding and system design practice with real-time coaching from Claude.

## Why This Exists

LeetCode Premium isn't customized enough. This tool adapts to **your** skill level, gives Socratic hints instead of answers, and builds a personalized study plan — like having a senior engineer mock-interview you on demand.

## Features

### Coding Practice
- **79 Blind 75 problems** (complete set + 4 bonus) across easy / medium / hard
- **LeetCode-style two-column layout** — problem statement + output on the left, full-height Monaco editor on the right, drag to resize
- **Monaco editor** (VS Code engine) with Java, Python, and JavaScript support; JetBrains Mono font, bracket colorization, smooth cursor
- **Submit = run against all test cases** — PASS / FAIL per test with input / expected / actual output
- **Compilation error banner** — red ⚠️ header when Java / Python fails to compile, before the raw stderr
- **Interview timer** — countdown with 20 / 30 / 45 / 60 min presets; turns yellow < 10 min, red < 5 min; pauses on solve; records elapsed time
- **Next Question button** — picks a random question at the same difficulty; also shown in the result banner on pass
- **AI Coach** — open on demand via flyout panel; ask for Socratic hints, discuss approach, get code reviews; never auto-triggers
- **Filter by** difficulty, algorithm, company, frequency, and category
- **Category pills** — one-click filter row (Arrays, Trees, DP, Graphs, …) above the question list
- **Dynamic question generation** — Claude generates new problems on any topic / difficulty
- Last submitted code reloads automatically when reopening a question

### Study Plans
- **Blind 75 — 4 Week Sprint** (2 problems/day, topic-ordered)
- **Algorithm Patterns — 6 Week Deep Dive** (pattern-focused, 2/day)
- **Quick Start — 2 Week Crash Course** (3/day, highest-frequency problems first)
- **Today's Mission card** — highlights today's problems at the top with a "Solve →" CTA; turns green when all done
- **Streak tracking** 🔥 — consecutive days with at least one problem marked done; resets if you skip a day
- **On-track / behind status** — tells you exactly how many problems from past days are still incomplete
- **Color-coded timeline** — ✅ done · 🔶 partial · 🔴 overdue · ▶ today (blue accent border) · ○ future
- **Auto-marks complete on passing submit** — solve from the study plan → all tests pass → checkbox ticks automatically
- **Toggle completion** — click a checked box to unmark it (marking done advances streak; unmarking does not)
- **Back to study plan** button in the coding UI when coming from a plan
- **Overdue catch-up banner** — yellow / red alert with count of missed problems
- Plan completion 🎉 screen when all problems are solved

### Progress Tracking
- Submission history persisted per user (code, language, pass rate, timestamp)
- Green ✓ on homepage for solved questions
- Study plan progress with per-week / per-day completion counts and a gradient progress bar
- Streak + day-number shown prominently in the plan motivation bar

### System Design
- Interactive mock interviews with Claude as the interviewer
- 10 design topics (URL Shortener, Chat App, News Feed, etc.)

### Assessment & Profiles
- 6-problem skill diagnostic; Claude scores and generates a personalized study plan
- User profiles with resume / LinkedIn for personalized coaching

## Prerequisites

- **Python 3.9+** — `python3 --version`
- **Node.js 18+** — `node --version` (install: `brew install node`)
- **Anthropic API key** — [Get one here](https://console.anthropic.com/) (coding/submit works without credits; AI coaching requires credits)
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

1. **Pick a study plan** or browse / filter questions from the homepage
2. **Click Today's Mission** to jump straight to today's problems
3. **Write your solution** in the Monaco editor (Java, Python, or JavaScript)
4. **Run** to test with sample inputs; **Submit** to run all test cases
5. **Ask the coach** for hints, discuss approach, or get a code review
6. Track your streak and daily progress from the study plan page

## Project Structure

```
├── start.sh                        # One-command startup
├── backend/
│   ├── main.py                     # FastAPI entry point
│   ├── data/
│   │   ├── coding_questions.json   # 79 Blind 75 problems with test cases
│   │   ├── study_plans.json        # 3 structured study plans
│   │   ├── generated/              # AI-generated questions
│   │   ├── submissions/            # Submission history per user
│   │   ├── progress/               # Study plan progress (streak, start date, completed)
│   │   ├── users/                  # User profiles (JSON)
│   │   ├── sessions/               # Saved coding sessions
│   │   └── assessments/            # Skill assessment results
│   ├── routers/
│   │   ├── coding.py               # Questions, submit, chat, filters
│   │   ├── study_plans.py          # Plans, progress, streak, start/complete toggle
│   │   ├── system_design.py        # System design sessions
│   │   ├── execute.py              # Code execution endpoint
│   │   ├── users.py                # User profiles
│   │   └── assessment.py           # Skill assessment
│   └── services/
│       ├── ai_coach.py             # Claude API + coaching prompts
│       ├── code_runner.py          # Subprocess execution (Python / JS / Java)
│       ├── question_bank.py        # Question loading / filtering
│       ├── question_generator.py   # Claude-powered question generation
│       └── submission_store.py     # Submission history persistence
└── frontend/
    └── src/
        ├── api/client.ts           # All API functions
        ├── pages/
        │   ├── Home.tsx            # Question browser, category pills, solved status
        │   ├── CodingSession.tsx   # Editor + timer + submit + coach flyout
        │   ├── StudyPlan.tsx       # Plans, streak, today's mission, timeline
        │   ├── Assessment.tsx      # Skill diagnostic
        │   ├── SystemDesignSession.tsx
        │   └── Onboarding.tsx      # Profile setup
        └── components/
            ├── CodeEditor.tsx      # Monaco wrapper + language switching
            └── ChatPanel.tsx       # Chat with markdown rendering
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React + Vite + TypeScript | Fast dev, type safety |
| Code Editor | Monaco Editor | Same engine as VS Code |
| Backend | FastAPI (Python 3.9) | Async, auto-docs at `/docs` |
| AI | Claude API (Anthropic) | Best reasoning for code review |
| Code Execution | subprocess + timeout | Python, JS, Java — no Docker needed |
| Storage | Local JSON files | Easy to inspect, zero setup |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/coding/questions` | List questions (filterable by difficulty, topic, company, category) |
| GET | `/api/coding/filters` | Get filter option lists |
| GET | `/api/coding/solved` | Get solved question IDs |
| POST | `/api/coding/start` | Start a coding session |
| POST | `/api/coding/submit` | Submit + run all test cases |
| POST | `/api/coding/chat` | Chat with AI coach |
| POST | `/api/coding/generate` | Generate new question via AI |
| GET | `/api/study/plans` | List study plans |
| GET | `/api/study/plans/{id}` | Get plan with weekly schedule |
| GET | `/api/study/plans/{id}/progress` | Get progress + computed stats (streak, today's day, on-track status) |
| POST | `/api/study/plans/{id}/start` | Record plan start date (idempotent) |
| POST | `/api/study/plans/{id}/complete` | Toggle question done / undone + update streak |
| POST | `/api/execute/run` | Run code without test cases |

## License

MIT
