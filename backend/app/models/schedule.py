from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_class_id = Column(Integer, ForeignKey("course_classes.course_class_id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="SET NULL"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    period_start = Column(Integer, ForeignKey("periods.period_id"), nullable=False)
    period_end = Column(Integer, ForeignKey("periods.period_id"), nullable=False)
    # Thêm thông tin tuần và ngày cụ thể cho học kỳ 10 tuần
    week_number = Column(Integer, nullable=True)  # Tuần thứ mấy (1-10)
    specific_date = Column(Date, nullable=True)   # Ngày cụ thể
    semester_id = Column(Integer, ForeignKey("semesters.semester_id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    course_class = relationship("CourseClass", back_populates="schedules")
    room = relationship("Room", back_populates="schedules")
    start_period = relationship("Period", foreign_keys=[period_start])
    end_period = relationship("Period", foreign_keys=[period_end])
    semester = relationship("Semester", back_populates="schedules")
    attendances = relationship("Attendance", back_populates="schedule", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint('day_of_week BETWEEN 1 AND 7', name='check_day_of_week'),
        CheckConstraint('week_number BETWEEN 1 AND 20', name='check_week_number'),
        UniqueConstraint('course_class_id', 'day_of_week', 'period_start', 'period_end', 'week_number', name='unique_schedule_week'),
    )