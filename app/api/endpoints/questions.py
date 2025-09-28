from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.db.session import SessionLocal
from app.schemas import QuestionCreate, QuestionOut, QuestionWithAnswers
from app.models.question import Question

router = APIRouter(prefix="/questions", tags=["questions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    stmt = select(Question).order_by(Question.created_at.desc())
    questions = db.execute(stmt).scalars().all()
    return questions

@router.post("/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Question text must not be empty")
    q = Question(text=text)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.get("/{question_id}", response_model=QuestionWithAnswers)
def get_question(question_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Question)
        .options(joinedload(Question.answers))
        .where(Question.id == question_id)
    )
    q = db.execute(stmt).unique().scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
    return
