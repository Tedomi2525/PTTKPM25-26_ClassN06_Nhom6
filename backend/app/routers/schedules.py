from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import schedule_service
from typing import Optional
from datetime import datetime, timedelta
from app.models import Schedule, CourseClass, Room, Period

router = APIRouter()

@router.post("/generate")
def generate_schedule(
    program_id: int = Query(..., description="Program ID to generate schedule for"),
    semester_id: Optional[int] = Query(None, description="Semester ID (if not provided, uses latest semester)"),
    total_weeks: int = Query(10, description="Total weeks for the semester", ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Tự động tạo thời khóa biểu hoàn chỉnh cho học kỳ:
    1. Tạo template cho 1 tuần
    2. Generate lịch cho toàn bộ học kỳ (10 tuần mặc định)
    """
    try:
        result = schedule_service.generate_schedule(db, program_id, semester_id, total_weeks)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "success": True,
            "message": f"Successfully generated schedule for {total_weeks} weeks",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate schedule: {str(e)}")
    
@router.get("/")
def get_schedules(
    semester_id: int = Query(..., description="Semester ID"),
    db: Session = Depends(get_db)
):
    try:
        schedules = (
            db.query(Schedule)
            .join(CourseClass)
            .join(Room)
            .join(Period, Schedule.period_start == Period.period_id)
            .filter(Schedule.semester_id == semester_id)
            .all()
        )

        result = []
        for s in schedules:
            # Giả sử mỗi tiết học kéo dài 50 phút, bắt đầu từ 6h45
            base_time = datetime.combine(s.specific_date, datetime.min.time()) + timedelta(hours=6, minutes=45)
            start_time = base_time + timedelta(minutes=50 * (s.period_start - 1))
            end_time = base_time + timedelta(minutes=50 * s.period_end)

            event = {
                "title": f"{s.course_class.course_class_name}\\nTiết {s.period_start}-{s.period_end}\\nPhòng {s.room.room_name}",
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "color": "#1e88e5"  # có thể chọn màu theo môn học
            }
            result.append(event)

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy thời khóa biểu: {str(e)}")
