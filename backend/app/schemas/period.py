from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class PeriodBase(BaseModel):
    period_number: int
    start_time: time
    end_time: time

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    period_number: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class Period(PeriodBase):
    period_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True