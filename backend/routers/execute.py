from fastapi import APIRouter
from models.schemas import ExecuteRequest, ExecuteResult
from services.code_runner import execute_code

router = APIRouter()


@router.post("/run", response_model=ExecuteResult)
def run_code(req: ExecuteRequest):
    result = execute_code(req.code, req.language)
    return result
