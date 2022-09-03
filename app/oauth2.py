from jose import JWSError, jwt        # we have to install a library pip install "python-jose[cryptography]"
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')      # this is gonna be an endpoint of our login .

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):                                                # the access token is gonna have a payload so whatever data we wanna encode in the token we have to provide that/ so we have to pass in as a variable called data and this is gonna be the type of dict.
    to_encode = data.copy()                                                         # make a copy of data cuz we're gonna manipulate this couple of times and we don't want to change the original data.
                                                                                    # (to_encode) this the data we're going to encode in our JWT token.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)        # to crate the expire time field we're going to provide the time 30 minutes from now. we grab the current time and timedelta.
    to_encode.update({"exp": expire})                                               # we passed an extra property and put it into all the data we want to encode into our JWT

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)            # jwt.encode this method is gonna create a jwt token

    return encoded_jwt
# we want to create a function to verify the create_access_token


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)     # for creating a token we used .encode method and we use .decode to extract data from the token.
        id: str = payload.get("user_id")               # to extract the specific data we can .get method

        if id is None:
           raise credentials_exception
        token_data = schemas.TokenData(id=id)        # this is gonna validate it matches to our specific token schema.
    except JWSError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session =Depends(database.get_db)):          # what this is gonna do is, can pass this as a dependency in our path operation and it's going to take the token from the request automatically
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})              # extract the id for us and verify the token is correct or not from  verify_access_token function  ?

    token = verify_access_token(token, credentials_exception)      # make a request to our database and since we have access to token we say...

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

