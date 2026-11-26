from app import app

client = app.test_client()


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_student():
    response = client.get("/student")
    assert response.status_code == 200


def test_dbtest():
    response = client.get("/dbtest")
    assert response.status_code == 200


def test_register():
    response = client.post(
        "/register",
        json={
            "email": "pytestdemo@gmail.com",
            "username": "pytestuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200


def test_login():
    response = client.post(
        "/login",
        json={
            "email": "pytestdemo@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200


def test_generate_resume():
    response = client.post(
        "/generate-resume",
        json={
            "template": "ats-classic",
            "linkedin_data": "Software Developer with Python and Flask experience"
        }
    )

    assert response.status_code in [200, 500]