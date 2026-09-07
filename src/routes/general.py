from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", summary="Show API information")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /public/info",
            "GET /tasks",
            "GET /tasks/{id}",
            "POST /tasks",
            "PUT /tasks/{id}",
            "DELETE /tasks/{id}",
            "POST /extract_tasks",
            "POST /auth/signup",
            "POST /auth/login",
            "POST /auth/logout",
            "GET /protected/profile",
            "GET /protected/dashboard",
        ],
    }

@router.get("/health",summary="Check API health")
def health_check():
    return { "status": "ok" }


@router.get("/public/info")
def info():
    return JSONResponse(
            status_code=200,
            content={"message": "Welcome stranger! This info is public."}
        )
