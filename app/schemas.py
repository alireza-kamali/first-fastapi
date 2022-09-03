from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class PostBase(BaseModel):                   # This is for validating the information that user sent . for example here we don't want an int or bool or... we just want str title and content
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr            # this is an email validator that we import from pydantic model.
    password: str


class UserOut(BaseModel):       # this is going to be the shape of our model when we sent back the user's data to the client.
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostResponse(PostBase):                   # all of our pydantic models have to extend by BaseModel. and then like creating a post we have to specify all the fields we want in response.(give data back to the user)
    id: int                                  # we may give all the data back, or we want some sort of data back.for example the user don't want his login/sign up account information data back
    created_at: datetime                     # to prevent dublication we inherit items that we defined in PostBase(in the prevois Class)
    owner_id: int
    owner: UserOut           # instead of str or int we are going to return a user (a pydantic model)

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True



    """   new_post = models.Post(**post.dict())         # The ** operator is used to pack and unpack dictionary in Python and is useful for sending them to a function
    db.add(new_post)        # just like sql we have to commit those changes into the database by this command.
    db.commit()
    db.refresh(new_post)      # we retrieve that post we created and stored in the variable new_post
    return new_post
    
when we maked this query we create a new post as a SQlAlchemy not a dictionary and pydantic models have no idea what to do with this .cuz pydantic just can read dictionary .
so we have to tell it to convert sqlalchemy model to a pydantic model with this code ( 
    class Config:
        orm_mode = True)"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)                # i would like to validate to ensure the value is just 0 or 1.   (le means less than or equal to... but note that it still contains the negative numbers)