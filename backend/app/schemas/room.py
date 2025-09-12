from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class RoomBase(BaseModel):
    name: str = Field(..., max_length=50, description="Room name")
    capacity: int = Field(..., gt=0, description="Room capacity")
    camera_stream_url: Optional[str] = Field(None, description="Camera stream URL", alias="cameraStreamUrl")

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="Room name")
    capacity: Optional[int] = Field(None, gt=0, description="Room capacity")
    camera_stream_url: Optional[str] = Field(None, description="Camera stream URL", alias="cameraStreamUrl")

class Room(RoomBase):
    room_id: int = Field(..., alias="roomId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
