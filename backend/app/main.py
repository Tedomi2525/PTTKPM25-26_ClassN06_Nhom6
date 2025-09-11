from fastapi import FastAPI
from app.routers import test
# Tạo app
app = FastAPI(
    title="QLDT API",
    description="Quản lý đào tạo - FastAPI backend",
    version="1.0.0"
)

app.include_router(test.router, prefix="/api")