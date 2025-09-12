from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.program import ProgramCreate, ProgramUpdate, Program as ProgramSchema
from app.database import SessionLocal
from app.services import program_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/programs", response_model=list[ProgramSchema])
def get_programs(db: Session = Depends(get_db)):
    return program_service.get_programs(db)

@router.get("/programs/search", response_model=list[ProgramSchema])
def search_programs(q: str, db: Session = Depends(get_db)):
    return program_service.search_programs(db, q)

@router.post("/programs", response_model=ProgramSchema)
def create_program(payload: ProgramCreate, db: Session = Depends(get_db)):
    return program_service.create_program(db, payload)

@router.put("/programs/{program_id}", response_model=ProgramSchema)
def update_program(program_id: int, payload: ProgramUpdate, db: Session = Depends(get_db)):
    program = program_service.update_program(db, program_id, payload)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.delete("/programs/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    success = program_service.delete_program(db, program_id)
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}
