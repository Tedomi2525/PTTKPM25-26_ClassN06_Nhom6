from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_code = Column(String(20), unique=True, nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    dob = Column(Date)
    gender = Column(String(10))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    
    class_name = Column("class", String(50))
    training_program = Column(String(50))
    course_years = Column(String(20))
    education_type = Column(String(50))
    faculty = Column(String(100))
    major = Column(String(100))
    position = Column(String(50))
    avatar = Column(String(255))
    
    status = Column(String(50), default="Đang học")

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")

    __table_args__ = (
        CheckConstraint("gender IN ('Nam', 'Nữ', 'Khác')", name="check_gender"),
        CheckConstraint("education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng')", name="check_education_type"),
        CheckConstraint("status IN ('Đang học', 'Bảo lưu', 'Đã tốt nghiệp')", name="check_status"),
    )