from fastapi import FastAPI

from app.database import create_db_and_tables, get_session
from app.routers import users, courses, resources

app = FastAPI()


@app.on_event("startup")
def on_startup():  # pragma: no cover
    create_db_and_tables()


app.include_router(users.router)
app.include_router(courses.router)
app.include_router(resources.router)
