#This test file uses Flask's test client to simulate requests to the server and verify responses.
#To run these tests, use the command python -m pytest -v
import io
import pytest
from server import app
import server

#Mock object to replace the Gemini model during tests
class MockModel:
    def generate_content(self, inputs):
        class Response:
            text = "Mock nutritional information about the food item."
        return Response()
    

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_upload_image_route(client, monkeypatch):
    #Mock Gemimi generate_content
    def mock_generate_content(prompt):
        return MockModel()
    monkeypatch.setattr('server.model', MockModel())

 # Create a fake image file
    fake_image = (io.BytesIO(b"fake image bytes"), "test.jpg")

    #send POST request to /upload with the fake image
    response = client.post('/upload', data={'image': fake_image}, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "analysis" in json_data
    assert json_data["analysis"] == "Mock nutritional information about the food item."