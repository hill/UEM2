import datetime
from typing import Callable, Generator, List, Dict
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.config import API_PREFIX
from app.core import security
from app.database import get_session
from app.models import Course, Resource, User, Topic, Assignment
from app.tests import util

TEST_USER_EMAIL = "harry.potter@hogwarts.magic"
TEST_USER_PASSWORD = "password"


@pytest.fixture(name="session")
def session_fixture() -> Generator:
    # use an in-memory database for testing
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="user")
def user_fixture(session: Session) -> User:
    user = User(
        name="Harry Potter",
        email=TEST_USER_EMAIL,
        password_hash=security.get_password_hash(TEST_USER_PASSWORD),
    )
    session.add(user)
    session.commit()
    yield user


@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    def get_session_override() -> Generator:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="normal_user_token_headers")
def normal_user_token_headers_fixture(
    client: TestClient, session: Session
) -> Dict[str, str]:
    return util.authentication_token_from_email(
        client=client, email="demo@email.com", db=session
    )


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(session: Session, user: User) -> TestClient:
    def get_session_override() -> Generator:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    token_headers = util.user_authentication_headers(
        client=client, email=user.email, password=TEST_USER_PASSWORD
    )
    client.headers.update(token_headers)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="get_request")
def get_request_fixture(client: TestClient) -> Callable[[str], dict]:
    def get_request(url: str):
        response = client.get(API_PREFIX + url)
        assert response.status_code == 200
        return response.json()

    return get_request


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


@pytest.fixture(name="assignment")
def assignment_fixture(course: Course, session: Session) -> Assignment:
    assignment = Assignment(
        name="Big Exam",
        description="Huge Exam",
        status="completed",
        due=datetime.date(2021, 12, 12),
        course_id=course.id,
        weight=50,
        mark=100,
        outcome="pass",
    )
    session.add(assignment)
    session.commit()
    yield assignment
