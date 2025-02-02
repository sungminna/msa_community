from models import Post
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from domain.post.schema import PostResponse, PostCreate

def get_post_list(db: Session):
    post_list = db.query(Post).all()
    return post_list

def get_post(db: Session, post_id: int):
    post = db.query(Post).get(post_id)
    return post

def create_post(db: Session, post_create: PostCreate, author_id: int):
    try:
        post = Post(title=post_create.title, 
                    content = post_create.content, 
                    board_id=post_create.board_id, 
                    author_id = author_id)
        db.add(post)
        db.commit()
        return post
    except IntegrityError as e:
        db.rollback()  # 트랜잭션 롤백
        if "foreign key constraint" in str(e):
            raise ValueError("not valid board_id")
        raise e

def delete_post(db: Session, post_id: int, current_user: int):
    try:
        post = db.query(Post).get(post_id)
        if post:
            if current_user == post.author_id:
                db.delete(post)
                db.commit()
                return post
            else:
                raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post"
                        )
        else:
            return None
    except Exception as e:
        raise e