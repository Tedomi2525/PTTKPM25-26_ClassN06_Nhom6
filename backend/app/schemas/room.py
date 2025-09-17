from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RoomBase(BaseModel):
    room_name: str = Field(..., alias="roomName", max_length=50, description="Room name")
    capacity: int = Field(..., gt=0, description="Room capacity")
    camera_stream_url: Optional[str] = Field(None, alias="cameraStreamUrl", description="Camera stream URL")
    
    class Config:
        populate_by_name = True

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_name: Optional[str] = Field(None, alias="roomName", max_length=50, description="Room name")
    capacity: Optional[int] = Field(None, gt=0, description="Room capacity")
    camera_stream_url: Optional[str] = Field(None, alias="cameraStreamUrl", description="Camera stream URL")
    
    class Config:
        populate_by_name = True

class Room(RoomBase):
    room_id: int = Field(..., alias="roomId", description="Room ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True
