from models import Comment
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from domain.comment.schema import CommentResponse, CommentCreate

def get_comment_list(db: Session):
    comment_list = db.query(Comment).all()
    return comment_list

def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).get(comment_id)
    return comment

def get_comment_by_post(db: Session, post_id: int):
    comment_list = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comment_list

def get_comment_by_parent_comment_id(db: Session, parent_comment_id: int):
    comment_list = db.query(Comment).filter(Comment.parent_comment_id == parent_comment_id).all()
    return comment_list

def create_comment(db: Session, comment_create: CommentCreate, author_id: int):
    try:
        comment = Comment(content = comment_create.content, 
                    post_id=comment_create.post_id, 
                    author_id = author_id, 
                    parent_comment_id=comment_create.parent_comment_id, 
                    )
        db.add(comment)
        db.commit()
        return comment
    except IntegrityError as e:
        db.rollback()  # 트랜잭션 롤백
        if "foreign key constraint" in str(e):
            raise ValueError("not valid post_id")
        raise e

def delete_comment(db: Session, comment_id: int, current_user: int):
    try:
        comment = db.query(Comment).get(comment_id)
        if comment:
            if current_user == comment.author_id:
                ## 삭제 or "삭제된 댓글입니다 변경경"
                db.delete(comment)
                db.commit()
                return comment
            else:
                raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post"
                        )
        else:
            return None
    except Exception as e:
        raise e