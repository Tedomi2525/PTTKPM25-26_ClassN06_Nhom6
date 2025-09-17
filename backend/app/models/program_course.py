from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ProgramCourse(Base):
    __tablename__ = "program_courses"

    program_course_id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    semester_no = Column(String(10), nullable=False)  # học kỳ dự kiến (HK_1_1, HK_1_2, etc.)
    is_required = Column(Boolean, default=True)       # bắt buộc hay tự chọn
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Unique constraint to prevent duplicate program-course-semester combinations
    __table_args__ = (
        UniqueConstraint('program_id', 'course_id', 'semester_no', name='uq_program_course_semester'),
    )

    # Relationships
    program = relationship("Program", backref="program_courses")
    course = relationship("Course", backref="program_courses")