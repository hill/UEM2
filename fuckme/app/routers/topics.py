from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from sqlmodel import (
    Session,
    select,
)

from app.database import get_session
from app.models import Topic, TopicRead, TopicCreate

router = APIRouter(prefix="/topics", tags=["topics"])


def get_topic(session: Session, topic_id: int) -> Topic:
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.post("/", response_model=TopicRead)
def create_topic(*, session: Session = Depends(get_session), topic: TopicCreate):
    db_topic = Topic.from_orm(topic)
    session.add(db_topic)
    session.commit()
    session.refresh(db_topic)
    return db_topic


@router.get("/", response_model=List[TopicRead])
def read_topics(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    topics = session.exec(select(Topic).offset(offset).limit(limit)).all()
    return topics


@router.get("/{topic_id}", response_model=TopicRead)
def read_resource(*, session: Session = Depends(get_session), topic_id: int):
    return get_topic(session, topic_id)
