from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth
from .config import settings

print(settings.database_name)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.routers)
app.include_router(users.routers)
app.include_router(auth.routers)