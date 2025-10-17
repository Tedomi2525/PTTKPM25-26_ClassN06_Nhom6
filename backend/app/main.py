from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.routers import test, rooms, programs, users, teacher, program_courses,schedules, students, enrollments, course_class, auth, courses, semesters, attendances
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
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router, prefix="/api", tags=["Test"])
app.include_router(rooms.router, prefix="/api", tags=["Rooms"])
app.include_router(programs.router, prefix="/api", tags=["Programs"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(teacher.router, prefix="/api", tags=["Teachers"])
app.include_router(schedules.router, prefix="/api", tags=["Schedules"])
app.include_router(program_courses.router, prefix="/api", tags=["Program Courses"])
app.include_router(students.router, prefix="/api", tags=["Students"])
app.include_router(enrollments.router, prefix="/api", tags=["Enrollments"])
app.include_router(course_class.router, prefix="/api", tags=["Course Classes"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api", tags=["Courses"])
app.include_router(semesters.router, prefix="/api", tags=["Semesters"])
app.include_router(attendances.router, prefix="/api", tags=["Attendances"])

# Create static directories if they don't exist
STATIC_DIR = "static"
AVATARS_DIR = os.path.join(STATIC_DIR, "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
