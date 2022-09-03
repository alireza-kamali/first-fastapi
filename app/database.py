# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# that is the format of the connection string we have to pass to sqlalchemy

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# we create an engine ,that is responsible for sqlalchemy to connect to a postgres database

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# in here we have to define our Base class and all of the models that we defined to create our tables in postgres gonna be extending to this class.
# now we want to define our tables by python mode with ORM instead of using pgadmin and SQL codes or any other extentions.

# dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    # what this ultimately is gonna do is,the session object is responsible for talking to the database and since we created this function we get a connection to our database or get a session to our database
                      # and every time we get a reaquest we get a session, we're going to sent a sql statement to it and after when the requset is done we close it out.
                      # now that we get our dependency we have to change our path parameter and pass one more parameter to perform some operation in the database .


    """while True:  # this means we're going to doing over and over again till we got the connection and break the while loop.
        try:
            conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='Alikm1212**hbk',
                                    cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("database connection was successful1")
            break
        except Exception as error:
            print("connection to database failed")
            print("Error:", error)
            time.sleep(2)  # cuz it's going to do this really quickly, we want to wait 2 seconds before reconnect.
            
            # anytime you have some kind of code in python that potentially can fail, we're gonna use the (try) statement.
            # we want to set up a connection to our database.
            # what cursor_factory do is , it is gonna return us the name of the column. otherwise it's just gonna give you the value of the column ,
            and if don't corrct this we will not gonna know which value match which column.so we (from psycopg2.extras import RealDictCursor)"""