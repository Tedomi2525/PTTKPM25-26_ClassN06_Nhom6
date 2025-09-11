from fastapi import APIRouter
from app.schemas.test import InputData

router = APIRouter()

@router.post("/test")
def test_post(payload: InputData):
    return {"only_a": payload.a}
