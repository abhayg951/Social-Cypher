from fastapi import Depends, status, HTTPException, APIRouter, Response
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

routers = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@routers.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= "" ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # new_post = models.Posts(
    #     title=post.title, content=post.content, published=post.published)
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)  # add post to the database
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new_post variable from the database
    return new_post


@routers.get('/{id}', response_model=schemas.PostResponse)
def get_single_post(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    single_post = db.query(models.Post).filter(models.Post.id == id).first()
    print(single_post)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {id}")

    return single_post


@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@routers.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    single_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = single_post.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    single_post.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return single_post.first()