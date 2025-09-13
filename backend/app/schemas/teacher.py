from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class TeacherBase(BaseModel):
    first_name: str = Field(..., alias="firstName", description="Teacher first name")
    last_name: str = Field(..., alias="lastName", description="Teacher last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[str] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", description="Phone number")
    department: Optional[str] = Field(None, alias="department", description="Department")
    faculty: Optional[str] = Field(None, alias="faculty", description="Faculty")
    specialization: Optional[str] = Field(None, alias="specialization", description="Specialization")
    degree: Optional[str] = Field(None, alias="degree", description="Academic degree")
    academic_rank: Optional[str] = Field(None, alias="academicRank", description="Academic rank")
    status: Optional[str] = Field("active", description="Status of the teacher, e.g., active or inactive")

class TeacherCreate(TeacherBase):
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    teacher_code: Optional[str] = Field(None, alias="teacherCode", description="Teacher code")

class TeacherUpdate(BaseModel):
    teacher_code: Optional[str] = Field(None, alias="teacherCode", description="Teacher code")
    first_name: Optional[str] = Field(None, alias="firstName", description="Teacher first name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Teacher last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[str] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", description="Phone number")
    department: Optional[str] = Field(None, alias="department", description="Department")
    faculty: Optional[str] = Field(None, alias="faculty", description="Faculty")
    specialization: Optional[str] = Field(None, alias="specialization", description="Specialization")
    degree: Optional[str] = Field(None, alias="degree", description="Academic degree")
    academic_rank: Optional[str] = Field(None, alias="academicRank", description="Academic rank")
    status: Optional[str] = Field(None, description="Status of the teacher, e.g., active or inactive")

class Teacher(TeacherBase):
    teacher_id: int = Field(..., alias="teacherId", description="Teacher ID")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True