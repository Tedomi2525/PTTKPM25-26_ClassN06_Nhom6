import os
import numpy as np
import faiss
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.face_service.embedding.face_embedding import get_face_embedding
from app.models.student_faces import StudentFace 
from app.models.student import Student

FAISS_INDEX_PATH = "face.index"
RECOGNITION_THRESHOLD = 0.6  # ngưỡng khớp (càng nhỏ càng khớp, L2 distance)

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def load_faiss_index():
    """Load FAISS index từ file"""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise ValueError("Không tìm thấy file FAISS index. Vui lòng tạo ít nhất một sinh viên trước.")
    return faiss.read_index(FAISS_INDEX_PATH)

# ==============================================================================
# FACE RECOGNITION SERVICES
# ==============================================================================

def search_face_by_image(image_content: bytes, db: Session):
    """
    Tìm kiếm sinh viên qua ảnh khuôn mặt
    
    Args:
        image_content: Nội dung file ảnh dạng bytes
        db: Database session
        
    Returns:
        dict: Thông tin sinh viên khớp và độ tương đồng
    """
    # 1. Tạo embedding từ ảnh
    try:
        embedding = get_face_embedding(image_content)
        if embedding is None:
            raise ValueError("Không phát hiện khuôn mặt trong ảnh.")

        # Chuẩn hóa embedding
        embedding = np.array(embedding, dtype=np.float32).flatten()
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Embedding không hợp lệ.")
        embedding /= norm
        
        query_vector = embedding.reshape(1, -1)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý ảnh: {str(e)}")

    # 2. Tìm kiếm trong FAISS index
    try:
        index = load_faiss_index()
        
        # Tìm k=1 kết quả gần nhất
        D, I = index.search(query_vector, k=1)
        
        # D[0][0] là khoảng cách L2 bình phương, cần sqrt
        distance = float(np.sqrt(D[0][0]))
        faiss_idx = int(I[0][0])
        
        print(f"FAISS search result - Index: {faiss_idx}, Distance: {distance}")
        
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tìm kiếm FAISS: {str(e)}")

    # 3. Tìm student face record từ faiss_index
    embedding_match = db.query(StudentFace).filter(StudentFace.faiss_index == faiss_idx).first()
    if not embedding_match:
        raise HTTPException(
            status_code=404, 
            detail=f"Không tìm thấy embedding tương ứng với FAISS index {faiss_idx}."
        )

    # 4. Tìm thông tin sinh viên
    student = db.query(Student).filter(Student.student_id == embedding_match.student_id).first()
    if not student:
        raise HTTPException(
            status_code=404, 
            detail=f"Không tìm thấy sinh viên với ID {embedding_match.student_id}."
        )

    # 5. Kiểm tra ngưỡng khớp
    is_match = distance < RECOGNITION_THRESHOLD
    confidence = max(0, min(100, (1 - distance) * 100))  # Chuyển thành % confidence

    return {
        "matched": is_match,
        "student": {
            "student_id": student.student_id,
            "student_code": student.student_code,
            "full_name": f"{student.last_name} {student.first_name}",
            "email": student.email,
            "avatar": student.avatar
        },
        "recognition_details": {
            "distance": round(distance, 4),
            "confidence": round(confidence, 2),
            "threshold": RECOGNITION_THRESHOLD,
            "faiss_index": faiss_idx
        },
        "message": "✅ Nhận diện thành công!" if is_match else f"⚠️ Độ tương đồng thấp (distance: {distance:.4f} >= threshold: {RECOGNITION_THRESHOLD})"
    }




