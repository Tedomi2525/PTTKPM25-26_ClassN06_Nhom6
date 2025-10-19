import os
import numpy as np
import faiss
import cv2
import time
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas import schedule, user

# Set environment variable để tránh lỗi OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from app.services.face_service.embedding.face_embedding import get_face_embedding
from app.models.student_faces import StudentFace 
from app.models.student import Student
from app.models.course_class import CourseClass
from app.models.attendance import Attendance
from app.models.schedule import Schedule
from app.models.enrollment import Enrollment

FAISS_INDEX_PATH = "face.index"
RECOGNITION_THRESHOLD = 0.6  # ngưỡng khớp (càng nhỏ càng khớp, L2 distance)
CAMERA_TIMEOUT = 15  # thời gian tối đa quét camera (giây)

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

def search_face_by_image(image_content: bytes, schedule_id: int, db: Session):
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

    if is_match:
        attendance = Attendance(
            student_id=student.student_id,
            schedule_id=schedule_id,
            date=datetime.now().date(),
            status="present",
            confirmed_at=datetime.now(),
            confirmed_by=1
        )
        db.add(attendance)
        db.commit()

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


def search_face_by_camera(schedule_id: int, db: Session, timeout: int = CAMERA_TIMEOUT):
    """
    Tìm kiếm sinh viên qua camera realtime
    
    Args:
        schedule_id: ID lịch học để lưu điểm danh
        db: Database session
        timeout: Thời gian tối đa quét camera (giây)
        
    Returns:
        dict: Thông tin sinh viên khớp hoặc thông báo không tìm thấy
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Không thể truy cập camera. Kiểm tra kết nối camera.")
    print(f"[CAMERA] Camera opened successfully.")
    start_time = time.time()
    found_student = None
    frame_count = 0
    
    try:
        # Load FAISS index
        index = load_faiss_index()
        
        print(f"[CAMERA] Bắt đầu quét camera trong {timeout} giây...")
        
        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            if not ret:
                print("[CAMERA] Không đọc được frame từ camera")
                continue
            
            frame_count += 1
            
            # Chỉ xử lý mỗi 5 frames để tăng hiệu suất
            if frame_count % 5 != 0:
                continue
            
            try:
                # Chuyển frame sang bytes
                _, buffer = cv2.imencode('.jpg', frame)
                image_bytes = buffer.tobytes()
                
                # Lấy embedding từ frame
                embedding = get_face_embedding(image_bytes)
                if embedding is None:
                    continue
                
                # Chuẩn hóa embedding
                embedding = np.array(embedding, dtype=np.float32).flatten()
                norm = np.linalg.norm(embedding)
                if norm == 0:
                    continue
                embedding /= norm
                
                query_vector = embedding.reshape(1, -1)
                
                # Tìm kiếm trong FAISS
                D, I = index.search(query_vector, k=1)
                distance = float(np.sqrt(D[0][0]))
                faiss_idx = int(I[0][0])
                
                print(f"[CAMERA] Frame {frame_count}: Distance={distance:.4f}, Threshold={RECOGNITION_THRESHOLD}")
                
                # Kiểm tra ngưỡng
                if distance >= RECOGNITION_THRESHOLD:
                    continue
                
                # Tìm student từ faiss_index
                embedding_match = db.query(StudentFace).filter(StudentFace.faiss_index == faiss_idx).first()
                if not embedding_match:
                    continue
                
                student = db.query(Student).filter(Student.student_id == embedding_match.student_id).first()
                if not student:
                    continue
                
                # Tìm thấy sinh viên khớp!
                confidence = max(0, min(100, (1 - distance) * 100))
                
                # Lưu điểm danh nếu có schedule_id
                if schedule_id:
                    attendance = Attendance(
                        student_id=student.student_id,
                        schedule_id=schedule_id,
                        date=datetime.now().date(),
                        status="present",
                        confirmed_at=datetime.now(),
                        confirmed_by=1
                    )
                    db.add(attendance)
                    db.commit()
                
                found_student = {
                    "matched": True,
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
                        "faiss_index": faiss_idx,
                        "frames_processed": frame_count
                    },
                    "message": "✅ Nhận diện thành công qua camera!"
                }
                
                print(f"[CAMERA] ✅ Tìm thấy: {student.student_code} - {student.last_name} {student.first_name}")
                break
                
            except Exception as e:
                print(f"[CAMERA] Lỗi xử lý frame {frame_count}: {str(e)}")
                continue
        
        cap.release()
        
        if found_student:
            return found_student
        else:
            elapsed_time = round(time.time() - start_time, 2)
            return {
                "matched": False,
                "message": f"❌ Không phát hiện sinh viên nào trong {elapsed_time}s (processed {frame_count} frames)",
                "recognition_details": {
                    "frames_processed": frame_count,
                    "elapsed_time": elapsed_time,
                    "threshold": RECOGNITION_THRESHOLD
                }
            }
    
    except ValueError as ve:
        cap.release()
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        cap.release()
        print(f"[CAMERA] Lỗi không mong đợi: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi camera: {str(e)}")

def get_attendance_status(schedule_id: int, db: Session):
    """
    Lấy danh sách trạng thái điểm danh của tất cả sinh viên trong lớp học
    
    Args:
        schedule_id: ID lịch học
        db: Database session
        
    Returns:
        dict: Danh sách sinh viên và trạng thái điểm danh
    """
    try:
        # Lấy thông tin lịch học và lớp
        schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch học")
        
        # Lấy danh sách sinh viên trong lớp
        students = db.query(Student).join(
            Enrollment, Student.student_id == Enrollment.student_id
        ).filter(Enrollment.class_id == schedule.class_id).all()
        
        # Lấy danh sách điểm danh của ngày hôm nay
        today = datetime.now().date()
        attendances = db.query(Attendance).filter(
            Attendance.schedule_id == schedule_id,
            Attendance.date == today
        ).all()
        
        # Tạo dict để tra cứu nhanh trạng thái điểm danh
        attendance_dict = {att.student_id: att for att in attendances}
        
        # Tạo danh sách kết quả
        attendance_list = []
        for student in students:
            attendance = attendance_dict.get(student.student_id)
            
            student_data = {
                "student_id": student.student_id,
                "student_code": student.student_code,
                "full_name": f"{student.last_name} {student.first_name}",
                "email": student.email,
                "avatar": student.avatar,
                "status": attendance.status if attendance else "absent",
                "confirmed_at": attendance.confirmed_at.isoformat() if attendance and attendance.confirmed_at else None,
                "confirmed_by": attendance.confirmed_by if attendance else None
            }
            attendance_list.append(student_data)
        
        # Thống kê
        total_students = len(students)
        present_count = len([att for att in attendances if att.status == "present"])
        absent_count = total_students - present_count
        attendance_rate = round((present_count / total_students * 100), 2) if total_students > 0 else 0
        
        return {
            "schedule_id": schedule_id,
            "date": today.isoformat(),
            "class_info": {
                "class_id": schedule.class_id,
                "class_name": schedule.course_class.class_name if schedule.course_class else None
            },
            "statistics": {
                "total_students": total_students,
                "present_count": present_count,
                "absent_count": absent_count,
                "attendance_rate": attendance_rate
            },
            "attendance_list": attendance_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy trạng thái điểm danh: {str(e)}")

def get_attendance_status_by_schedule_and_student(schedule_id: int, student_id: int, db: Session):
    """
    Lấy trạng thái điểm danh của một sinh viên trong một lịch học cụ thể
    
    Args:
        schedule_id: ID lịch học
        student_id: ID sinh viên
        db: Database session
        
    Returns:
        dict: Thông tin trạng thái điểm danh của sinh viên
    """
    try:
        attendance = db.query(Attendance).filter(
            Attendance.schedule_id == schedule_id,
            Attendance.student_id == student_id
        ).first()
        
        if not attendance:
            return {
                "student_id": student_id,
                "schedule_id": schedule_id,
                "status": "absent",
                "confirmed_at": None,
                "confirmed_by": None
            }
        
        return {
            "student_id": student_id,
            "schedule_id": schedule_id,
            "status": attendance.status,
            "confirmed_at": attendance.confirmed_at.isoformat() if attendance.confirmed_at else None,
            "confirmed_by": attendance.confirmed_by
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy trạng thái điểm danh: {str(e)}")
