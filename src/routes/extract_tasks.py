import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import ExtractTasksRequest
from src.llm.schema import ExtractTasksResponse

router = APIRouter()

@router.post("/extract_tasks", response_model=ExtractTasksResponse)
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

    return JSONResponse(
                            status_code=503,
                            content={"message":"Not yet implemented"}
                        )

