from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.room import Room as RoomModel
from app.schemas.room import RoomCreate, RoomUpdate

def get_rooms(db: Session):
    return db.query(RoomModel).all()

def search_rooms(db: Session, q: str):
    return db.query(RoomModel).filter(
        or_(
            RoomModel.name.ilike(f"%{q}%"),
            RoomModel.camera_stream_url.ilike(f"%{q}%")
        )
    ).all()

def create_room(db: Session, payload: RoomCreate):
    new_room = RoomModel(**payload.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def update_room(db: Session, room_id: int, payload: RoomUpdate):
    room = db.query(RoomModel).filter(RoomModel.room_id == room_id).first()
    if not room:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_id: int):
    room = db.query(RoomModel).filter(RoomModel.room_id == room_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return True
