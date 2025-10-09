import os
from datetime import date, datetime
from enum import Enum
from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel, EmailStr, Field, field_validator

# ==============================================================================
# BASE SCHEMA
# ==============================================================================

class StudentBase(BaseModel):
    student_code: Optional[str] = Field(None, alias="studentCode")
    first_name: str = Field(..., alias="firstName", max_length=50)
    last_name: str = Field(..., alias="lastName", max_length=100)
    dob: Optional[date] = Field(None, alias="dob")
    gender: Optional[str] = Field(None, alias="gender")
    email: Optional[str] = Field(None, alias="email")
    phone: Optional[str] = Field(None, alias="phone", max_length=20)
    class_name: Optional[str] = Field(None, alias="className", max_length=50)
    user_id: Optional[int] = Field(None, alias="userId")
    training_program: Optional[str] = Field(None, alias="trainingProgram", max_length=50)
    course_years: Optional[str] = Field(None, alias="courseYears", max_length=20)
    education_type: Optional[str] = Field(None, alias="educationType")
    faculty: Optional[str] = Field(None, alias="faculty", max_length=100)
    major: Optional[str] = Field(None, alias="major", max_length=100)
    status: Optional[str] = Field(None, alias="status")
    position: Optional[str] = Field(None, alias="position", max_length=50)
    avatar: Optional[str] = Field(None, alias="avatar", max_length=255)

    class Config:
        populate_by_name = True


# ==============================================================================
# CREATE SCHEMA
# ==============================================================================

class StudentCreate(StudentBase):
    avatar_file: Optional[UploadFile] = None
    @classmethod
    def as_form(
        cls,
        studentCode: Optional[str] = Form(None),
        firstName: str = Form(...),
        lastName: str = Form(...),
        dob: Optional[str] = Form(None),
        gender: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        className: Optional[str] = Form(None),
        userId: Optional[int] = Form(0),
        trainingProgram: Optional[str] = Form(None),
        courseYears: Optional[str] = Form(None),
        educationType: Optional[str] = Form(None),
        faculty: Optional[str] = Form(None),
        major: Optional[str] = Form(None),
        status: Optional[str] = Form(None),
        position: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        avatar_file: Optional[UploadFile] = File(None),
    ):
        return cls(
            studentCode=studentCode,
            firstName=firstName,
            lastName=lastName,
            dob=dob,
            gender=gender,
            phone=phone,
            className=className,
            userId=userId,
            trainingProgram=trainingProgram,
            courseYears=courseYears,
            educationType=educationType,
            faculty=faculty,
            major=major,
            status=status,
            position=position,
            avatar=avatar,
            avatar_file=avatar_file,
        )

    @field_validator('dob', mode='before')
    @classmethod
    def validate_dob(cls, v):
        if not v or str(v).strip().lower() in ['string', 'null', 'undefined']:
            return None
        return v

    @field_validator('class_name', 'training_program', 'course_years', 'faculty', 'major', 'position', 'avatar', mode='before')
    @classmethod
    def validate_string_fields(cls, v):
        if not v or str(v).strip().lower() in ['string', 'null', 'undefined']:
            return None
        return str(v).strip()

    @field_validator('avatar_file', mode='before')
    @classmethod
    def validate_avatar_file(cls, v):
        if v in (None, "", "null", "undefined"):
            return None
        return v


# ==============================================================================
# UPDATE & RESPONSE SCHEMAS
# ==============================================================================

class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    student_id: int = Field(..., alias="studentId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
