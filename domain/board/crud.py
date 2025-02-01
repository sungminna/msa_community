from models import Board
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from domain.board.schema import BoardResponse, BoardCreate

def get_board_list(db: Session):
    board_list = db.query(Board).all()
    return board_list


def get_board(db: Session, board_id: int):
    board = db.query(Board).get(board_id)
    return board


def create_board(db: Session, board_create: BoardCreate):
    try:
        board = Board(name=board_create.name, description=board_create.description)
        db.add(board)
        db.commit()
        return board
    except IntegrityError as e:
        db.rollback()  # 트랜잭션 롤백
        if "duplicate key" in str(e).lower():
            raise ValueError("Board name already exists")
        raise

def delete_board(db: Session, board_id: int):
    try:
        board = db.query(Board).get(board_id)
        if board:
            db.delete(board)
            db.commit()
            return board
        else:
            return None
    except Exception as e:
        raise e
