from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class CourseClass(Base):
    __tablename__ = "course_classes"

    course_class_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id", ondelete="SET NULL"))
    semester = Column(String(20), nullable=False)
    year = Column(String(20), nullable=False)
    section = Column(String(20))

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    course = relationship("Course", back_populates="course_classes")
    teacher = relationship("Teacher", back_populates="course_classes")
