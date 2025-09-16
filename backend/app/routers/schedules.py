from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import schedule_service
from typing import Optional

router = APIRouter()

@router.get("/timetables")
def get_timetables(
    program_id: Optional[int] = Query(None, description="Filter timetables by program ID to show only current semester courses"),
    db: Session = Depends(get_db)
):
    return schedule_service.get_timetables(db, program_id)