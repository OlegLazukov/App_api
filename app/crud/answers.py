from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.answer import Answer

def create_answer(db: Session, question_id: int, user_id: str, text: str) -> Answer:
    ans = Answer(question_id=question_id, user_id=user_id.strip(), text=text.strip())
    db.add(ans)
    db.commit()
    db.refresh(ans)
    return ans

def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    stmt = select(Answer).where(Answer.id == answer_id)
    return db.execute(stmt).scalar_one_or_none()

def delete_answer(db: Session, answer_id: int) -> bool:
    stmt = delete(Answer).where(Answer.id == answer_id)
    res = db.execute(stmt)
    db.commit()
    return res.rowcount > 0
