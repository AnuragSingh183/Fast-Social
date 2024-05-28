from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text,func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # owner=relationship("User",back_populates="posts")



class User(Base):

    __tablename__="users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    #is_active = Column(Boolean, default=True)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #phone_number = Column(String, nullable=False, unique=True)
    # posts= relationship("Post",back_populates="owner")  #use to define one to many relationship between tables. a user can have multiple post.
    





