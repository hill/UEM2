import datetime
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .app import Course, Resource, User, app, get_session


@pytest.fixture(name="session")
def session_fixture():
    # use an in-memory database for testing
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user")
def user_fixture(session: Session):
    user = User(
        name="Harry Potter",
        email="harry.potter@hogwarts.magic",
        password_hash="magic_hashed",
    )
    session.add(user)
    session.commit()
    yield user


@pytest.fixture(name="resource")
def resource_fixture(user: User, session: Session):
    resource = Resource(name="UNSW", url="unsw.edu.au", user_id=user.id)
    session.add(resource)
    session.commit()
    yield resource


@pytest.fixture(name="course")
def course_fixture(user: User, session: Session):
    course = Course(
        name="Discrete Maths",
        description="Hello world",
        status="completing",
        due=datetime.date(2021, 8, 29),
        user_id=user.id,
        syllabus=[{"item": 123}],
    )
    session.add(course)
    session.commit()
    yield course


class TestUsers:
    def test_create_user(self, client: TestClient):
        new_user = {
            "name": "Harry Potter",
            "email": "h.potter@hogwarts.magic",
            "password": "wizzzard",
        }
        response = client.post(
            "/users/",
            json=new_user,
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == new_user["name"]
        assert data["email"] == new_user["email"]
        assert data["id"] is not None
        assert "password" not in data

    def test_create_user_incomplete(self, client: TestClient):
        response = client.post("/users/", json={"name": "Harry Potter"})
        assert response.status_code == 422

    def test_create_user_invalid(self, client: TestClient):
        response = client.post(
            "/users/", json={"name": "Harry Potter", "email": {}, "password": "magics"}
        )
        assert response.status_code == 422

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

        response = client.get("/users/")
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["name"] == user_1.name
        assert data[0]["email"] == user_1.email
        assert data[0]["id"] == user_1.id
        assert "password" not in data[0]
        assert "password_hash" not in data[0]

    def test_read_user(self, user: User, client: TestClient):
        response = client.get(f"/users/{user.id}")
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == user.name
        assert data["email"] == user.email
        assert data["id"] == user.id
        assert "password" not in data
        assert "password_hash" not in data

    def test_update_user(self, user: User, client: TestClient):
        response = client.patch(f"/users/{user.id}", json={"name": "Harry Granger"})
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Harry Granger"
        assert data["email"] == user.email
        assert "password" not in data
        assert "password_hash" not in data

    def test_delete_user(self, user: User, session: Session, client: TestClient):

        response = client.delete(f"/users/{user.id}")

        user_in_db = session.get(User, user.id)

        assert response.status_code == 200
        assert user_in_db is None

    def test_user_not_found(self, client: TestClient):
        response = client.get("/users/69")
        assert response.status_code == 404


class TestResource:
    def test_create_resource(self, user: User, client: TestClient):
        new_resource = {"name": "google", "url": "google.com", "user_id": user.id}
        response = client.post("/resources/", json=new_resource)
        data = response.json()
        assert response.status_code == 200
        # check resource is a subset of the response
        assert all(item in data.items() for item in new_resource.items())

    def test_read_resources(self, resource: Resource, client: TestClient):
        response = client.get("/resources/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == resource.name
        assert data[0]["url"] == resource.url
        assert data[0]["user_id"] == resource.user_id
        assert len(data) == 1

    def test_update_resource(self, resource: Resource, client: TestClient):
        response = client.patch(f"/resources/{resource.id}", json={"name": "Xoogle"})
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Xoogle"
        assert data["url"] == resource.url
        assert data["user_id"] == resource.user_id
        assert data["votes"] == resource.votes

    def test_delete_resource(
        self, resource: Resource, session: Session, client: TestClient
    ):
        response = client.delete(f"/resources/{resource.id}")
        assert response.status_code == 200
        resource_in_db = session.get(Resource, resource.id)
        assert resource_in_db is None

    def test_upvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(f"/resources/{resource.id}/vote?vote=1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count + 1

    def test_downvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(f"/resources/{resource.id}/vote?vote=-1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count - 1

    def test_too_many_votes_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(f"/resources/{resource.id}/vote?vote=100")
        assert response.status_code == 400
        assert resource.votes == old_vote_count

    def test_resource_not_found(self, client: TestClient):
        response = client.get("/resources/69")
        assert response.status_code == 404


class TestCourse:
    def test_create_course(self, user: User, client: TestClient):
        new_course = {
            "name": "Discrete Maths",
            "description": "hello world",
            "status": "completing",
            "due": "2021-08-29",
            "syllabus": [{"item": 123}],
            "user_id": user.id,
        }
        response = client.post("/courses/", json=new_course)
        data = response.json()
        assert response.status_code == 200
        assert all(item in data.items() for item in new_course.items())

    def test_read_courses(self, course: Course, client: TestClient):
        response = client.get("/courses/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == course.name
        assert data[0]["user_id"] == course.user_id
        assert len(data) == 1

    def test_update_course(self, course: Course, client: TestClient):
        response = client.patch(
            f"/courses/{course.id}", json={"name": "Linear Algebra"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Linear Algebra"
        assert data["user_id"] == course.user_id

    def test_delete_course(self, course: Course, session: Session, client: TestClient):
        response = client.delete(f"/courses/{course.id}")
        assert response.status_code == 200
        course_in_db = session.get(Course, course.id)
        assert course_in_db is None

    def test_course_not_found(self, client: TestClient):
        response = client.get("/courses/69")
        assert response.status_code == 404
