# student_face.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, LargeBinary, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class StudentFace(Base):
    __tablename__ = "student_faces"

    face_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    embedding_vector = Column(LargeBinary, nullable=True)  # lưu vector nhị phân
    is_primary = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    )
    faiss_index = Column(Integer, nullable=True)

    # Quan hệ với bảng students
    student = relationship("Student", back_populates="student_faces")
