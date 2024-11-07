from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_main_endpoint_integration():
    """
    Test the `/usage` endpoint of the FastAPI app.
    Ensures the route is correctly integrated and responds.
    """
    response = client.get("/usage")
    # Assuming the API works correctly, it should return 200.
    # If dependencies are mocked properly, this can return the mocked data.
    assert response.status_code == 200
    assert "usage" in response.json()