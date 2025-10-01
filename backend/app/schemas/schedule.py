from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    course_class_id: int = Field(..., alias="courseClassId", description="ID of the course class")
    room_id: int = Field(..., alias="roomId", description="ID of the room")
    day_of_week: int = Field(..., alias="dayOfWeek", ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    period_start: int = Field(..., alias="periodStart", description="Start period")
    period_end: int = Field(..., alias="periodEnd", description="End period")
    
    class Config:
        populate_by_name = True

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    course_class_id: Optional[int] = Field(None, alias="courseClassId", description="ID of the course class")
    room_id: Optional[int] = Field(None, alias="roomId", description="ID of the room")
    day_of_week: Optional[int] = Field(None, alias="dayOfWeek", ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    period_start: Optional[int] = Field(None, alias="periodStart", description="Start period")
    period_end: Optional[int] = Field(None, alias="periodEnd", description="End period")
    
    class Config:
        populate_by_name = True

class ScheduleResponse(ScheduleBase):
    schedule_id: int = Field(..., alias="scheduleId", description="ID of the schedule")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True