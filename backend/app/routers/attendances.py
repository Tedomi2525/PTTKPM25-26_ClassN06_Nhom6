from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import attendance_service

router = APIRouter()

@router.post("/attendances/face-recognition", summary="Nhận diện khuôn mặt sinh viên qua ảnh")
async def recognize_face(
    file: UploadFile = File(..., description="Ảnh khuôn mặt sinh viên"),
    schedule_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Nhận diện sinh viên qua ảnh khuôn mặt
    
    - **file**: File ảnh chứa khuôn mặt (JPG, PNG)
    - Trả về thông tin sinh viên nếu khớp
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File phải là ảnh (JPG, PNG, etc.)")
    
    try:
        # Read file content
        image_content = await file.read()
        
        # Process face recognition
        result = attendance_service.search_face_by_image(image_content, schedule_id, db)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in face recognition endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")


@router.post("/attendances/face-recognition-camera", summary="Nhận diện khuôn mặt sinh viên qua camera")
def recognize_face_camera(
    schedule_id: int = None,
    timeout: int = 15,
    db: Session = Depends(get_db)
):
    """
    Nhận diện sinh viên qua camera realtime
    
    - **schedule_id**: ID lịch học để lưu điểm danh
    - **timeout**: Thời gian tối đa quét camera (giây), mặc định 15s
    - Camera sẽ tự động quét và nhận diện khuôn mặt
    - Trả về thông tin sinh viên ngay khi tìm thấy
    """
    try:
        result = attendance_service.search_face_by_camera(schedule_id, db, timeout)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in camera recognition endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")
    
@router.get("/attendances/getStatus", summary="Lấy thông tin điểm danh theo ID")
def get_attendance_status(
    student_id: int,
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin điểm danh theo ID
    
    - **attendance_id**: ID điểm danh
    - Trả về thông tin điểm danh
    """
    try:
        result = attendance_service.get_attendance_status_by_schedule_and_student(schedule_id, student_id, db)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get attendance status endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")
    
@router.get("/attendances/status-by-schedule", summary="Lấy danh sách điểm danh theo lịch học")
def get_attendance_status_by_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách điểm danh của tất cả sinh viên theo lịch học

    - **schedule_id**: ID lịch học
    - Trả về danh sách thông tin điểm danh
    """
    try:
        result = attendance_service.get_attendance_status(schedule_id, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get attendance status by schedule endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")
    
@router.post("/attendances/mark", summary="Ghi nhận điểm danh cho sinh viên")
def mark_attendance(
    schedule_id: int,
    student_id: int,
    status: str,
    confirmed_by: int = 1,  # ví dụ: ID giảng viên, tạm mặc định
    db: Session = Depends(get_db)
):
    """
    Ghi nhận điểm danh cho sinh viên.
    - Nếu status='present' → thêm/cập nhật.
    - Nếu status='absent' → xóa bản ghi.
    """
    try:
        return attendance_service.mark_attendance(schedule_id, student_id, status, confirmed_by, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")