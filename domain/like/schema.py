from pydantic import BaseModel, field_validator
import datetime

    
class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime.datetime

class LikeCreate(BaseModel):
    post_id: int
    
    @field_validator('post_id')
    def validate_board_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('post_id must be a positive integer.')
        return v
    