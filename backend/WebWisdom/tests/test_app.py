from fastapi.testclient import TestClient

from ..webwisdom.main import app


client = TestClient(app)

def test_get():
    response = client.get("/")
    assert response.status_code == 200
