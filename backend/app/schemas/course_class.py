from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CourseClassBase(BaseModel):
    course_id: int
    teacher_id: int
    section: Optional[str] = None
    max_students: Optional[int] = Field(None, gt=0)
    min_students: Optional[int] = Field(None, ge=0)

class CourseClassCreate(CourseClassBase):
    pass

class CourseClassUpdate(BaseModel):
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    section: Optional[str] = None
    max_students: Optional[int] = Field(None, gt=0)
    min_students: Optional[int] = Field(None, ge=0)

class CourseClassResponse(CourseClassBase):
    course_class_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        
        # Aliases for response
        def get_alias_generator():
            return {
                'course_class_id': 'id',
                'course_id': 'courseId',
                'teacher_id': 'teacherId',
                'max_students': 'maxStudents',
                'min_students': 'minStudents',
                'created_at': 'createdAt',
                'updated_at': 'updatedAt'
            }