from datetime import timedelta
from typing import Any, List, Optional

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import (
    Session,
    select,
)

from app import deps
from app.core import security
from app.database import get_session
from app.models import User, UserCreate, UserRead, UserUpdate, UserReadWithDetails

router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(session: Session, *, email: str, password: str) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not security.verify_password(password, user.password_hash):
        return None
    return user


@router.post("/login/access-token", response_model=deps.Token)
def login_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(
        session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=UserRead)
def test_token(current_user: User = Depends(deps.get_current_user)) -> User:
    """
    Test access token
    """
    return current_user


# TODO(TOM): password recovery and reset password
# https://github.dev/tiangolo/full-stack-fastapi-postgresql/blob/490c554e23343eec0736b06e59b2108fdd057fdc/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/api/api_v1/endpoints/login.py
