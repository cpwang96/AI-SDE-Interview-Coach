# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Home   │  │CodingSession │  │ SystemDesign  │  │
│  │(question │  │(Monaco+Chat) │  │   (Chat)      │  │
│  │ picker)  │  │              │  │               │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
│                       │                              │
│              Vite proxy /api/*                        │
└───────────────────────┼─────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────┐
│               Backend (FastAPI)                      │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐    │
│  │              API Routers                     │    │
│  │  /api/coding  /api/system-design  /api/exec  │    │
│  │  /api/users   /api/assessment                │    │
│  └────────────────────┼────────────────────────┘    │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐    │
│  │              Services                        │    │
│  │  ai_coach.py     code_runner.py              │    │
│  │  question_bank.py  user_service.py           │    │
│  │  assessment.py   session_store.py            │    │
│  └────────────────────┼────────────────────────┘    │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐    │
│  │           Data Layer (Local JSON)            │    │
│  │  data/coding_questions.json                  │    │
│  │  data/users/{user_id}.json                   │    │
│  │  data/sessions/{date}_{topic}.json           │    │
│  │  data/assessments/{user_id}.json             │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │           External: Claude API               │    │
│  │  - Coding coach (Socratic hints, review)     │    │
│  │  - System design interviewer                 │    │
│  │  - Assessment & study plan generation        │    │
│  │  - User profile analysis                     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## User Flow

### First-Time User
1. Land on Home → prompted to create profile
2. Optionally upload resume or provide LinkedIn URL
3. Claude analyzes background and tailors experience
4. **Assessment phase**: Claude presents 5-8 problems across topics/difficulties
5. Based on results, Claude generates a personalized study plan
6. Study plan persisted locally for future sessions

### Returning User
1. Land on Home → sees their study plan + progress
2. Pick a recommended problem or browse freely
3. All session data persisted for continuity

## Data Persistence (MVP)

Using local JSON files under `backend/data/`:

```
data/
├── coding_questions.json       # Static question bank
├── users/
│   └── {user_id}.json          # Profile, resume text, skills
├── assessments/
│   └── {user_id}.json          # Assessment results, skill levels
└── sessions/
    └── {user_id}/
        └── {date}_{question_id}.json   # Code, chat history, outcome
```

### Why Local JSON (not DB)?
- MVP simplicity — single user, no deployment
- Easy to inspect, version control, share with Claude
- Migration path to PostgreSQL is straightforward when needed

## API Design

### Users
- `POST /api/users/profile` — Create/update user profile
- `GET /api/users/profile/{user_id}` — Get user profile
- `POST /api/users/upload-resume` — Upload resume for analysis

### Assessment
- `POST /api/assessment/start` — Begin skill assessment
- `POST /api/assessment/submit` — Submit answer for a problem
- `GET /api/assessment/results/{user_id}` — Get assessment results + study plan

### Coding
- `GET /api/coding/questions` — List questions (filterable)
- `POST /api/coding/start` — Start a coding session
- `POST /api/coding/chat` — Chat with coach during session

### System Design
- `GET /api/system-design/topics` — List topics
- `POST /api/system-design/start` — Start a session
- `POST /api/system-design/chat` — Chat with coach

### Execution
- `POST /api/execute/run` — Execute code

## Key Design Decisions

1. **Local code execution via subprocess** — No Docker/Judge0 dependency for MVP. Supports Python and JavaScript. Sandboxed with timeout.
2. **Claude Sonnet for coaching** — Good balance of speed and quality for interactive sessions. Can upgrade to Opus for deeper analysis.
3. **Session-based AI memory** — Each interview session maintains full conversation history. Cross-session learning via persisted assessments.
4. **Vite proxy** — Frontend dev server proxies API calls, avoiding CORS complexity in development.

## Future Architecture Changes
- PostgreSQL for multi-user data
- WebSocket for streaming AI responses
- Judge0 Docker container for more languages + true sandboxing
- Excalidraw integration for system design diagrams
- OAuth for user auth
