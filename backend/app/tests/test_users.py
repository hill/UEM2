from app.tests.conftest import API_PREFIX, Session, TestClient, User


class TestUsers:
    def test_create_user(self, client: TestClient, patch_stripe):
        new_user = {
            "name": "Harry Potter",
            "email": "h.potter@hogwarts.magic",
            "password": "wizzzard",
        }
        response = client.post(
            API_PREFIX + "/users/",
            json=new_user,
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == new_user["name"]
        assert data["email"] == new_user["email"]
        assert data["id"] is not None
        assert "password" not in data

    def test_create_user_incomplete(self, client: TestClient, patch_stripe):
        response = client.post(API_PREFIX + "/users/", json={"name": "Harry Potter"})
        assert response.status_code == 422

    def test_create_user_invalid(self, client: TestClient, patch_stripe):
        response = client.post(
            API_PREFIX + "/users/",
            json={"name": "Harry Potter", "email": {}, "password": "magics"},
        )
        assert response.status_code == 422

    def test_read_user_me(self, authenticated_client: TestClient, user: User):
        response = authenticated_client.get(API_PREFIX + "/users/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user.email
        assert data["name"] == user.name

    def test_read_users(self, session: Session, client: TestClient):
        user_1 = User(
            name="Harry Potter",
            email="harry.potter@hogwarts.magic",
            password_hash="magic_hashed",
        )
        user_2 = User(
            name="Hermione Granger",
            email="h.granger@hogwarts.magic",
            password_hash="leviosaaaa_hashed",
        )
        session.add(user_1)
        session.add(user_2)
        session.commit()

        response = client.get(API_PREFIX + "/users/")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["name"] == user_1.name
        assert data[0]["email"] == user_1.email
        assert data[0]["id"] == user_1.id
        assert "password" not in data[0]
        assert "password_hash" not in data[0]

    def test_read_user(self, user: User, client: TestClient):
        response = client.get(API_PREFIX + f"/users/{user.id}")
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == user.name
        assert data["email"] == user.email
        assert data["id"] == user.id
        assert "password" not in data
        assert "password_hash" not in data

    def test_update_user(self, user: User, authenticated_client: TestClient):
        response = authenticated_client.patch(
            API_PREFIX + f"/users/{user.id}", json={"name": "Harry Granger"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Harry Granger"
        assert data["email"] == user.email
        assert "password" not in data
        assert "password_hash" not in data

    def test_delete_user(
        self, user: User, session: Session, authenticated_client: TestClient
    ):
        response = authenticated_client.delete(API_PREFIX + f"/users/{user.id}")

        user_in_db = session.get(User, user.id)

        assert response.status_code == 200
        assert user_in_db is None

    def test_user_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/users/69")
        assert response.status_code == 404
