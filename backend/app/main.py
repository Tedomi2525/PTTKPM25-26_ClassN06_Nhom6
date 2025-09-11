from fastapi import FastAPI

# Tạo app
app = FastAPI(
    title="QLDT API",
    description="Quản lý đào tạo - FastAPI backend",
    version="1.0.0"
)

# Đăng ký router

# Root test
@app.get("/")
def root():
    return {"message": "QLDT Backend is running 🚀"}
