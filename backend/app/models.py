import datetime
from typing import Dict, List, Optional

from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
    Column,
    JSON,
)

# ===== #
# Users #
# ===== #


class UserBase(SQLModel):
    name: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = True
    is_superuser: bool = False
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


# ==================== #
# Resources and Topics #
# ==================== #


class ResourceTopicLink(SQLModel, table=True):
    resource_id: Optional[int] = Field(
        default=None, foreign_key="resource.id", primary_key=True
    )
    topic_id: Optional[int] = Field(
        default=None, foreign_key="topic.id", primary_key=True
    )


class TopicBase(SQLModel):
    name: str


class Topic(TopicBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resources: List["Resource"] = Relationship(
        back_populates="topics", link_model=ResourceTopicLink
    )


class TopicCreate(TopicBase):
    pass


class TopicRead(TopicBase):
    id: int


class ResourceBase(SQLModel):
    name: str
    url: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    votes: Optional[int] = Field(default=0)
    broken: Optional[int] = Field(default=0)

    user: User = Relationship(back_populates="resources")
    topics: List[Topic] = Relationship(
        back_populates="resources", link_model=ResourceTopicLink
    )


class ResourceCreate(ResourceBase):
    topics: Optional[List[int]] = []


class ResourceRead(ResourceBase):
    id: int
    votes: int
    broken: int


class ResourceUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    topics: Optional[List[int]] = None


# ======= #
# Courses #
# ======= #


class CourseBase(SQLModel):
    name: str
    code: str
    description: str
    status: str
    due: datetime.date
    cover: Dict = Field(sa_column=Column(JSON), default={"color": "#222222"})
    syllabus: List[Dict] = Field(sa_column=Column(JSON))
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="courses")
    assignments: List["Assignment"] = Relationship(back_populates="course")


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
    cover: Optional[Dict]


class AssignmentBase(SQLModel):
    name: str
    status: str  # completed / in_progress
    description: Optional[str]
    due: Optional[datetime.date]
    mark: Optional[float]
    outcome: Optional[str]  # pass/fail
    weight: Optional[float]
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")


class Assignment(AssignmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course: Course = Relationship(back_populates="assignments")


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentRead(AssignmentBase):
    id: int


class ResourceReadWithDetails(ResourceRead):
    user: Optional[UserRead] = None
    topics: List[TopicRead] = []


class UserReadWithDetails(UserRead):
    resources: List[ResourceRead] = []
    courses: List[CourseRead] = []


class CourseReadWithDetails(CourseRead):
    assignments: List[AssignmentRead] = []
