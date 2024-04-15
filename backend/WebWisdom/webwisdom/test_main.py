from fastapi.testclient import TestClient
from .main import app 
from .database.database import Base
from .routers.auth import get_db


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest


# in memory DB that is deleted when test is done
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    
def test_create_user():
    response = client.post(
        "/auth/register",
        json={"username": "test@test.com",
              "password": "123Rock123???"},
    )
    assert response.is_success