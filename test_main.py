from fastapi.testclient import TestClient
from main import app

test_client = TestClient(app)

users = [
    {
        "id" : "fd822558-fb95-11ec-8bea-b174a14e8f75",
        "name" : "martin",
        "favorite_tv_show" : "breaking_bad"
    },
    {
        "id" : "0d81105e-fb96-11ec-8bea-b174a14e8f75",
        "name" : "lukas",
        "favorite_tv_show" : "the_wire"
    },
    {
        "id" : "158c1064-fb96-11ec-8bea-b174a14e8f75",
        "name" : "dominik",
        "favorite_tv_show" : "breaking_bad"
    }
]

def test_read_root():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message" : "hello world!"}

def test_create_user():
    response = test_client.post(
        "/user/create",
        json=users[0]
    )
    assert response.status_code == 200
    assert response.json() == {"status" : "Success", 
                        "message" : "User created!"}

    response = test_client.post(
        "/user/create",
        json=users[1]
    )
    assert response.status_code == 200
    assert response.json() == {"status" : "Success", 
                        "message" : "User created!"}

    response = test_client.post(
        "/user/create",
        json=users[2]
    )
    assert response.status_code == 200
    assert response.json() == {"status" : "Success", 
                        "message" : "User created!"}

def test_create_existing_user():
    response = test_client.post(
        "/user/create",
        json=users[0]
    )
    assert response.status_code == 409
    assert response.json() == {"detail" : "User already exists"}

def test_modify_user():
    response = test_client.patch(
        "/user/modify/158c1064-fb96-11ec-8bea-b174a14e8f75?favorite_tv_show=the_wire"
    )
    assert response.status_code == 200
    assert response.json() == {"status" : "Success", "message" : "User data modified"}

def test_modify_missing_user():
    response = test_client.patch(
        "/user/modify/158c1064-fb96-11ec-8bea-b174a14e8f76?favorite_tv_show=the_wire"
    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "User doesn't exists"}

def test_delete_user():
    response = test_client.delete(
        "/user/delete/158c1064-fb96-11ec-8bea-b174a14e8f75"
    )
    assert response.status_code == 200
    assert response.json() == {"status" : "Success", "message" : "User data deleted"}

def test_delete_missing_user():
    response = test_client.delete(
        "/user/delete/158c1064-fb96-11ec-8bea-b174a14e8f76"
    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "User doesn't exists"}

def test_find_users():
    response = test_client.get(
        "/users/find/breaking_bad" 
    )
    assert response.status_code == 200
    assert response.json() == { "users" : [
        {
            "id" : "fd822558-fb95-11ec-8bea-b174a14e8f75",
            "name" : "martin"
        }
    ] }

    response = test_client.get(
        "/users/find/the_wire" 
    )
    assert response.status_code == 200
    assert response.json() == { "users" : [
        {
            "id" : "0d81105e-fb96-11ec-8bea-b174a14e8f75",
            "name" : "lukas"
        }
    ] }