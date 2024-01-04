from fastapi import Depends, status, HTTPException, APIRouter, Response
from .. import oauth2, schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def perform_like(like: schemas.LikeSchema, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.owner_id == current_user.id)
    found_like = like_query.first()

    if(like.like_dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already liked post {like.post_id}")
        new_like = models.Like(post_id=like.post_id, owner_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked the post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like Does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully disliked the post"}