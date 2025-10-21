from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .course_class import CourseClassResponse

class EnrollmentBase(BaseModel):
    student_id: int = Field(..., alias="studentId", description="ID of the student")
    course_class_id: int = Field(..., alias="courseClassId", description="ID of the course class")
    
    class Config:
        populate_by_name = True

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = Field(None, alias="studentId", description="ID of the student")
    course_class_id: Optional[int] = Field(None, alias="courseClassId", description="ID of the course class")
    
    class Config:
        populate_by_name = True

class Enrollment(EnrollmentBase):
    enrollment_id: int = Field(..., alias="enrollmentId", description="ID of the enrollment")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")
    course_class: Optional[CourseClassResponse] = Field(None, alias="courseClass")
    
    class Config:
        from_attributes = True
        populate_by_name = True