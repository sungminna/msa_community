from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint

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
    content = Column(String(1000))
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    author_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    post_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE")) 
    author_id = Column(Integer)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    user_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uix_post_user"),
    )
