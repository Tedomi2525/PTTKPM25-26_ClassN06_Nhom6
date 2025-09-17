from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Program(Base):
    __tablename__ = "programs"
    program_id = Column(Integer, primary_key=True, index=True)
    program_name = Column(String(150), nullable=False)
    department = Column(String(100))
    start_year = Column(Integer, nullable=False)
    duration = Column(Integer)
    current_semester = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)