import datetime
from typing import Dict, List, Optional

from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
    Column,
    JSON,
)


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
    broken: Optional[int] = Field(default=0)
    user: User = Relationship(back_populates="resources")


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int
    votes: int
    broken: int


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
