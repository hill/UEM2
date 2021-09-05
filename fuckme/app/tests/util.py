import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core import security, config
from app.tests.conftest import (
    Session,
    User,
)


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{config.API_PREFIX}/auth/login/access-token", data=data)
    assert r.status_code == 200
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    password_hash = security.get_password_hash(password)
    user = db.query(User).where(User.email == email).first()
    if not user:
        # TODO(TOM): put Create op in some util function
        user = User(name=email.split("@")[0], email=email, password_hash=password_hash)
    else:
        user.password_hash = password_hash

    db.add(user)
    db.commit()
    db.refresh(user)

    return user_authentication_headers(client=client, email=email, password=password)
