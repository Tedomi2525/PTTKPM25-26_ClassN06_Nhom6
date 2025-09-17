from sqlalchemy import Column, Integer, Time, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from sqlalchemy.orm import relationship

class Period(Base):
    __tablename__ = "periods"

    period_id = Column(Integer, primary_key=True, autoincrement=True)
    period_number = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    schedule_templates = relationship("ScheduleTemplate", back_populates="period")