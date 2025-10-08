from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Nested schemas for related data
class CourseInfo(BaseModel):
    course_id: int = Field(..., alias="courseId")
    course_code: str = Field(..., alias="courseCode")
    name: str
    credits: int
    
    class Config:
        from_attributes = True
        populate_by_name = True

class TeacherInfo(BaseModel):
    teacher_id: int = Field(..., alias="teacherId")
    teacher_code: str = Field(..., alias="teacherCode")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True

class CourseClassBase(BaseModel):
    course_id: int = Field(..., alias="courseId", description="ID of the course")
    teacher_id: int = Field(..., alias="teacherId", description="ID of the teacher")
    section: Optional[str] = Field(None, description="Section name")
    max_students: Optional[int] = Field(None, alias="maxStudents", gt=0, description="Maximum number of students")
    min_students: Optional[int] = Field(None, alias="minStudents", ge=0, description="Minimum number of students")
    
    class Config:
        populate_by_name = True

class CourseClassCreate(CourseClassBase):
    pass

class CourseClassUpdate(BaseModel):
    course_id: Optional[int] = Field(None, alias="courseId", description="ID of the course")
    teacher_id: Optional[int] = Field(None, alias="teacherId", description="ID of the teacher")
    section: Optional[str] = Field(None, description="Section name")
    max_students: Optional[int] = Field(None, alias="maxStudents", gt=0, description="Maximum number of students")
    min_students: Optional[int] = Field(None, alias="minStudents", ge=0, description="Minimum number of students")
    
    class Config:
        populate_by_name = True

class CourseClassResponse(CourseClassBase):
    course_class_id: int = Field(..., alias="courseClassId", description="ID of the course class")
    course: CourseInfo = Field(..., description="Course information")
    teacher: TeacherInfo = Field(..., description="Teacher information")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True