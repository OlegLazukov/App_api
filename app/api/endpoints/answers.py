from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas import AnswerCreate, AnswerOut
from app.models.question import Question
from app.models.answer import Answer

router = APIRouter(prefix="/answers", tags=["answers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/questions/{question_id}/answers/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int, payload: AnswerCreate, db: Session = Depends(get_db)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    text = payload.text.strip()
    user_id = payload.user_id.strip()
    if not text or not user_id:
        raise HTTPException(status_code=422, detail="user_id and text must not be empty")
    ans = Answer(question_id=question_id, user_id=user_id, text=text)
    db.add(ans)
    db.commit()
    db.refresh(ans)
    return ans

@router.get("/{answer_id}", response_model=AnswerOut)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    ans = db.get(Answer, answer_id)
    if not ans:
        raise HTTPException(status_code=404, detail="Answer not found")
    return ans

@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    ans = db.get(Answer, answer_id)
    if not ans:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(ans)
    db.commit()
    return
