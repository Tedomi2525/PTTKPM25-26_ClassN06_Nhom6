from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class AttendanceBase(BaseModel):
    student_id: int
    schedule_id: int
    date: date
    status: str = Field(..., regex="^(present|absent|late)$")

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(present|absent|late)$")
    confirmed_at: Optional[datetime]
    confirmed_by: Optional[int]

class AttendanceInDBBase(AttendanceBase):
    attendance_id: int
    confirmed_at: Optional[datetime]
    confirmed_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Attendance(AttendanceInDBBase):
    pass