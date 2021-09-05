from typing import Dict
import pytest
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from app.tests.conftest import (
    API_PREFIX,
    Session,
    User,
    Course,
    Topic,
    Resource,
    Assignment,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)
from app.util import data
from app.core import config


class TestUtil:
    @pytest.mark.parametrize(
        "model",
        [User, Course, Topic, Resource, Assignment],
    )
    def test_generate_demo_data(self, session: Session, model: SQLModel):

        # data does not exist before
        assert session.query(model).count() == 0

        data.generate_demo_data(session)

        # data exists after
        assert session.query(model).count() != 0

    @pytest.mark.parametrize(
        "model, count",
        [(User, 1), (Course, 0), (Topic, 0), (Resource, 0), (Assignment, 0)],
    )
    def test_generate_demo_data_preexisting_data(
        self, session: Session, model: SQLModel, count: int
    ):
        user = User(
            name="pre-exisitng user",
            email="yeet@mcskeet.com",
            password_hash="password123",
        )
        session.add(user)
        session.commit()

        assert session.query(model).count() == count

        data.generate_demo_data(session)

        # check it did not generate additional data
        assert session.query(model).count() == count


class TestAuth:
    def test_access_token(self, client: TestClient, user: User) -> None:
        login_data = {
            "username": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
        }
        r = client.post(f"{API_PREFIX}/auth/login/access-token", data=login_data)
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    def test_use_access_token(
        self, client: TestClient, normal_user_token_headers: Dict[str, str]
    ) -> None:
        r = client.post(
            f"{API_PREFIX}/auth/login/test-token",
            headers=normal_user_token_headers,
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
