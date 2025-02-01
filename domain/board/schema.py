from pydantic import BaseModel, field_validator

class BoardResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    
class BoardCreate(BaseModel):
    name: str
    description: str | None = None

    @field_validator('name')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('name is needed')
        return v