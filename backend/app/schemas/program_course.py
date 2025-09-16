from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProgramCourseBase(BaseModel):
    program_id: int = Field(..., alias="programId", description="ID of the program")
    course_id: int = Field(..., alias="courseId", description="ID of the course")
    semester_no: str = Field(..., alias="semesterNo", description="Semester number")
    is_required: bool = Field(..., alias="isRequired", description="Is this course required?")

class ProgramCourseCreate(ProgramCourseBase):
    pass

class ProgramCourseUpdate(BaseModel):
    semester_no: Optional[str] = Field(None, alias="semesterNo", description="Semester number")
    is_required: Optional[bool] = Field(None, alias="isRequired", description="Is this course required?")

class ProgramCourseResponse(ProgramCourseBase):
    program_course_id: int = Field(..., alias="programCourseId", description="ID of the program-course relationship")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True

class ProgramCourseWithDetails(ProgramCourseResponse):
    course_name: Optional[str] = Field(None, alias="courseName", description="Name of the course")
    course_code: Optional[str] = Field(None, alias="courseCode", description="Code of the course")
    credits: Optional[int] = Field(None, alias="credits", description="Credits of the course")
    program_name: Optional[str] = Field(None, alias="programName", description="Name of the program")