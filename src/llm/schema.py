from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict

class ExtractedTask(BaseModel):
    title : str = Field(min_length=1)
    done : bool

    model_config = ConfigDict(strict=True, extra="forbid")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        if not value.strip():
            raise ValueError("Title cannot be empty")

        return value

class ExtractTasksResponse(BaseModel):
    tasks : list[ExtractedTask]
    model_config = ConfigDict(strict=True, extra="forbid")