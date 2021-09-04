"""Route Dependencies"""

from typing import Optional
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from pydantic import BaseModel, ValidationError

from app.core import config, security
from app.database import get_session
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=config.API_PREFIX + "/auth/login/access-token"
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # TODO(TOM): make CRUD classes
    # See https://github.dev/tiangolo/full-stack-fastapi-postgresql/blob/490c554e23343eec0736b06e59b2108fdd057fdc/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py
    user = session.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
