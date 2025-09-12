from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.schemas.room import RoomCreate, RoomUpdate, Room as RoomSchema
from app.models.room import Room as RoomModel
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rooms", response_model=list[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    results = db.query(RoomModel).all()
    return results

@router.get("/rooms/search", response_model=list[RoomSchema])
def get_room(q: str, db: Session = Depends(get_db)):
    results = db.query(RoomModel).filter(
        or_(
            RoomModel.name.ilike(f"%{q}%"),
            RoomModel.camera_stream_url.ilike(f"%{q}%")
        )
    ).all()
    return results

@router.post("/rooms", response_model=RoomSchema)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    new_room = RoomModel(**payload.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.put("/rooms/{room_id}", response_model=RoomSchema)
def update_room(room_id: int, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}
