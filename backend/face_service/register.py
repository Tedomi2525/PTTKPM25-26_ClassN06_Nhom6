import os
import shutil
import numpy as np
import faiss
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Import các module trong project
from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.models.student_faces import StudentFace
from face_service.embedding.face_embedding import get_face_embedding

# ----------- Cấu hình cơ bản -----------
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

FAISS_INDEX_PATH = "face_service/face.index"
IMAGE_DIR = "images/students"  # Thư mục lưu ảnh
os.makedirs(IMAGE_DIR, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

app = FastAPI(title="Face Registration with Student Creation")

# ----------- Middleware CORS -----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------- Response Model -----------
class RegisterResult(BaseModel):
    student_id: int
    student_code: str
    avatar: str
    status: str


# ----------- Xử lý Student + User -----------
def get_or_create_student(
    db: Session,
    student_code: str,
    first_name: str,
    last_name: str,
    dob: datetime = None,
    gender: str = None,
    email: str = None,
    phone: str = None,
    class_name: str = None,
    training_program: str = None,
    course_years: str = None,
    education_type: str = None,
    faculty: str = None,
    major: str = None,
    status: str = "Đang học",
    position: str = None,
    avatar: str = None
) -> Student:
    """
    Kiểm tra student đã tồn tại chưa.
    Nếu chưa có -> tạo mới User và Student
    """
    # Kiểm tra student tồn tại
    student = db.query(Student).filter(Student.student_code == student_code).first()
    if student:
        return student

    # 1. Sinh mật khẩu mặc định
    default_password = f"{student_code}@123"
    hashed_password = pwd_context.hash(default_password)

    # 2. Tạo User trước
    new_user = User(
        username=student_code,
        password=hashed_password,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. Tạo Student
    new_student = Student(
        student_code=student_code,
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        gender=gender,
        email=email,
        phone=phone,
        class_name=class_name,
        training_program=training_program,
        course_years=course_years,
        education_type=education_type,
        faculty=faculty,
        major=major,
        status=status,
        position=position,
        avatar=avatar,
        user_id=new_user.user_id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# ----------- FAISS Index -----------
def load_or_create_faiss_index(d: int) -> faiss.Index:
    """Load FAISS index nếu có, nếu chưa thì tạo mới"""
    if os.path.exists(FAISS_INDEX_PATH):
        return faiss.read_index(FAISS_INDEX_PATH)
    return faiss.IndexFlatL2(d)


def save_faiss_index(index: faiss.Index):
    """Lưu FAISS index ra file"""
    faiss.write_index(index, FAISS_INDEX_PATH)


# ----------- API Đăng ký -----------
@app.post("/register", response_model=RegisterResult)
async def register_face(
    student_code: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    dob: str = Form(None),               # format: YYYY-MM-DD
    gender: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    class_name: str = Form(None),
    training_program: str = Form(None),
    course_years: str = Form(None),
    education_type: str = Form(None),
    faculty: str = Form(None),
    major: str = Form(None),
    status: str = Form("Đang học"),
    position: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    API đăng ký sinh viên:
    1. Lưu ảnh
    2. Lấy embedding khuôn mặt
    3. Lưu vào FAISS
    4. Lưu Student + User + StudentFace vào DB
    """

    # ---------- 1. Lưu ảnh ----------
    try:
        file_ext = os.path.splitext(file.filename)[1]  # .jpg / .png
        saved_filename = f"{student_code}{file_ext}"
        saved_path = os.path.join(IMAGE_DIR, saved_filename)

        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        avatar_path = f"images/students/{saved_filename}"  # lưu path tương đối
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    # ---------- 2. Lấy embedding từ ảnh ----------
    try:
        with open(saved_path, "rb") as img_file:
            content = img_file.read()
        emb = get_face_embedding(content)
        if emb is None or len(emb) == 0:
            raise ValueError("Face not detected")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Face embedding error: {str(e)}")

    # Chuẩn hóa vector
    emb = np.array(emb, dtype=np.float32).flatten()
    emb /= np.linalg.norm(emb)

    # ---------- 3. Thêm vào FAISS ----------
    index = load_or_create_faiss_index(len(emb))
    index.add(np.expand_dims(emb, axis=0))
    faiss_index = index.ntotal - 1  # vị trí mới thêm vào
    save_faiss_index(index)

    # ---------- 4. Lưu Student + User ----------
    dob_parsed = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None

    student = get_or_create_student(
        db=db,
        student_code=student_code,
        first_name=first_name,
        last_name=last_name,
        dob=dob_parsed,
        gender=gender,
        email=email,
        phone=phone,
        class_name=class_name,
        training_program=training_program,
        course_years=course_years,
        education_type=education_type,
        faculty=faculty,
        major=major,
        status=status,
        position=position,
        avatar=avatar_path
    )

    # ---------- 5. Lưu embedding vào bảng student_faces ----------
    try:
        new_face = StudentFace(
            student_id=student.student_id,
            embedding_vector=emb.tobytes(),  # lưu numpy array thành nhị phân
            is_primary=True,  # ảnh đầu tiên làm ảnh chính
            faiss_index=faiss_index
        )
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving embedding to DB: {str(e)}")

    return RegisterResult(
        student_id=student.student_id,
        student_code=student.student_code,
        avatar=student.avatar,
        status="registered successfully"
    )
