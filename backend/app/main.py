from fastapi import FastAPI

from app.routers import test, rooms, programs, users, teacher, program_courses,schedules, students, enrollments, course_class, auth, course_class, courses, semesters
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="QLDT API",
    description="Quản lý đào tạo - FastAPI backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
