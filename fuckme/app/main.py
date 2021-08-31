from fastapi import FastAPI, APIRouter

from app.core import config
from app.database import create_db_and_tables
from app.routers import users, courses, resources, topics

app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)


@app.on_event("startup")
def on_startup():  # pragma: no cover
    create_db_and_tables()


api_router = APIRouter(prefix=config.API_PREFIX)
api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(resources.router)
api_router.include_router(topics.router)

app.include_router(api_router)
