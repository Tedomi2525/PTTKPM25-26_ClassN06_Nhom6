from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SemesterBase(BaseModel):
    semester_name: str = Field(..., alias="semesterName", description="Name of the semester")
    start_time: datetime = Field(..., alias="startTime", description="Start date of the semester")
    end_time: datetime = Field(..., alias="endTime", description="End date of the semester")

    class Config:
        populate_by_name = True


class SemesterCreate(SemesterBase):
    pass

class SemesterUpdate(BaseModel):
    semester_name: Optional[str] = Field(None, alias="semesterName", description="Name of the semester")
    start_time: Optional[datetime] = Field(None, alias="startTime", description="Start date of the semester")
    end_time: Optional[datetime] = Field(None, alias="endTime", description="End date of the semester")

    class Config:
        populate_by_name = True

class Semester(SemesterBase):
    semester_id: int = Field(..., alias="semesterId", description="Unique ID of the semester")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True
