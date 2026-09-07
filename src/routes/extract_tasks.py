import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import ExtractTasksRequest
from src.llm.schema import ExtractTasksResponse
from src.llm.client import extract_tasks_with_llm

router = APIRouter()

@router.post("/extract_tasks")
def extract_tasks(request:ExtractTasksRequest):

    llm_stub = os.getenv("LLM_STUB", "0") == "1"

    if llm_stub:
        response = {
        "tasks": [
            {"title": "Water plants", "done": True},
            {"title": "Feed cat", "done": False}
        ]
    } 
        return response

    return extract_tasks_with_llm(request.text)

