# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .teacher import Teacher
from .course import Course
from .course_class import CourseClass
from .room import Room
from .semester import Semester
from .program import Program
from .program_course import ProgramCourse
from .schedule import Schedule
from .schedule_template import ScheduleTemplate
from .student import Student
from .period import Period

__all__ = [
    "User",
    "Teacher", 
    "Course",
    "CourseClass",
    "Room",
    "Semester",
    "Program",
    "ProgramCourse",
    "Schedule",
    "ScheduleTemplate",
    "Student", 
    "Period",
]