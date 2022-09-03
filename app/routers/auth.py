from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)
# the user is gonna generate and provide us credential so our path opereation is gonna be post.


@router.post('/login', response_model=schemas.Token)     # we set response model to class Token to make sure token will be sent in those 2 fields when we return a token.
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):                      # def login(user_credentials:schemas.UserLogin, db: Session =Depends(get_db)):
                                                                              # we are going to create a dependency for user_credentials this is gonna requier us to retrieve the credentials and then fast api is gonna stored in user_credentials
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
# we have to make a small change here cuz when you retrieve the attempted credentials from OAuth2PasswordRequestForm , it's gonna stored them in a field not called email but it's gonna stored in a field called (username) .so we change user_credentials.email to user_credentials.username
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):     # if the attempted pass was not equal to stored pass...
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")
    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})       # this is (in data) all we want to put in to the payload
    return {"access_token": access_token, "token_type": "bearer"}



