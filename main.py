from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from src.exception_handlers import handle_request_validation

from src.routes.extract_tasks import router as extraction_router
from src.routes.tasks import router as tasks_router
from src.routes.auth import router as auth_router
from src.routes.protected import router as protected_router
from src.routes.general import router as general_router


app = FastAPI()

app.add_exception_handler(
    RequestValidationError,
    handle_request_validation,
)

app.include_router(extraction_router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(general_router)
