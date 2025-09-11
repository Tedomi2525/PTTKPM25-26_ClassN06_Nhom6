from fastapi import APIRouter, Depends
from app.schemas.test import InputData
from app.database import SessionLocal
from app.models.semester import Semester

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_test")
def get_test(db=Depends(get_db)):
    data = db.query(Semester).all()
    return {"data": data} 

@router.post("/post_test")
def post_test(payload: InputData):
    return {"only_a": payload.a}
