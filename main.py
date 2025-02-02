from fastapi import FastAPI
from domain.board import router as board_router
from domain.post import router as post_router

app = FastAPI()

app.include_router(board_router.router)
app.include_router(post_router.router)
