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


# when running pytest -v -s add the s flag to see the print statements of tests that pass

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
    create_user = client.post(
        "/auth/register",
        json={"username": "test@test.com",
              "password": "123Rock123???"},
    )
    jwt_token = create_user.cookies.get("jwt_token")
    client.cookies.set(name="jwt_token",value=jwt_token)
    
    assert create_user.status_code == 200


def test_create_penetration_test_with_user_jwt():
  
    response = client.get("/api/test-parse")
    
    response_data = response.content.decode('utf-8')
     
    assert "testurl.com" in response_data
    

def test_retrieve_penetration_test_for_user():
    client.get("/api/test-parse")
    response = client.get("/auth/get-all-results")
    response_data = response.content.decode('utf-8')
    
    assert '"id":1' in response_data and '"id":2' in response_data
    assert '"user_id":1' in response_data
    assert '"user_id":2' not in response_data