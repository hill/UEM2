from sqlmodel import Session
from app import models
from app.core.config import logger
from app.database import get_session


def generate_demo_data(session: Session):
    """Generates demonstration data from models"""

    # check that the db is empty
    if session.query(models.User).first():
        logger.info("Data already exists, skipping data generation.")
        return
    logger.info("Generating demo data.")

    user = models.User(
        name="Tom Hill", email="tomhill98@me.com", password_hash="pwhash"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    discrete_maths = models.Course(
        name="Discrete Mathematics",
        description="description",
        status="completing",
        due="2021-12-12",
        syllabus=[{"yeet": "cowboy"}],
        user_id=user.id,
    )

    maths = models.Topic(name="Mathematics")
    algebra = models.Topic(name="Algebra")

    session.add_all([discrete_maths, maths, algebra])
    session.commit()
    session.refresh(maths)
    session.refresh(algebra)  # could try session.expire_all() instead?

    linear_algebra = models.Resource(
        name="Interactive Linear Algebra",
        url="http://textbooks.math.gatech.edu/ila/index.html",
        user_id=user.id,
        topics=[maths, algebra],
    )

    big_exam = models.Assignment(
        name="Big Exam",
        due="2021-12,12",
        course_id=discrete_maths.id,
        status="in_progress",
        weight=50,
    )

    session.add_all([linear_algebra, big_exam])
    session.commit()
