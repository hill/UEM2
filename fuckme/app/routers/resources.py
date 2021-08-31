from typing import List, Optional

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from sqlmodel import (
    Session,
    select,
)

from app.database import get_session
from app.models import (
    Resource,
    ResourceCreate,
    ResourceRead,
    ResourceUpdate,
    ResourceReadWithDetails,
    Topic,
    ResourceTopicLink,
)

router = APIRouter(prefix="/resources", tags=["resources"])


def get_resource(session: Session, resource_id: int) -> Resource:
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.post("/", response_model=ResourceReadWithDetails)
def create_resource(
    *, session: Session = Depends(get_session), resource: ResourceCreate
):
    db_resource = Resource.from_orm(resource)

    # TODO(TOM): make this get or create topic
    db_resource.topics = [session.get(Topic, topic_id) for topic_id in resource.topics]

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@router.get("/", response_model=List[ResourceReadWithDetails])
def read_resources(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    search: Optional[str] = None,
    topics: Optional[str] = None,
):
    query = select(Resource)

    if topics:
        topics = topics.split(",")
        query = (
            query.join(ResourceTopicLink, Resource.id == ResourceTopicLink.resource_id)
            .join(Topic, Topic.id == ResourceTopicLink.topic_id)
            .where(Topic.name.in_(topics) | Topic.id.in_(topics))
        )

    if search:
        query = query.where(Resource.name.contains(search))

    query = query.order_by(Resource.votes.desc()).offset(offset).limit(limit)
    resources = session.exec(query).all()
    return resources


@router.get("/{resource_id}", response_model=ResourceReadWithDetails)
def read_resource(*, session: Session = Depends(get_session), resource_id: int):
    return get_resource(session, resource_id)


@router.patch("/{resource_id}", response_model=ResourceRead)
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


@router.patch("/{resource_id}/vote", response_model=ResourceRead)
def vote_on_resource(
    *, session: Session = Depends(get_session), resource_id: int, vote: int
):
    """Upvote or downvote a resource using the `vote` query param.

    Use `/vote?vote=1` for an upvote, `/vote?vote=-1` for a downvote.
    Any user (including unauthorized users) may PATCH to this route.
    """
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


@router.patch("/{resource_id}/broken", response_model=ResourceRead)
def mark_resource_broken(*, session: Session = Depends(get_session), resource_id: int):
    """Mark a resource as broken"""
    db_resource = get_resource(session, resource_id)
    db_resource.broken += 1
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


@router.delete("/{resource_id}")
def delete_resource(*, session: Session = Depends(get_session), resource_id: int):
    resource = get_resource(session, resource_id)
    session.delete(resource)
    session.commit()
    return {"ok": True}
