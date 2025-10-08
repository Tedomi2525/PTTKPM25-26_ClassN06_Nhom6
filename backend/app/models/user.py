from datetime import datetime
from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, ForeignKey, TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150))
    password = Column(String(512), nullable=False)
    role = Column(String(20), CheckConstraint("role IN ('admin','teacher','student')"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)