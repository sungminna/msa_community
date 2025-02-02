from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
from domain.board import schema, crud
from starlette import status

router = APIRouter(
    prefix="/api/board",
)

@router.get("/list", response_model=list[schema.BoardResponse])
def board_list(db: Session = Depends(get_db)):
    try:
        _board_list = crud.get_board_list(db=db)
        return _board_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{board_id}", response_model=schema.BoardResponse)
def board_detail(board_id: int, db: Session = Depends(get_db)):
    try:
        board = crud.get_board(db=db, board_id=board_id)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="board not found")
        return board
    except Exception as e:
        raise e

@router.post("/", response_model=schema.BoardResponse)
def board_create(_board_create: schema.BoardCreate, db: Session = Depends(get_db)):
    try:
        board = crud.create_board(db=db, board_create=_board_create)
        if not board:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="board creation failed")
        return board
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def board_delete(board_id: int, db: Session = Depends(get_db)):
    try:
        board = crud.delete_board(db=db, board_id=board_id)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="board not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise e