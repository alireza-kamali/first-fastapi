from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func      # it's gonna access us to the function like count


router = APIRouter(
    prefix="/posts",       # by this we tell the router, every path operation starts with /posts .so we can remove them.
    tags=['Posts']
)


"""about published and rating part we defined a default value for them .it means if user pass a value for them it will shown as a bool or
 int and if they doesn't pass, the server will show our default value for them(True,None).for other part in title or content if user didn't pass
a value (str) we got an error

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite food", "content": "i like pizza", "id": 3}]


def find_post(id):                           # this function is for grabbing the information by their IDs. it's a way to retrieving an individual post.
    for p in my_posts:                       # 'p' represents the specific post that we are looking for it.
        if p['id'] == id:                    # p['id'] is the list of IDs that given to the posts. and (== id) is the id that is given to the function .
            return p                         # we return that specific post.


def find_index_post(id):                     # for deleting post ,find the index in the array that has required ID ,my_post.pop(index)
    for i, p in enumerate(my_posts):         # By this we are going to access the specific post that we interested in as well as the index of that
        if p["id"] == id:
            return i                         # This is gonna give us the index of the dictionary with that specific id."""


# if i change this to /login that means this path operation only apply if the user goes to our URL and goes to /login

@router.get("/sqlalchemy")
def get_posts(db: Session = Depends(get_db)):                   # we're gonna run our first query.anytime you wanna perform any kind of database operation with sqlalchemy within fastapi you have to make sure you pass it as a parameter into our path operation function
    posts = db.query(models.Post).all()                         # models.Post => that's gonna allow us to access us to the models and posts table that we created in the Post model.
    return posts                                      # we want to query all the posts, so we use (all) method.


@router.get("/", response_model=List[schemas.PostOut])            # we're gonna import List from typing and use that here cuz we are returning a list of posts we should ba able to returning a list not an individual post.
def get_posts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search:Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")     # we run this command of SQL to retrieve our posts from our postgre database.
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by\
        (models.Post.id).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



""" @app.post("/createposts")                           we can name "payload" whatever we want.
def create_posts(payload: dict = Body(...)):        what this is going to do is extract all the fields from the body(in the post man app section) and converted them to a python dictionary and it's going to stored them into a variable named payload. to doing that we're going into
 (postman app) and in Body section we select "raw" and JSON type and then we write like a python dictionary.
    print(payload)                                 to extract the data from the body from the payload at first we have to import Body.
    return {"new_post": f"title :{payload['title']}, content:{payload['content']}"} """      #by this we learn not only send data in the body with the postman request we're also able to extract that data and send that to the user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)              # By this trick we can change the default status code for any kind of method we use!
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends
    (oauth2.get_current_user)):

    # cursor.execute(f"INSERT INTO posts(title, content, published) VALUES({post.title}, {post.content}, {post.published})")     we can also use this simple command but we do cuz our code gonna be vulnerble and weak against SQL injections (for example if the user for the title decided to pass a wierd SQL statement like INSERT INTO ..... he can manipulate data
    # and database with SQL attack that's why we don't have to pass the data directly into that )
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING  * """,
                   # (post.title, post.content, post.published))    # therefor we use (%s statement) and put the data into the second field .(and remember that these %s statements are jsut variables .and we put the entries into the second parameter)
    # conn.commit()
    # new_post = cursor.fetchone()

# in sqlalchemy way.

    # new_post = models.Post(title= post.title, content= post.content, published= post.published)
    print(current_user.id)

    new_post = models.Post(owner_id=current_user.id, **post.dict())         # The ** operator is used to pack and unpack dictionary in Python and is useful for sending them to a function
    db.add(new_post)                                                        # just like sql we have to commit those changes into the database by this command.
    db.commit()
    db.refresh(new_post)                                                    # we retrieve that post we created and stored in the variable new_post
    return new_post

    # whenever you insert a data(obviously in post method) run this command to save it into the postgres database otherwise it's not gonna be saved.

    # ***TO DEFINE THE RESPONSE MODEL : we just pass another field in path parameter (response_model=schemas.PostResponse) ***     the data we got back is not a valid dict.cuz pydantic class works with dictionary take that dict and converts it to a specific model


""" post_dict = post.dict()                   post_dict is a pydantic model that converted to a dictionary
    post_dict['id'] = randrange(0, 10000000)     we need to have an id for every entry.(remember normally the database handle this)
    .we want to assign an unique number as an "id" for every post_dict that we create.
    my_posts.append(post_dict)
    return {"data": "created post"}

    print(post)
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)
    print(post.dict())

* if we need to convert our pydantic model to a dictionary we have to do this(post.dict())
* return {"data": "post"}
* path parameter
* if we don't comply with this order(at first str path parameter and then int path parameter) we confront a problem cuz ID is an int and 'latest' is a str. API has to match the number or str in the url to the functions.
* keep that in mind when U structuring the API


@router.get("/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post"""


@router.get("/{id}", response_model=schemas.PostOut)                                                      # cuz the users are going to provide us the id of the specific post that they interested in.that's why it(id) embeded in the url.
def get_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends
    (oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))       # if you hard code the id you're going to be vulnerable to the SQL injections.so we use the id we used in from the path parameter.and at first we use %s as a place holder and in the second field we put id
    #post = cursor.fetchone()
    # print(type(id))                                                        # use (type function) is a way to figour out what the type of our variable is. when we use that we found out the type of the id is 'str' so as we want to == id with smth we have to convert that to an int
    # post = find_post(int(id))

    # post = db.query(models.Post).filter(models.Post.id == id).first()          # at first we have to specify what model we want to query, and then we have to filter the posts by their id. if the id that user pass to the program was equal to the id of the any entry in our table (databse )it will return you back and if not it give you the error.(we use {.first} cuz we know we have just one post with every single id so to prevent wasting time to looking for any id like that by postgres we use {.first} not {.all})

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found"}

    """if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")"""
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db),  current_user: int = Depends
    (oauth2.get_current_user)):

    #cursor.execute(
    #   """ DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))         #we use (str(id)) cuz in here we have to pass a string but in privous part we had to convert the id to the integer
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)        # define the query
    post = post_query.first()                                              # find the post


    if post == None:                                                         # if user entered an id that doesn't exist in our database.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)       # this is going to delete the post
    db.commit()                                    # to execute the changes
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)                  # we don't want to send data back it is the feature of 204 status code .
    # return {"message": "post successfully deleted"}


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published,(str(id)) ))
    # at first when we write the codes we didn't specify where and what id we wanna to update so SQL update all the entries!we have to use WHERE statement to prevent that.
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)      # make the dependency
    post = post_query.first()

    if post == None:                                                       # if user entered an id that doesn't exist in our database.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)           # (post.dict())this is gonna turn all the fields in the Post class to a python dictionary and we have to put our data in a python dictionary in the postman.(pass the fields we wanna update into a python dict) form
    db.commit()                                                           # AttributeError: 'Post' object has no attribute 'update'      it's a common attributeError you may see.
    return post

    # index = find_index_post(id)


""" post_dict = post.dict()          # That's gonna take all the data from frontend which is stored in post and it's going to convert it to a dictionary.
post_dict['id'] = id                # we are going to set an id inside this new dictionary.this final dictionary has an id built in.
my_posts[index] = post_dict         # we are going to pass the index of the specific post we wanna update.this line says: with this post with this index we're just going to replace it with our new post dict.
print(post)"""