# AGENT.md — Claude Development Context

## Project: AI SDE Interview Coach
**Repo**: https://github.com/cpwang96/AI-SDE-Interview-Coach
**Owner**: chuping (cpwang96)
**Primary language**: Java (user's interview language)

## Current Status (2026-04-15)
- **Phase**: MVP — coding practice is functional and usable
- **Backend**: FastAPI on port 8000 — all routers working
- **Frontend**: React + Vite + TypeScript on port 5173 — fully functional
- **Code Execution**: Local subprocess (Python, JS, Java) — Java requires JDK install
- **AI Coaching**: Works but requires Anthropic API credits (currently exhausted)
- **Data Storage**: Local JSON files under `backend/data/`

## Architecture

### Backend (Python 3.9, FastAPI)
- `backend/main.py` — App entry, registers all routers with CORS for localhost:5173
- `backend/routers/coding.py` — **Most critical file**: questions, submit, chat, filters, solved status
- `backend/routers/study_plans.py` — Study plan CRUD + progress tracking
- `backend/routers/system_design.py` — System design sessions
- `backend/routers/execute.py` — Raw code execution endpoint
- `backend/routers/users.py` — User profile management
- `backend/routers/assessment.py` — Skill assessment flow
- `backend/services/ai_coach.py` — Claude API integration, system prompts
- `backend/services/code_runner.py` — Subprocess execution with 10s timeout (Python/JS/Java)
- `backend/services/question_bank.py` — Question loading + filtering by difficulty/topic/company/frequency/category
- `backend/services/question_generator.py` — Claude-powered dynamic question generation
- `backend/services/submission_store.py` — Submission history (code + results + timestamps)

### Frontend (React 18, TypeScript, Vite)
- `frontend/src/App.tsx` — Routes: /, /coding, /study, /system-design, /assessment, /onboarding
- `frontend/src/api/client.ts` — All API functions
- `frontend/src/pages/Home.tsx` — Question browser with 4 filter dropdowns, solved checkmarks, Blind 75 header
- `frontend/src/pages/CodingSession.tsx` — Monaco editor + Submit/Run + coach chat + loads previous submission
- `frontend/src/pages/StudyPlan.tsx` — Plan selection + weekly/daily progress with checkboxes
- `frontend/src/components/CodeEditor.tsx` — Monaco wrapper, 3 languages (Python/JS/Java)
- `frontend/src/components/ChatPanel.tsx` — Chat with markdown rendering

### Data
- `backend/data/coding_questions.json` — 32 questions, 294 test cases, company/algorithm/frequency tags
- `backend/data/study_plans.json` — 3 plans (Blind75 4wk, Algo Patterns 6wk, Quick Start 2wk)
- `backend/data/submissions/` — Per-user submission history
- `backend/data/progress/` — Per-user study plan progress
- `backend/data/generated/` — AI-generated questions
- `backend/data/users/` — User profiles
- `backend/data/assessments/` — Assessment results

## Development Commands
```bash
# Start everything
./start.sh

# Backend only (must use venv — system python3 doesn't have uvicorn)
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Frontend only
cd frontend && npx vite

# Or use full node path if npm not in PATH
/opt/homebrew/bin/node node_modules/.bin/vite
```

## Key Design Decisions
1. **Submit = run against test cases** (like Leetcode), NOT "send to coach for review"
2. **Auto-generated test runners** from `test_cases` JSON — no hardcoded test code per question
3. **Graceful fallback** when Claude API has no credits — coding/submit still works, coaching shows fallback message
4. **Java must be supported** — user's primary interview language
5. **Questions should be dynamically generated** by Claude, not just a static bank
6. **Local JSON storage** — no database, easy to inspect/debug

## What's Done
- [x] 32 Blind75-style coding problems with Java/Python/JS starter code
- [x] 294 test cases with edge cases (8-12 per problem)
- [x] Submit with auto-generated test runners (PASS/FAIL output)
- [x] Filter by company, algorithm, difficulty, frequency
- [x] 3 structured study plans with daily topics and progress tracking
- [x] Submission history persistence + solved indicators on homepage
- [x] Previous submission code reloads when reopening a question
- [x] AI coaching (requires API credits)
- [x] Dynamic question generation (requires API credits)
- [x] System design mock interviews (requires API credits)
- [x] Skill assessment flow
- [x] User profiles

## What's Next
- [ ] Install Java JDK on dev machine (`brew install openjdk@21`)
- [ ] Add Anthropic API credits to enable AI features
- [ ] Expand question bank toward full 75 questions
- [ ] Streaming AI responses (WebSocket or SSE)
- [ ] Behavioral question module
- [ ] Resume deep-dive simulation
- [ ] Progress analytics dashboard
- [ ] Company-specific question sets
- [ ] Excalidraw integration for system design diagrams

## Known Issues
- Java execution requires JDK installed locally (`brew install openjdk@21`)
- Anthropic API account has no credits — AI coaching/generation returns fallback messages
- Python 3.9 on this machine — can't use `dict | None` syntax, use `Optional[dict]`
- Node.js is at `/opt/homebrew/bin/` — may not be in PATH, start.sh exports it
