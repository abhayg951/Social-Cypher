from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, like
from .config import settings
from os import getenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_name)

app = FastAPI(
    title="Post System",
    summary="This API enables users to Create, Read, Update, and Delete records seamlessly while ensuring security through robust user authentication, offering a comprehensive data management solution.",
    description='''This comprehensive API empowers users with full CRUD capabilities for managing posts while ensuring secure access through user authentication\n. 
    Beyond basic operations, it features a robust like system, enabling users to interact with posts by viewing and contributing to like counts\n. 
    With seamless Create, Read, Update, and Delete functionalities, coupled with user authentication and a dynamic like system, this API offers a versatile and secure platform for content management and user engagement, making it ideal for applications where posts play a central role and user interactions are key.''',
    version="1.0",
    contact={
        "name": "Abhay Gupta",
        "email": "insuabhay951@gmail.com"
    },
     docs_url="/"
)

origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.routers)
app.include_router(users.routers)
app.include_router(auth.routers)
app.include_router(like.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)