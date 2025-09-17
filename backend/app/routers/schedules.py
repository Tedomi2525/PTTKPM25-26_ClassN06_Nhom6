from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import schedule_service
from typing import Optional

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
