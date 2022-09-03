from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

""" When we want to import smth from one file into another file that they are both are in the same directory we use one dot (.) and 
 import that file, like: from . import models, schemas, utils       
 but when we want to import a file that does not exist in our directory 
 we use two dots and the of those files. like :from .. import models, schemas, utils"""

router = APIRouter(
    prefix="/users",
    tags=['Users']           # this is for creating nice and clean and grouped documentation in Fast API doxs
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",  response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id :{id} does not exist")
    return user
