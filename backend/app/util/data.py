from sqlmodel import Session
import stripe

from app import models
from app.core.logger import log
from app.core import security


def generate_demo_data(session: Session):
    """Generates demonstration data from models"""

    # check that the db is empty
    if session.query(models.User).first():
        log.info("Data already exists, skipping data generation.")
        return
    log.info("Generating demo data.")

    user = models.User(
        name="Tom Hill",
        email="tomhill98@me.com",
        password_hash=security.get_password_hash("password"),
        stripe_customer_id=stripe.Customer.create()["id"],
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    discrete_maths = models.Course(
        name="Introduction to Reinforcement Learning",
        code="RL479",
        description="description",
        status="completing",
        due="2021-12-12",
        syllabus=[
            {
                "id": 1,
                "name": "Introduction to Reinforcement Learning",
                "completed": False,
            },
            {"id": 2, "name": "Exploration and Control", "completed": False},
            {"id": 3, "name": "MDPs and Dynamic Programming", "completed": False},
            {
                "id": 4,
                "name": "Fundementals of Dynamic Programming Algorithms",
                "completed": False,
            },
            {"id": 5, "name": "Model-Free Prediction", "completed": False},
            {"id": 6, "name": "Model-Free Control", "completed": False},
            {"id": 7, "name": "Function Approximation", "completed": False},
            {"id": 8, "name": "Planning & Models", "completed": False},
            {
                "id": 9,
                "name": "Policy-Gradient and Actor-Critic Methods",
                "completed": False,
            },
            {"id": 10, "name": "Approximate Dynamic Programming", "completed": False},
            {"id": 11, "name": "Multi-Step & Off Policy", "completed": False},
            {"id": 12, "name": "Deep RL 1", "completed": False},
            {"id": 13, "name": "Deep RL 2", "completed": False},
        ],
        cover={"color": "#8bbeb2"},
        user_id=user.id,
    )

    maths = models.Topic(name="mathematics")
    algebra = models.Topic(name="algebra")

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
        description="Examination of:Set theory, Proof, Graph Theory",
        due="2021-12-12",
        course_id=discrete_maths.id,
        status="in_progress",
        weight=50,
    )

    session.add_all([linear_algebra, big_exam])
    session.commit()
