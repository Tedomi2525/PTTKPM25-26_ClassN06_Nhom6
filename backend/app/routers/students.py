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

# ==============================================================================
# ENDPOINT THÊM SINH VIÊN (HỖ TRỢ FILE UPLOAD)
# ==============================================================================
@router.post("/students", response_model=StudentSchema, status_code=201)
async def create_student_with_avatar(
    # Data Fields (Form) - Sử dụng alias để khớp với tên trường trong StudentBase (ví dụ: firstName -> first_name)
    firstName: Annotated[str, Form(..., alias="firstName")],
    lastName: Annotated[str, Form(..., alias="lastName")],
    dob: Annotated[str, Form(..., alias="dob")], # Nhận string, Pydantic sẽ chuyển thành date
    gender: Annotated[str, Form(..., alias="gender")],
    email: Annotated[str, Form(..., alias="email")],
    phone: Annotated[str, Form(..., alias="phone")],
    
    # Optional Data Fields
    studentCode: Annotated[Optional[str], Form(alias="studentCode")] = None,
    className: Annotated[Optional[str], Form(alias="className")] = None,
    userId: Annotated[Optional[int], Form(alias="userId")] = 0,
    trainingProgram: Annotated[Optional[str], Form(alias="trainingProgram")] = None,
    courseYears: Annotated[Optional[str], Form(alias="courseYears")] = None,
    educationType: Annotated[Optional[str], Form(alias="educationType")] = None,
    faculty: Annotated[Optional[str], Form(alias="faculty")] = None,
    major: Annotated[Optional[str], Form(alias="major")] = None,
    status: Annotated[Optional[str], Form(alias="status")] = None,
    position: Annotated[Optional[str], Form(alias="position")] = None,
    
    # File Field
    avatar_file: Annotated[Optional[UploadFile], File(alias="avatar")] = None, # Đổi tên biến để tránh xung đột
    db: Session = Depends(get_db)
):
    avatar_url = None
    
    # 1. LƯU FILE ẢNH VÀO FOLDER TRÊN SERVER
    if avatar_file and avatar_file.filename:
        try:
            file_extension = os.path.splitext(avatar_file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as buffer:
                # Sao chép nội dung file từ upload buffer vào file vật lý
                shutil.copyfileobj(avatar_file.file, buffer)
            
            # Tạo đường dẫn URL công khai để lưu vào DB
            avatar_url = f"/static/avatars/{unique_filename}"
            
        except Exception as e:
            print(f"Error saving avatar file: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi lưu tệp ảnh trên server.")
    
    # 2. TẠO DICT DỮ LIỆU ĐỂ KHỞI TẠO STUDENTCREATE
    student_payload_dict = {
        "studentCode": studentCode,
        "firstName": firstName,
        "lastName": lastName,
        "dob": dob,
        "gender": gender,
        "email": email,
        "phone": phone,
        "className": className,
        "userId": userId,
        "trainingProgram": trainingProgram,
        "courseYears": courseYears,
        "educationType": educationType,
        "faculty": faculty,
        "major": major,
        "status": status,
        "position": position,
        "avatar": avatar_url # Đường dẫn string đã được lưu
    }
    
    try:
        # Pydantic sẽ xử lý ánh xạ alias (camelCase -> snake_case) và validation
        # Ví dụ: "firstName" được ánh xạ thành first_name
        student_payload = StudentCreate(**student_payload_dict)
    except Exception as e:
        # Lỗi Pydantic validation (422)
        print(f"Pydantic Validation Error: {e}")
        raise HTTPException(status_code=422, detail=f"Lỗi validation dữ liệu: {str(e)}")

    # 3. GỌI SERVICE LAYER
    try:
        return student_service.create_student(db, student_payload)
    except ValueError as e:
        # Lỗi nghiệp vụ (Email đã tồn tại, check constraint)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in create_student endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server nội bộ: {str(e)}")
# ==============================================================================

@router.get("/students/{student_id}", response_model=StudentSchema)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

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