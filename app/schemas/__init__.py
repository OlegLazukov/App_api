from .question import QuestionCreate, QuestionOut, QuestionWithAnswers
from .answer import AnswerCreate, AnswerOut

# Optional: resolve forward refs at runtime (helps Pydantic v2)
try:
    QuestionWithAnswers.model_rebuild()
except Exception:
    pass
