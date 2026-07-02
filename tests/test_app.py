from app.app import app

def test_home_page():
    client = app.test_client()

    response = client.get("/r")

    assert response.status_code == 200