import pytest
from sqlmodel import SQLModel

from app.tests.conftest import (
    Session,
    User,
    Course,
    Topic,
    Resource,
    Assignment,
)
from app.util import data


class TestUtil:
    @pytest.mark.parametrize(
        "model",
        [User, Course, Topic, Resource, Assignment],
    )
    def test_generate_demo_data(self, session: Session, model: SQLModel):

        # data does not exist before
        assert session.query(model).count() is 0

        data.generate_demo_data(session)

        # data exists after
        assert session.query(model).count() is not 0

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
