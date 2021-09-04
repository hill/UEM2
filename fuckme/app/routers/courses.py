from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from sqlmodel import (
    Session,
    select,
)

from app.database import get_session
from app.models import (
    Course,
    CourseCreate,
    CourseRead,
    CourseUpdate,
    AssignmentRead,
    Assignment,
    AssignmentCreate,
)

router = APIRouter(prefix="/courses", tags=["courses"])


def get_course(session: Session, course_id: int) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseRead)
def create_course(*, session: Session = Depends(get_session), course: CourseCreate):
    db_course = Course.from_orm(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


@router.get("/", response_model=List[CourseRead])
def read_courses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    courses = session.exec(select(Course).offset(offset).limit(limit)).all()
    return courses


@router.get("/{course_id}", response_model=CourseRead)
def read_course(*, session: Session = Depends(get_session), course_id: int):
    return get_course(session, course_id)


@router.patch("/{course_id}", response_model=CourseRead)
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


@router.delete("/{course_id}")
def delete_course(*, session: Session = Depends(get_session), course_id: int):
    course = get_course(session, course_id)
    session.delete(course)
    session.commit()
    return {"ok": True}


def get_assignment(session: Session, assignment_id: int) -> Assignment:
    assignment = session.get(Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")
    return assignment


@router.get("/{course_id}/assignments/{assignment_id}", response_model=AssignmentRead)
def read_assignment(*, session: Session = Depends(get_session), assignment_id: int):
    return get_assignment(session, assignment_id)


@router.get("/{course_id}/assignments", response_model=List[AssignmentRead])
def read_assignments(
    *,
    session: Session = Depends(get_session),
    course_id: int,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    assignments = session.exec(
        select(Assignment)
        .where(Assignment.course_id == course_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return assignments


@router.post("/{course_id}/assignments", response_model=AssignmentRead)
def create_assignment(
    *,
    session: Session = Depends(get_session),
    course_id: int,
    assignment: AssignmentCreate,
):
    assignment_db = Assignment.from_orm(assignment)
    assignment_db.course_id = course_id  # assign to this course
    session.add(assignment_db)
    session.commit()
    session.refresh(assignment_db)
    return assignment_db
