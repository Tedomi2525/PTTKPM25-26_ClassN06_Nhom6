from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.room import RoomCreate, RoomUpdate, Room as RoomSchema
from app.database import SessionLocal
from app.services import room_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rooms", response_model=list[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    return room_service.get_rooms(db)

@router.get("/rooms/search", response_model=list[RoomSchema])
def search_rooms(q: str, db: Session = Depends(get_db)):
    return room_service.search_rooms(db, q)

@router.post("/rooms", response_model=RoomSchema)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db, payload)

@router.put("/rooms/{room_id}", response_model=RoomSchema)
def update_room(room_id: int, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = room_service.update_room(db, room_id, payload)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    success = room_service.delete_room(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}
