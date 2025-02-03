from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

    
class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int
    parent_comment_id: int
    created_at: datetime.datetime

class CommentCreate(BaseModel):
    content: str
    post_id: int
    parent_comment_id: Optional[int] = None
    
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('content is needed')
        return v
    
    @field_validator('post_id')
    def validate_post_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('post_id must be a positive integer.')
        return v
    