import json


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass",
    }
    response = client.post("/users/", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["is_active"] == True
