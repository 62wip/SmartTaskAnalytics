# def test_register_user(test_client):
#     response = test_client.post("/auth/register", json={
#         "username": "testuser",
#         "email": "test@example.com",
#         "password": "testpass123"
#     })
#     assert response.status_code == 201
#     assert response.json()["username"] == "testuser"
