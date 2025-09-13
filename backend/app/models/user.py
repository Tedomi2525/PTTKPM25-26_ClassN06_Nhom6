from datetime import datetime
from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150))
    password = Column(String(255), nullable=False)
    role = Column(String(20), CheckConstraint("role IN ('admin','teacher','student')"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)