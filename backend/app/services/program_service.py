from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.program import Program as ProgramModel
from app.schemas.program import ProgramCreate, ProgramUpdate

def get_programs(db: Session):
    return db.query(ProgramModel).all()

def search_programs(db: Session, q: str):
    q_clean = q.replace(" ", "").lower()
    return db.query(ProgramModel).filter(
        func.replace(func.unaccent(func.lower(ProgramModel.program_name)), " ", "")
        .ilike(f"%{q_clean}%")
    ).all()

def create_program(db: Session, payload: ProgramCreate):
    new_program = ProgramModel(**payload.dict())
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program

def update_program(db: Session, program_id: int, payload: ProgramUpdate):
    program = db.query(ProgramModel).filter(ProgramModel.id == program_id).first()
    if not program:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(program, key, value)
    db.commit()
    db.refresh(program)
    return program

def delete_program(db: Session, program_id: int):
    program = db.query(ProgramModel).filter(ProgramModel.program_id == program_id).first()
    if not program:
        return None
    db.delete(program)
    db.commit()
    return True
