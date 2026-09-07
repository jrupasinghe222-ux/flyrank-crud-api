from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler


async def handle_request_validation(
    request: Request,
    exc: RequestValidationError,
):
    if request.method == "POST" and request.url.path == "/extract_tasks":
        errors = [
            {
                "field": ".".join(
                    str(part) for part in error["loc"] if part != "body"
                ) or "body",
                "message": error["msg"],
            }
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=400,
            content={"detail": errors},
        )

    return await request_validation_exception_handler(request, exc)