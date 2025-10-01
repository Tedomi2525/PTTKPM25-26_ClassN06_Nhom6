import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from app.schemas import student
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from face_service.embedding.face_embedding import get_face_embedding
from app.models.student_faces import StudentFace 
from app.models.user import User
from app.models.student import Student
import numpy as np
import faiss

app = FastAPI(title="Face Recognition API")

FAISS_INDEX_PATH = "face_service/face.index"
RECOGNITION_THRESHOLD = 0.9  # ngưỡng khớp

def load_faiss_index():
    if not os.path.exists(FAISS_INDEX_PATH):
        raise ValueError("Không tìm thấy file FAISS index.")
    return faiss.read_index(FAISS_INDEX_PATH)

@app.post("/search")
async def search_face(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        image = await file.read()
        embedding = get_face_embedding(image)
        if embedding is None:
            raise ValueError("Không phát hiện khuôn mặt.")

        embedding = np.array(embedding, dtype=np.float32).flatten()
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Embedding không hợp lệ.")
        embedding /= norm
        query_vector = embedding.reshape(1, -1)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi tạo embedding: {str(e)}")

    try:
        index = load_faiss_index()
        D, I = index.search(query_vector, k=1)
        distance = float(np.sqrt(D[0][0]))
        idx = int(I[0][0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi FAISS: {str(e)}")

    # ⚠️ Tìm theo faiss_index thay vì index_in_faiss
    embedding_match = db.query(StudentFace).filter(StudentFace.faiss_index == idx).first()
    if not embedding_match:
        raise HTTPException(status_code=404, detail="Không tìm thấy user ứng với embedding.")

    user = db.query(Student).filter(Student.student_id == embedding_match.student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin người dùng.")

    is_match = distance < RECOGNITION_THRESHOLD

    return {
        "matched_user_id": user.student_code,
        "username": user.last_name + " " + user.first_name,
        "distance": round(distance, 4),
        "is_match": is_match,
        "message": "✅ Khớp người dùng!" if is_match else "❌ Không khớp người dùng nào."
    }




