from pydantic import BaseModel, field_validator
import datetime

    
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    board_id: int
    author_id: int
    created_at: datetime.datetime

class PostCreate(BaseModel):
    title: str
    content: str
    board_id: int

    @field_validator('title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('title is needed')
        return v
    
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('content is needed')
        return v
    
    @field_validator('board_id')
    def validate_board_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('board_id must be a positive integer.')
        return v
    