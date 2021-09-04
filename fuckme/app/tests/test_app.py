from app.tests.conftest import (
    API_PREFIX,
    Session,
    TestClient,
    User,
    Course,
    Topic,
    Resource,
)
from app.util import data


class TestUtil:
    def test_generate_demo_data(self, session: Session):

        assert session.query(User).first() is None
        assert session.query(Course).first() is None
        assert session.query(Topic).first() is None
        assert session.query(Resource).first() is None

        data.generate_demo_data(session)

        assert session.query(User).first() is not None
        assert session.query(Course).first() is not None
        assert session.query(Topic).first() is not None
        assert session.query(Resource).first() is not None

    def test_generate_demo_data_preexisting_data(self, session: Session):
        user = User(
            name="pre-exisitng user",
            email="yeet@mcskeet.com",
            password_hash="password123",
        )
        session.add(user)
        session.commit()

        assert session.query(User).count() == 1
        assert session.query(Course).first() is None
        assert session.query(Topic).first() is None
        assert session.query(Resource).first() is None

        data.generate_demo_data(session)

        # check it did not generate additional data
        assert session.query(User).count() == 1
        assert session.query(Course).first() is None
        assert session.query(Topic).first() is None
        assert session.query(Resource).first() is None
