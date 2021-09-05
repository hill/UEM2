from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from sqlmodel import (
    Session,
    select,
)

from app import deps
from app.core import security
from app.database import get_session
from app.models import User, UserCreate, UserRead, UserUpdate, UserReadWithDetails

router = APIRouter(prefix="/users", tags=["users"])


def get_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=UserRead)
def read_user_me(
    *,
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get the current user"""
    return current_user


@router.post("/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(
        user, {"password_hash": security.get_password_hash(user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserReadWithDetails)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    return get_user(session, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
):
    db_user = get_user(session, user_id)
    if db_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int, current_user: User = Depends(deps.get_current_active_user),):
    user = get_user(session, user_id)
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session.delete(user)
    session.commit()
    return {"ok": True}
