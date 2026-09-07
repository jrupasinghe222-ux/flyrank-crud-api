from pydantic import BaseModel, Field, field_validator

class ExtractedTask(BaseModel):
    title : str = Field(min_length=1)
    done : bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        if not value.strip():
            raise ValueError("Title cannot be empty")

        return value

class ExtractTasksResponse(BaseModel):
    tasks : list[ExtractedTask]