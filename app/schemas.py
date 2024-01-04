from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class PostResponse(BasePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    likes: int

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

'''
for creating the like system we create the response schema for the like system
'post_id' will be the post id, and
'like_dir' is the like direction which can be 1 or 0
1 means that post is liked  and
0 means that post is not liked
'''

class LikeSchema(BaseModel):
    post_id: int
    like_dir: conint(le=1)
