from pydantic import BaseModel

class NewTask(BaseModel):
    title: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None

class AuthCredentials(BaseModel):
    email: str | None = None
    password: str | None = None