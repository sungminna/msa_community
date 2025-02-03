from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
from authentication import get_current_user
from domain.comment import schema, crud
from starlette import status

router = APIRouter(
    prefix="/api/comment",
)

@router.get("/list", response_model=list[schema.CommentResponse])
def comment_list(db: Session = Depends(get_db)):
    try:
        _comment_list = crud.get_comment_list(db=db)
        return _comment_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{comment_id}", response_model=schema.CommentResponse)
def comment_detail(comment_id: int, db: Session = Depends(get_db),):
    try:
        comment = crud.get_comment(db=db, comment_id=comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="comment not found")
        return comment
    except Exception as e:
        raise e

@router.get("/list/{post_id}", response_model=list[schema.CommentResponse])
def comment_list_by_post_id(post_id: int, db: Session = Depends(get_db)):
    try:
        _comment_list = crud.get_comment_by_post(db=db, post_id=post_id)
        return _comment_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/list/parent/{parent_comment_id}", response_model=list[schema.CommentResponse])
def comment_list_by_parent_comment_id(parent_comment_id: int, db: Session = Depends(get_db)):
    try:
        _comment_list = crud.get_comment_by_parent_comment_id(db=db, parent_comment_id=parent_comment_id)
        return _comment_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    
@router.post("/", response_model=schema.CommentResponse)
def comment_create(_comment_create: schema.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        if current_user == 0:
            # anon user
            pass
        comment = crud.create_comment(db=db, comment_create=_comment_create, author_id=current_user)
        if not comment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="comment creation failed")
        return comment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        comment = crud.delete_comment(db=db, comment_id=comment_id, current_user=current_user)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="comment not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise e