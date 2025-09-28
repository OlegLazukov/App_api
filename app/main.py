from fastapi import FastAPI
from app.api.endpoints import questions as questions_router
from app.api.endpoints import answers as answers_router
from app.core.logging_config import setup_logging

setup_logging()
app = FastAPI(title="Q&A API", version="1.0.0")

app.include_router(questions_router.router)
app.include_router(answers_router.router)
