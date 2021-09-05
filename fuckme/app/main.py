import os
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.core import config
from app.core.logger import log
from app.database import create_db_and_tables, get_session
from app.routers import auth, users, courses, resources, topics
from app.util.data import generate_demo_data

app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

if config.BACKEND_CORS_ORIGINS:
    log.warning(f"CORS enabled for {config.BACKEND_CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup():  # pragma: no cover
    log.info(
        f"[yellow]App running in [bold]{config.ENVIRONMENT}[/bold] mode[/]",
        extra={"markup": True},
    )
    create_db_and_tables()
    if config.ENVIRONMENT != "production":
        generate_demo_data(next(get_session()))


@app.on_event("shutdown")
def on_shutdown():
    if config.ENVIRONMENT != "production" and not config.PERSIST_DB:
        log.warn("Removing database. (PERSIST_DB is false).")
        os.remove("database.db")


api_router = APIRouter(prefix=config.API_PREFIX)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(resources.router)
api_router.include_router(topics.router)

app.include_router(api_router)
