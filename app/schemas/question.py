from datetime import datetime
from pydantic import BaseModel, Field

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1)

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True

class QuestionWithAnswers(QuestionOut):
    answers: list["AnswerOut"] = []  # forward ref
