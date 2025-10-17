from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendances"
    
    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.schedule_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    confirmed_at = Column(DateTime)
    confirmed_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint("status IN ('present', 'absent', 'late')", name="check_attendance_status"),
        UniqueConstraint('student_id', 'schedule_id', 'date', name='unique_student_schedule_date'),
    )
    
    # Relationships
    student = relationship("Student", back_populates="attendances")
    schedule = relationship("Schedule", back_populates="attendances")
    confirmer = relationship("User", foreign_keys=[confirmed_by])