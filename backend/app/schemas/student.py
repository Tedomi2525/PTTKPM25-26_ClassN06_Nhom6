from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Nam"
    FEMALE = "Nữ"
    OTHER = "Khác"

class EducationTypeEnum(str, Enum):
    REGULAR = "Đại học chính quy"
    TRANSFER = "Liên thông"
    COLLEGE = "Cao đẳng"

class StatusEnum(str, Enum):
    STUDYING = "Đang học"
    ON_LEAVE = "Bảo lưu"
    GRADUATED = "Đã tốt nghiệp"

class StudentBase(BaseModel):
    student_code: Optional[str] = Field(None, alias="studentCode", description="Student code")
    first_name: str = Field(..., alias="firstName", max_length=50, description="Student first name")
    last_name: str = Field(..., alias="lastName", max_length=100, description="Student last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[GenderEnum] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", max_length=20, description="Phone number")
    class_name: Optional[str] = Field(None, alias="className", max_length=50, description="Class name")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    training_program: Optional[str] = Field(None, alias="trainingProgram", max_length=50, description="Training program")
    course_years: Optional[str] = Field(None, alias="courseYears", max_length=20, description="Course years")
    education_type: Optional[EducationTypeEnum] = Field(None, alias="educationType", description="Education type")
    faculty: Optional[str] = Field(None, alias="faculty", max_length=100, description="Faculty")
    major: Optional[str] = Field(None, alias="major", max_length=100, description="Major")
    status: Optional[StatusEnum] = Field(None, alias="status", description="Student status")
    position: Optional[str] = Field(None, alias="position", max_length=50, description="Position")
    avatar: Optional[str] = Field(None, alias="avatar", max_length=255, description="Avatar URL")
    
    class Config:
        populate_by_name = True

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    student_code: Optional[str] = Field(None, alias="studentCode", max_length=20, description="Student code")
    first_name: Optional[str] = Field(None, alias="firstName", max_length=50, description="Student first name")
    last_name: Optional[str] = Field(None, alias="lastName", max_length=100, description="Student last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[GenderEnum] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", max_length=20, description="Phone number")
    class_name: Optional[str] = Field(None, alias="className", max_length=50, description="Class name")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    training_program: Optional[str] = Field(None, alias="trainingProgram", max_length=50, description="Training program")
    course_years: Optional[str] = Field(None, alias="courseYears", max_length=20, description="Course years")
    education_type: Optional[EducationTypeEnum] = Field(None, alias="educationType", description="Education type")
    faculty: Optional[str] = Field(None, alias="faculty", max_length=100, description="Faculty")
    major: Optional[str] = Field(None, alias="major", max_length=100, description="Major")
    status: Optional[StatusEnum] = Field(None, alias="status", description="Student status")
    position: Optional[str] = Field(None, alias="position", max_length=50, description="Position")
    avatar: Optional[str] = Field(None, alias="avatar", max_length=255, description="Avatar URL")
    
    class Config:
        populate_by_name = True

class Student(StudentBase):
    student_id: int = Field(..., alias="studentId", description="Student ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True
