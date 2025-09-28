from datetime import datetime
from pydantic import BaseModel, Field

class AnswerBase(BaseModel):
    user_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)

class AnswerCreate(AnswerBase):
    pass

class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
