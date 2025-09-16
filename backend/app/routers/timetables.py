from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import timetable_service
from typing import Optional

router = APIRouter()

@router.get("/timetables")
def get_timetables(
    program_id: Optional[int] = Query(None, description="Filter timetables by program ID to show only current semester courses"),
    db: Session = Depends(get_db)
):
    """
    Get timetables with optional program filtering.
    
    If program_id is provided, only courses for the current semester of that program will be included.
    The current semester is determined based on:
    - Program creation date
    - Latest semester start time
    - Semester rules: ≤4 months = semester 1, 5-8 months = semester 2, 9-12 months = semester 3
    """
    return timetable_service.get_timetables(db, program_id)