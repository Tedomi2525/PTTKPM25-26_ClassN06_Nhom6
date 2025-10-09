from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional, Annotated
import os
import shutil
import uuid

# Đảm bảo bạn đã import StudentCreate và StudentUpdate từ file schema của bạn
from app.schemas.student import StudentCreate, StudentUpdate, Student as StudentSchema 
from app.database import get_db
from app.services import student_service 

# --- CONFIGURATION FOR FILE UPLOAD ---
# Đảm bảo thư mục tồn tại và được cấu hình trong main.py
UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# --- END CONFIGURATION ---

router = APIRouter()

@router.get("/students", response_model=list[StudentSchema])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_students(db)

@router.get("/students/search", response_model=list[StudentSchema])
def search_students(q: str, db: Session = Depends(get_db)):
    return student_service.search_students(db, q)

@router.post("/students", response_model=StudentSchema, status_code=201)
async def create_student_with_avatar(
    form_data: Annotated[StudentCreate, Depends(StudentCreate.as_form)],
    db: Session = Depends(get_db)
):
    avatar_url = None

    # Lưu file avatar (nếu có)
    if form_data.avatar_file and form_data.avatar_file.filename:
        try:
            ext = os.path.splitext(form_data.avatar_file.filename)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_name)
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(form_data.avatar_file.file, buffer)

            avatar_url = f"/static/avatars/{unique_name}"
        except Exception as e:
            print(f"Error saving avatar file: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi lưu tệp ảnh trên server.")

    # Cập nhật avatar_url nếu có
    data_dict = form_data.model_dump()
    data_dict["avatar"] = avatar_url or data_dict.get("avatar")
    data_dict.pop("avatar_file", None)

    try:
        student_obj = StudentCreate(**data_dict)
        return student_service.create_student(db, student_obj)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in create_student endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server nội bộ: {str(e)}")
    
@router.put("/students/{student_id}", response_model=StudentSchema)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        success = student_service.delete_student(db, student_id)
        if success is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"detail": "Student deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/students/weekly-schedule")
def get_student_weekly_schedule(
    student_id: int,
    sunday_date: str = Query(..., description="Ngày chủ nhật của tuần (DD/MM/YYYY hoặc YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Lấy lịch học của sinh viên trong tuần cụ thể
    """
    try:
        result = student_service.get_student_weekly_schedule(db, student_id, sunday_date)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {
            "success": True,
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get student weekly schedule: {str(e)}")