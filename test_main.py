from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test():
	response = client.get("/weather/summary")
	assert response.status_code == 	200
	data = response.json()
	assert isinstance(data, list) 
	if len(data) > 0:
		assert "According to the Analysis" in data[0]["analysis"]
		assert "total_students" in data[0]
		assert isinstance(data[0]["total_students"], int)