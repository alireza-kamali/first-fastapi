# this file is going to store all of our models. every model represent a table in our database.
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))    # just like when we typed in the dafault values in the pgadmin we have to pass

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

    # our default values like this with (server_default) parameter.

""" remember this point about creating the tables with sqlalchemy.whenever you change your table and columns and add smth to that ,
your table in the postgres is not gonna update and does not include that new parameter .because (models.Base.metadata.create_all(bind=engine)
)this command that has the responsibility to creating the table is going to search in postgres and look for the table with (posts) name 
 if it did found that table it's not gonna touch it anymore and do nothing so to get the changes we have to delete that table and refresh the databses."""


class User(Base):         # we're going to handle the registration.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)       # unique=True this is gonna prevent a single email to register twice.
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    phone_number = Column(String, nullable=False, unique=True )


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



