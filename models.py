from pydantic import BaseModel, Field, field_validator

class NewTask(BaseModel):
    title: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None

class AuthCredentials(BaseModel):
    email: str | None = None
    password: str | None = None

class ExtractTasksRequest(BaseModel):
    text: str = Field(min_length=1,max_length=2000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):

        if not value.strip():
            raise ValueError("Input cannot be empty")

        return value
