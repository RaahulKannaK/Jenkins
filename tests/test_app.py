import app as application

def test_home_returns_successful_response():
    client = application.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["application"] == "Jenkins CI/CD Demo"
    assert payload["status"] == "running"

def test_health_endpoint():
    client = application.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}
