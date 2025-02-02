from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
from authentication import get_current_user
from domain.post import schema, crud
from starlette import status

router = APIRouter(
    prefix="/api/post",
)

@router.get("/list", response_model=list[schema.PostResponse])
def post_list(db: Session = Depends(get_db)):
    try:
        _post_list = crud.get_post_list(db=db)
        return _post_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{post_id}", response_model=schema.PostResponse)
def post_detail(post_id: int, db: Session = Depends(get_db),):
    try:
        post = crud.get_post(db=db, post_id=post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="post not found")
        return post
    except Exception as e:
        raise e
    
@router.post("/", response_model=schema.PostResponse)
def post_create(_post_create: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        if current_user == 0:
            # anon user
            pass
        post = crud.create_post(db=db, post_create=_post_create, author_id=current_user)
        if not post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="post creation failed")
        return post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def post_delete(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        post = crud.delete_post(db=db, post_id=post_id, current_user=current_user)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="post not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise e