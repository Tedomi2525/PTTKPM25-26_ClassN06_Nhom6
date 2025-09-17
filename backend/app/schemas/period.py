from pydantic import BaseModel, Field
from datetime import time, datetime
from typing import Optional

class PeriodBase(BaseModel):
    period_number: int = Field(..., alias="periodNumber", description="Period number")
    start_time: time = Field(..., alias="startTime", description="Start time of the period")
    end_time: time = Field(..., alias="endTime", description="End time of the period")

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    period_number: Optional[int] = Field(None, alias="periodNumber", description="Period number")
    start_time: Optional[time] = Field(None, alias="startTime", description="Start time of the period")
    end_time: Optional[time] = Field(None, alias="endTime", description="End time of the period")

class Period(PeriodBase):
    period_id: int = Field(..., alias="periodId", description="ID of the period")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True