import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from sqlmodel import (
    Field,
    Session,
    SQLModel,
    create_engine,
    select,
    Relationship,
    Column,
    JSON,
)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


class UserBase(SQLModel):
    name: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str

    resources: List["Resource"] = Relationship(back_populates="user")
    courses: List["Course"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class ResourceBase(SQLModel):
    name: str
    url: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    votes: Optional[int] = Field(default=0)
    user: User = Relationship(back_populates="resources")


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int
    votes: int


class ResourceUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None


class CourseBase(SQLModel):
    name: str
    description: str
    status: str
    due: datetime.date
    syllabus: List[Dict] = Field(sa_column=Column(JSON))
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="courses")


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int


class CourseUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]
    due: Optional[datetime.date]
    syllabus: Optional[List[Dict]]


class ResourceReadWithUser(ResourceRead):
    user: Optional[UserRead] = None


class UserReadWithDetails(UserRead):
    resources: List[ResourceRead] = []
    courses: List[CourseRead] = []


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():  # pragma: no cover
    SQLModel.metadata.create_all(engine)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():  # pragma: no cover
    create_db_and_tables()


def get_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user, {"password_hash": user.password + "_hash"})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/users/{user_id}", response_model=UserReadWithDetails)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    return get_user(session, user_id)


@app.patch("/users/{user_id}", response_model=UserRead)
def update_user(
    *, session: Session = Depends(get_session), user_id: int, user: UserUpdate
):
    db_user = get_user(session, user_id)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = get_user(session, user_id)
    session.delete(user)
    session.commit()
    return {"ok": True}


def get_resource(session: Session, resource_id: int) -> Resource:
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@app.post("/resources/", response_model=ResourceRead)
def create_resource(
    *, session: Session = Depends(get_session), resource: ResourceCreate
):
    db_resource = Resource.from_orm(resource)
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@app.get("/resources/", response_model=List[ResourceRead])
def read_resources(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    resources = session.exec(select(Resource).offset(offset).limit(limit)).all()
    return resources


@app.get("/resources/{resource_id}", response_model=ResourceReadWithUser)
def read_resource(*, session: Session = Depends(get_session), resource_id: int):
    return get_resource(session, resource_id)


@app.patch("/resources/{resource_id}", response_model=ResourceRead)
def update_resource(
    *,
    session: Session = Depends(get_session),
    resource_id: int,
    resource: ResourceUpdate,
):
    db_resource = get_resource(session, resource_id)
    resource_data = resource.dict(exclude_unset=True)
    for key, value in resource_data.items():
        setattr(db_resource, key, value)
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@app.patch("/resources/{resource_id}/vote", response_model=ResourceRead)
def update_resource(
    *, session: Session = Depends(get_session), resource_id: int, vote: int
):
    if vote not in {1, -1}:
        print("wrong vote!")
        raise HTTPException(
            status_code=400, detail="Vote may only upvote (1) or downvote (-1) once"
        )
    db_resource = get_resource(session, resource_id)
    db_resource.votes += vote
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@app.delete("/resources/{resource_id}")
def delete_resource(*, session: Session = Depends(get_session), resource_id: int):
    resource = get_resource(session, resource_id)
    session.delete(resource)
    session.commit()
    return {"ok": True}


def get_course(session: Session, course_id: int) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses/", response_model=CourseRead)
def create_course(*, session: Session = Depends(get_session), course: CourseCreate):
    db_course = Course.from_orm(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


@app.get("/courses/", response_model=List[CourseRead])
def read_courses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    courses = session.exec(select(Course).offset(offset).limit(limit)).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseRead)
def read_course(*, session: Session = Depends(get_session), course_id: int):
    return get_course(session, course_id)


@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(
    *,
    session: Session = Depends(get_session),
    course_id: int,
    course: CourseUpdate,
):
    db_course = get_course(session, course_id)
    course_data = course.dict(exclude_unset=True)
    for key, value in course_data.items():
        setattr(db_course, key, value)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


@app.delete("/courses/{course_id}")
def delete_course(*, session: Session = Depends(get_session), course_id: int):
    course = get_course(session, course_id)
    session.delete(course)
    session.commit()
    return {"ok": True}
