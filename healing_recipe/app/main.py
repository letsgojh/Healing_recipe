# app/main.py

from fastapi import FastAPI
from app.api.v1.recommend import router as recommend_router
from fastapi.middleware.cors import CORSMiddleware # 👈 1. 이거 임포트


app = FastAPI(title="Healing Recipe API")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 출처 목록
    allow_credentials=True,
    allow_methods=["*"],        # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],        # 모든 헤더 허용
)

app.include_router(recommend_router, prefix="/api/v1", tags=["recommend"])