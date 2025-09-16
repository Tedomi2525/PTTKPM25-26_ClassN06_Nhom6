from fastapi import FastAPI
from app.routers import test, rooms, programs, users, teacher, program_courses,schedules

# Tạo app
app = FastAPI(
    title="QLDT API",
    description="Quản lý đào tạo - FastAPI backend",
    version="1.0.0"
)

app.include_router(test.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(programs.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")
app.include_router(schedules.router, prefix="/api")
app.include_router(program_courses.router, prefix="/api")