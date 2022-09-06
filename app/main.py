from fastapi import FastAPI                           # cd PycharmProjects , cd API 2, uvicorn app.main:app --reload
from .database import engine
from . import models
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, post, auth, vote    # we use one dot cuz they are in the same directory

#models.Base.metadata.create_all(bind=engine)
""" after using alembic we actually don't need this command this is the command that tell sqlalchemy run the create statement to generate all of 
the tables when it first started up but since we have alembic you no longer need this command .you can delete this.if it does create
tables for you then your first alembic migration isn't gonna do anything cuz everything is already there"""

app = FastAPI()

"""if someone sends a request to our app before it actually goes to all of our routers below it'll actually goes to the middlewere and our middlewere
can perform some sort of operations.at first we have to specify the origins we wanna allow what domains should be able to talk to our API .cuz righ now
 there is no domains. to do that we create a list of origins.in allow_method we can specify the specific http method we wanna get from the users.for 
example when we are building a public API where people can retrieve data we may don't want to allow them to send post, put, delete requests and 
  by this option we can limit them to only send get request.
to specify origins we can simply write the address of the domain we wanna talk to our API
if you wanna set up a public API that everyone can access it, then your origins will be["*"] that means every single domain or every single origin"""

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

"""what we basicly done here? when we get a http request before we have all of our path operation instead ,whats gonna happen is 
   we go down the list like we normally do, and as we go down in here app.include_router(post.router)
 this is the first match object on the list and in here it says i want to include everything in my post.router .so requst is gonna go
   in post file in router directory and the user request is gonna look for a match in the post file.this is how we break out our code
   into separate files.(we use these router object that we import above.)"""










