from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

class ScheduleTemplate(Base):
    __tablename__ = "schedule_templates"
    
    template_id = Column(Integer, primary_key=True, index=True)
    course_class_id = Column(Integer, ForeignKey("course_classes.course_class_id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="SET NULL"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.period_id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    course_class = relationship("CourseClass", back_populates="schedule_templates")
    room = relationship("Room", back_populates="schedule_templates")
    period = relationship("Period", back_populates="schedule_templates")
    