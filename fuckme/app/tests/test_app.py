import datetime
from typing import Callable, List
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.config import API_PREFIX
from app.database import get_session
from app.models import Course, Resource, User, Topic


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
def client_fixture(session: Session) -> TestClient:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="get_request")
def get_request_fixture(client: TestClient) -> Callable[[str], dict]:
    def get_request(url: str):
        response = client.get(API_PREFIX + url)
        assert response.status_code == 200
        return response.json()

    return get_request


@pytest.fixture(name="user")
def user_fixture(session: Session) -> User:
    user = User(
        name="Harry Potter",
        email="harry.potter@hogwarts.magic",
        password_hash="magic_hashed",
    )
    session.add(user)
    session.commit()
    yield user


@pytest.fixture(name="topic")
def topic_fixture(session: Session) -> Topic:
    topic = Topic(name="Mathematics")
    session.add(topic)
    session.commit()
    yield topic


@pytest.fixture(name="resource")
def resource_fixture(user: User, topic: Topic, session: Session) -> Resource:
    resource = Resource(name="UNSW", url="unsw.edu.au", user_id=user.id, topics=[topic])
    session.add(resource)
    session.commit()
    yield resource


@pytest.fixture(name="many_resources")
def many_resources_fixture(
    user: User, topic: Topic, session: Session
) -> List[Resource]:
    resources = [
        Resource(name="Google", url="google.com", user_id=user.id, topics=[topic]),
        Resource(name="UNSW", url="unsw.edu.au", user_id=user.id, topics=[]),
        Resource(
            name="Introduction To Deep Learning",
            url="https://sebastianraschka.com/blog/2021/dl-course.html",
            user_id=user.id,
            topics=[topic],
        ),
    ]
    for resource in resources:
        session.add(resource)
    session.commit()
    yield resources


@pytest.fixture(name="course")
def course_fixture(user: User, session: Session) -> Course:
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


# TODO(TOM): abstract common CRUD tests?
class TestUsers:
    def test_create_user(self, client: TestClient):
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

    def test_create_user_incomplete(self, client: TestClient):
        response = client.post(API_PREFIX + "/users/", json={"name": "Harry Potter"})
        assert response.status_code == 422

    def test_create_user_invalid(self, client: TestClient):
        response = client.post(
            API_PREFIX + "/users/",
            json={"name": "Harry Potter", "email": {}, "password": "magics"},
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

    def test_update_user(self, user: User, client: TestClient):
        response = client.patch(
            API_PREFIX + f"/users/{user.id}", json={"name": "Harry Granger"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Harry Granger"
        assert data["email"] == user.email
        assert "password" not in data
        assert "password_hash" not in data

    def test_delete_user(self, user: User, session: Session, client: TestClient):

        response = client.delete(API_PREFIX + f"/users/{user.id}")

        user_in_db = session.get(User, user.id)

        assert response.status_code == 200
        assert user_in_db is None

    def test_user_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/users/69")
        assert response.status_code == 404


class TestResource:
    def test_create_resource(self, user: User, topic: Topic, client: TestClient):
        new_resource = {
            "name": "google",
            "url": "google.com",
            "user_id": user.id,
            "topics": [topic.id],
        }
        response = client.post(API_PREFIX + "/resources/", json=new_resource)
        data = response.json()
        assert response.status_code == 200

        assert data["name"] == new_resource["name"]
        assert data["url"] == new_resource["url"]
        assert data["user_id"] == new_resource["user_id"]
        assert len(data["topics"]) == 1
        assert data["topics"][0]["name"] == topic.name

    def test_read_resources(
        self,
        resource: Resource,
        get_request: Callable[[str], dict],
    ):
        data = get_request("/resources/")
        assert data[0]["name"] == resource.name
        assert data[0]["url"] == resource.url
        assert data[0]["user_id"] == resource.user_id
        assert len(data) == 1

    def test_search_resources(
        self,
        many_resources: List[Resource],
        topic: Topic,
        get_request: Callable[[str], dict],
    ):
        data = get_request("/resources/?search=goog")
        assert many_resources[0].name == "Google"
        assert data[0]["name"] == many_resources[0].name
        assert data[0]["url"] == many_resources[0].url
        assert data[0]["user_id"] == many_resources[0].user_id
        assert len(data) == 1

        # check multiple matches but not all results will return
        data = get_request("/resources/?search=o")
        for item in data:
            assert "o" in item["name"]

        # TODO(TOM): search by multiple topics
        # search by topic name
        data = get_request(f"/resources/?topics={topic.name}")
        assert len(data) == 2

        # search by topic id
        data = get_request(f"/resources/?topics={topic.id}")
        assert len(data) == 2

        # search by topic id and search term
        data = get_request(f"/resources/?search=goog&topics={topic.id}")
        assert len(data) == 1
        assert data[0]["name"] == "Google"

    def test_update_resource(self, resource: Resource, client: TestClient):
        response = client.patch(
            API_PREFIX + f"/resources/{resource.id}", json={"name": "Xoogle"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Xoogle"
        assert data["url"] == resource.url
        assert data["user_id"] == resource.user_id
        assert data["votes"] == resource.votes

    def test_delete_resource(
        self, resource: Resource, session: Session, client: TestClient
    ):
        response = client.delete(API_PREFIX + f"/resources/{resource.id}")
        assert response.status_code == 200
        resource_in_db = session.get(Resource, resource.id)
        assert resource_in_db is None

    def test_upvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count + 1

    def test_downvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=-1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count - 1

    def test_too_many_votes_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=100")
        assert response.status_code == 400
        assert resource.votes == old_vote_count

    def test_mark_as_broken(self, resource: Resource, client: TestClient):
        assert resource.broken == 0
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/broken")
        assert response.status_code == 200
        assert resource.broken == 1

    def test_resource_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/resources/69")
        assert response.status_code == 404


class TestTopic:
    def test_create_topic(self, user: User, client: TestClient):
        new_topic = {"name": "Algebra"}
        response = client.post(API_PREFIX + "/topics/", json=new_topic)
        data = response.json()
        assert response.status_code == 200
        # check topic is a subset of the response
        assert all(item in data.items() for item in new_topic.items())

    def test_read_topics(self, topic: Topic, client: TestClient):
        response = client.get(API_PREFIX + "/topics/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == topic.name
        assert len(data) == 1

    def test_read_topic(self, topic: Topic, client: TestClient):
        response = client.get(API_PREFIX + f"/topics/{topic.id}")
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == topic.name

    def test_read_topic_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/topics/69")
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
        response = client.post(API_PREFIX + "/courses/", json=new_course)
        data = response.json()
        assert response.status_code == 200
        assert all(item in data.items() for item in new_course.items())

    def test_read_courses(self, course: Course, client: TestClient):
        response = client.get(API_PREFIX + "/courses/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == course.name
        assert data[0]["user_id"] == course.user_id
        assert len(data) == 1

    def test_update_course(self, course: Course, client: TestClient):
        response = client.patch(
            API_PREFIX + f"/courses/{course.id}", json={"name": "Linear Algebra"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Linear Algebra"
        assert data["user_id"] == course.user_id

    def test_delete_course(self, course: Course, session: Session, client: TestClient):
        response = client.delete(API_PREFIX + f"/courses/{course.id}")
        assert response.status_code == 200
        course_in_db = session.get(Course, course.id)
        assert course_in_db is None

    def test_course_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/courses/69")
        assert response.status_code == 404
