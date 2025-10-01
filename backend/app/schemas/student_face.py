from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ----- Base Schema -----
class StudentFaceBase(BaseModel):
    student_id: int
    is_primary: Optional[bool] = False
    faiss_index: Optional[int] = None


# ----- Schema khi tạo mới -----
class StudentFaceCreate(StudentFaceBase):
    # embedding_vector dạng bytes để lưu vào DB (LargeBinary)
    embedding_vector: bytes


# ----- Schema khi update -----
class StudentFaceUpdate(BaseModel):
    student_id: Optional[int] = None
    embedding_vector: Optional[bytes] = None
    is_primary: Optional[bool] = None
    faiss_index: Optional[int] = None


# ----- Schema trả ra khi đọc -----
class StudentFaceOut(StudentFaceBase):
    face_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
