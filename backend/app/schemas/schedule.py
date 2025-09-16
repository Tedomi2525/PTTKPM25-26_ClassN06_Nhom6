from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    course_class_id: int
    room_id: int
    day_of_week: int = Field(..., ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    period_start: int
    period_end: int

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    course_class_id: Optional[int] = None
    room_id: Optional[int] = None
    day_of_week: Optional[int] = Field(None, ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    period_start: Optional[int] = None
    period_end: Optional[int] = None

class ScheduleResponse(ScheduleBase):
    schedule_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True