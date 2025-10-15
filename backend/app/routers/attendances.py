from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import attendance_service

router = APIRouter()

@router.post("/attendances/face-recognition", summary="Nhận diện khuôn mặt sinh viên")
async def recognize_face(
    file: UploadFile = File(..., description="Ảnh khuôn mặt sinh viên"),
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
        result = attendance_service.search_face_by_image(image_content, db)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in face recognition endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")