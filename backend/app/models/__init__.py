# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .teacher import Teacher
from .course import Course
from .course_class import CourseClass
from .room import Room
from .semester import Semester
from .program import Program
from .attendance import Attendance
from .timetable import Timetable

__all__ = [
    "User",
    "Teacher", 
    "Course",
    "CourseClass",
    "Room",
    "Semester",
    "Program",
    "Attendance", 
    "Timetable"
]