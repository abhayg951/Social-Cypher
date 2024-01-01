from fastapi import FastAPI, Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, utils, models, oauth2


routers = APIRouter(
    tags=["Authentication"]
)

@routers.post("/login", response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    # This OAuth2PasswordRequestForm will return the following thing:
    # {
        # "username": "user@gmail.com",
        # "password": "password" 
    # }
    # it takes username as a email
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token= oauth2.create_access_token(data = {"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}