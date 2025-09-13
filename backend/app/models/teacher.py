from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_code = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    dob = Column(Date)
    gender = Column(String(10))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    
    department = Column(String(100))
    faculty = Column(String(100))
    specialization = Column(String(100))
    
    degree = Column(String(50))
    academic_rank = Column(String(50))
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    status = Column(String(20), default="active")  # active, inactive

    # Relationship 
    user = relationship("User", back_populates="teacher")