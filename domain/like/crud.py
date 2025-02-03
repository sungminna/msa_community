from models import Like
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from domain.like.schema import LikeResponse, LikeCreate

def get_like_list(db: Session):
    like_list = db.query(Like).all()
    return like_list

def get_like(db: Session, like_id: int):
    like = db.query(Like).get(like_id)
    return like

def create_like(db: Session, like_create: LikeCreate, author_id: int):
    existing_like = db.query(Like).filter(
            Like.post_id == like_create.post_id, 
            Like.user_id == author_id
        ).first()
    if existing_like:
        raise ValueError("User already liked the post")
    try:
        like = Like(
                    post_id=like_create.post_id, 
                    user_id = author_id)
        db.add(like)
        db.commit()
        return like
    except IntegrityError as e:
        db.rollback()  # 트랜잭션 롤백
        if "foreign key constraint" in str(e):
            raise ValueError("not valid post_id")
        raise e

def delete_like(db: Session, post_id: int, current_user: int):
    try:
        like = Like(
                    post_id=post_id, 
                    user_id = current_user)
        if like:
            if current_user == like.author_id:
                db.delete(like)
                db.commit()
                return like
            else:
                raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post"
                        )
        else:
            return None
    except Exception as e:
        raise e
    
def count_like(db: Session, post_id: int):
    try:
        like_list = db.query(Like).filter(Like.post_id == post_id).all()
        return len(like_list)
    except Exception as e:
        raise e