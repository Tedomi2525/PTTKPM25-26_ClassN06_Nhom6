from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import schedule_service
from typing import Optional

router = APIRouter()

@router.post("/generate")
def generate_schedule(
    program_id: int = Query(..., description="Program ID to generate schedule for"),
    db: Session = Depends(get_db)
):
    return schedule_service.generate_schedule(db, program_id)

@router.get("/schedules")
def get_schedule(
    program_id: Optional[int] = Query(None, description="Filter schedule by program ID to show only current semester courses"),
    db: Session = Depends(get_db)
):
    return schedule_service.get_schedule(db, program_id)