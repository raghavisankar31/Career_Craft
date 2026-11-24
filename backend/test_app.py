from app import app

def test_home():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    assert b"Backend Running Successfully" in response.data


def test_student():

    client = app.test_client()

    response = client.get("/student")

    assert response.status_code == 200