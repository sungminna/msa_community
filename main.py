from fastapi import FastAPI, Request
from domain.board import router as board_router
from domain.post import router as post_router
from otel import init_telemetry, instrument_app


app = FastAPI()
logger = init_telemetry("community-service")


app.include_router(board_router.router)
app.include_router(post_router.router)


instrument_app(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """ 모든 요청과 응답을 로깅 """
    logger.info(f"🔹 Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"🔹 Response: {response.status_code} {request.url}")
    return response