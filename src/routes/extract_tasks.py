import os
import json
from pydantic import ValidationError
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import ExtractTasksRequest
from src.llm.schema import ExtractTasksResponse
from src.llm.llm_service import extract_validated_tasks
from openai import APITimeoutError, APIStatusError

router = APIRouter()

@router.post("/extract_tasks", response_model=ExtractTasksResponse)
def extract_tasks(request:ExtractTasksRequest):

    llm_enabled = os.getenv("LLM_ENABLED", "true").strip().lower() == "true"

    if not llm_enabled:
        return JSONResponse(
            status_code=503,
            content={"error": "Task extraction is currently disabled."},
        )

    llm_stub = os.getenv("LLM_STUB", "0") == "1"

    if llm_stub:
        response = {
        "tasks": [
            {"title": "Water plants", "done": True},
            {"title": "Feed cat", "done": False}
        ]
    } 
        return response

    try:
        return extract_validated_tasks(request.text)
    except (json.JSONDecodeError, ValidationError):
        return JSONResponse(
                status_code=422,
                content={"error": "Could not produce valid task data after one repair attempt."}
            )
    except APITimeoutError:
        return JSONResponse(
            status_code=504,
            content={"error": "The model service took too long to respond."},
        )
    except APIStatusError as error:
        if error.status_code == 429 or 500 <= error.status_code < 600:
            return JSONResponse(
                status_code=503,
                content={
                    "error": "The model service is temporarily unavailable."
                },
            )

        return JSONResponse(
            status_code=502,
            content={
                "error": "The model service could not complete the request."
            },
        )


