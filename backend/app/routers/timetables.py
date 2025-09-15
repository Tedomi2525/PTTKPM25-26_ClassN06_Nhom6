from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import timetable_service

router = APIRouter()

@router.get("/timetables")
def get_timetables(db: Session = Depends(get_db)):
    return timetable_service.get_timetables(db)