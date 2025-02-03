from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
from authentication import get_current_user
from domain.like import schema, crud
from starlette import status

router = APIRouter(
    prefix="/api/like",
)

@router.get("/list", response_model=list[schema.LikeResponse])
def like_list(db: Session = Depends(get_db)):
    try:
        _like_list = crud.get_like_list(db=db)
        return _like_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{like_id}", response_model=schema.LikeResponse)
def like_detail(like_id: int, db: Session = Depends(get_db),):
    try:
        like = crud.get_like(db=db, like_id=like_id)
        if not like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="like not found")
        return like
    except Exception as e:
        raise e
    
@router.post("/", response_model=schema.LikeResponse)
def like_create(_like_create: schema.LikeCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        if current_user == 0:
            # anon user
            pass
        like = crud.create_like(db=db, like_create=_like_create, author_id=current_user)
        if not like:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="like creation failed")
        return like
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
def like_delete(like_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        like = crud.delete_like(db=db, like_id=like_id, current_user=current_user)
        if not like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="like not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise e
    
@router.get("/count/{post_id}")
def like_count(post_id: int, db: Session = Depends(get_db)):
    try:
        cnt = crud.count_like(db=db, post_id=post_id)
        return {"count": cnt}
    except Exception as e:
        raise e