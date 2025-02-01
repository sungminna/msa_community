from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from database import Base

class Board(Base):
    __tablename__= "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(500))

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(String(2000))
    community_id = Column(Integer, ForeignKey("boards.id"))
    author_id = Column(Integer)
    created_at = Column(DateTime)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    post_id = Column(Integer, ForeignKey("posts.id")) 
    author_id = Column(Integer)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"))
    created_at = Column(DateTime)

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer)
    created_at = Column(DateTime)
