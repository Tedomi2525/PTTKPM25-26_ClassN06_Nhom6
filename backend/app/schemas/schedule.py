from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    course_class_id: int = Field(..., description="ID of the course class", alias="courseClassId")
    room_id: int = Field(..., description="ID of the room", alias="roomId")
    day_of_week: int = Field(..., ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)", alias="dayOfWeek")
    period_start: int = Field(..., description="Start period", alias="periodStart")
    period_end: int = Field(..., description="End period", alias="periodEnd")

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    course_class_id: Optional[int] = Field(None, description="ID of the course class", alias="courseClassId")
    room_id: Optional[int] = Field(None, description="ID of the room", alias="roomId")
    day_of_week: Optional[int] = Field(None, ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)", alias="dayOfWeek")
    period_start: Optional[int] = Field(None, description="Start period", alias="periodStart")
    period_end: Optional[int] = Field(None, description="End period", alias="periodEnd")

class ScheduleResponse(ScheduleBase):
    schedule_id: int = Field(..., description="ID of the schedule", alias="scheduleId")
    created_at: datetime = Field(..., description="Creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    class Config:
        from_attributes = True