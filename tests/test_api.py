from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.api.endpoints.questions import get_db as get_db_questions
from app.api.endpoints.answers import get_db as get_db_answers

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_questions] = override_get_db
app.dependency_overrides[get_db_answers] = override_get_db

client = TestClient(app)

def setup_module(_module):
    Base.metadata.create_all(bind=engine)

def teardown_module(_module):
    Base.metadata.drop_all(bind=engine)

def test_full_flow():
    resp = client.post("/questions/", json={"text": "Что такое FastAPI?"})
    assert resp.status_code == 201
    q = resp.json()
    qid = q["id"]

    resp = client.get("/questions/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    a1 = client.post(f"/answers/questions/{qid}/answers/", json={"user_id": "user-123", "text": "Современный веб-фреймворк."})
    a2 = client.post(f"/answers/questions/{qid}/answers/", json={"user_id": "user-123", "text": "Быстрый и удобный."})
    assert a1.status_code == 201 and a2.status_code == 201

    resp = client.get(f"/questions/{qid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == qid
    assert len(data["answers"]) == 2

    resp = client.delete(f"/questions/{qid}")
    assert resp.status_code == 204

    ans_id = a1.json()["id"]
    resp = client.get(f"/answers/{ans_id}")
    assert resp.status_code == 404
