from typing import Sequence, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.question import Question

def list_questions(db: Session) -> Sequence[Question]:
    stmt = select(Question).order_by(Question.created_at.desc())
    return db.execute(stmt).scalars().all()

def create_question(db: Session, text: str) -> Question:
    q = Question(text=text.strip())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

def get_question(db: Session, question_id: int) -> Optional[Question]:
    stmt = select(Question).where(Question.id == question_id)
    return db.execute(stmt).scalar_one_or_none()

def delete_question(db: Session, question_id: int) -> bool:
    stmt = delete(Question).where(Question.id == question_id)
    res = db.execute(stmt)
    db.commit()
    return res.rowcount > 0
