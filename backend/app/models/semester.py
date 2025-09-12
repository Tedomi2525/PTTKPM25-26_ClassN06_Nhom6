from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, CheckConstraint, UniqueConstraint, Time
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Semester(Base):
    __tablename__ = "semesters"
    semester_id = Column(Integer, primary_key=True, index=True)
    semester_name = Column(String(50), unique=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)