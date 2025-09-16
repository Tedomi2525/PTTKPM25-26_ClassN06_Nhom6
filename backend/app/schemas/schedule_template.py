from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ScheduleTemplateBase(BaseModel):
    course_class_id: int = Field(..., description="ID của lớp học")
    room_id: int = Field(..., description="ID phòng học")
    period_id: int = Field(..., description="ID ca học")

class ScheduleTemplateCreate(ScheduleTemplateBase):
    pass

class ScheduleTemplateUpdate(ScheduleTemplateBase):
    course_class_id: Optional[int] = Field(None, description="ID của lớp học")
    room_id: Optional[int] = Field(None, description="ID phòng học")
    period_id: Optional[int] = Field(None, description="ID ca học")

class ScheduleTemplate(ScheduleTemplateBase):
    template_id: int = Field(..., alias="templateId", description="ID của mẫu lịch")
    created_at: datetime = Field(..., alias="createdAt", description="Thời gian tạo")
    updated_at: datetime = Field(..., alias="updatedAt", description="Thời gian cập nhật")
    day_of_week: int = Field(..., alias="dayOfWeek", description="Thứ trong tuần (1=Thứ Hai, 7=Chủ Nhật)")
    class Config:
        from_attributes = True
        populate_by_name = True

class WeeklyScheduleRequest(BaseModel):
    program_id: int = Field(..., description="ID chương trình đào tạo")
    semester_id: Optional[int] = Field(None, description="ID học kỳ (nếu không có sẽ lấy học kỳ hiện tại)")
    total_weeks: int = Field(10, description="Tổng số tuần trong học kỳ", ge=1, le=20)

class SemesterScheduleResponse(BaseModel):
    message: str
    template_info: dict
    semester_info: dict