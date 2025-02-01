from fastapi import FastAPI
from domain.board import router as board_router

app = FastAPI()

app.include_router(board_router.router)
