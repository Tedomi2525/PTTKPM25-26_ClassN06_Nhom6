from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.routers import test, rooms, programs, users, teacher, program_courses,schedules, students, enrollments, course_class, auth, course_class, courses, semesters
from fastapi.middleware.cors import CORSMiddleware
# Import models to ensure they are registered with SQLAlchemy
import app.models

app = FastAPI(
    title="QLDT API",
    description="Quản lý đào tạo - FastAPI backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(programs.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")
app.include_router(schedules.router, prefix="/api")
app.include_router(program_courses.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(enrollments.router, prefix="/api")
app.include_router(course_class.router, prefix="/api")
app.include_router(auth.router, prefix="/auth")
app.include_router(course_class.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(semesters.router, prefix="/api")

# Create static directories if they don't exist
STATIC_DIR = "static"
AVATARS_DIR = os.path.join(STATIC_DIR, "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
