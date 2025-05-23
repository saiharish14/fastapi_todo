from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# your tests here...


def test_create_student_success():
    response = client.post("/students", json={
        "name": "Harish",
        "age": 19,
        "grade": "A"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Student added"


def test_get_all_students():
    response = client.get("/students")
    print("status code:", response.status_code)
    print("Respons JSON", response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_partial_student_update_student_success():
    # Ensure a student exists before partial update
    client.post("/students", json={
        "name": "TestUser",
        "age": 18,
        "grade": "B"
    })
    response = client.patch("/students/0", json={
        "age": 20
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Student partially updated"
    assert response.json()["data"]["age"] == 20
    print("status code:", response.status_code)
    print("response json", response.json())


def test_partial_update_invalid_id():
    response = client.patch("/students/999", json={"age": 30})
    assert response.status_code == 404
    assert "Student not found" in response.json()["detail"]
    print("status code", response.status_code)


def test_create_student_invalid_data():
    response = client.post("/students", json={
        "name": "bob"
    })
    assert response.status_code == 422
    print("status code:", response.status_code)
    print("response json:", response.json())


def test_patch_invalid_student_data():
    # Ensure a student exists before patching with invalid data
    client.post("/students", json={
        "name": "AnotherUser",
        "age": 22,
        "grade": "C"
    })
    response = client.patch("/students/1", json={
        "age": "twenty"
    })
    assert response.status_code == 422
    print("status code:", response.status_code)
    print("response json:", response.json())
