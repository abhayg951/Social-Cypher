from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import CreatePost

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # new_post = models.Posts(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)  # add post to the database
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new_post variable from the database
    return {'data': new_post}


@app.get('/posts/{id}')
def get_single_post(id: str, db: Session = Depends(get_db)):
    single_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id), ))
    # single_post = cursor.fetchone()
    print(single_post)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {id}")

    return {'data': single_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id)
    # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db)):
    single_post = db.query(models.Posts).filter(models.Posts.id == id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = single_post.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")

    single_post.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": single_post.first()}
