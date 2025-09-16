from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    course_class = relationship("CourseClass", back_populates="schedules")
    room = relationship("Room", back_populates="schedules")
    start_period = relationship("Period", foreign_keys=[period_start])
    end_period = relationship("Period", foreign_keys=[period_end])

    # Constraints
    __table_args__ = (
        CheckConstraint('day_of_week BETWEEN 1 AND 7', name='check_day_of_week'),
        UniqueConstraint('course_class_id', 'day_of_week', 'period_start', 'period_end', name='unique_schedule'),
    )