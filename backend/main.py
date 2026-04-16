from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import coding, system_design, execute, users, assessment, study_plans

load_dotenv()

app = FastAPI(title="Interview Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coding.router, prefix="/api/coding", tags=["coding"])
app.include_router(system_design.router, prefix="/api/system-design", tags=["system-design"])
app.include_router(execute.router, prefix="/api/execute", tags=["execute"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["assessment"])
app.include_router(study_plans.router, prefix="/api/study", tags=["study-plans"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
