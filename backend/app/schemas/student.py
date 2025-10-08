from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional
from enum import Enum

# ==============================================================================
# ENUMERATIONS
# ==============================================================================

class GenderEnum(str, Enum):
    MALE = "Nam"
    FEMALE = "Nữ"
    OTHER = "Khác"

class EducationTypeEnum(str, Enum):
    REGULAR = "Đại học chính quy"
    TRANSFER = "Liên thông"
    COLLEGE = "Cao đẳng"

class StatusEnum(str, Enum):
    STUDYING = "Đang học"
    ON_LEAVE = "Bảo lưu"
    GRADUATED = "Đã tốt nghiệp"

# ==============================================================================
# BASE SCHEMA
# ==============================================================================

class StudentBase(BaseModel):
    # Sử dụng alias để ánh xạ giữa camelCase (Frontend) và snake_case (Backend/DB)
    student_code: Optional[str] = Field(None, alias="studentCode", description="Student code")
    first_name: str = Field(..., alias="firstName", max_length=50, description="Student first name")
    last_name: str = Field(..., alias="lastName", max_length=100, description="Student last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[GenderEnum] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", max_length=20, description="Phone number")
    class_name: Optional[str] = Field(None, alias="className", max_length=50, description="Class name")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    training_program: Optional[str] = Field(None, alias="trainingProgram", max_length=50, description="Training program")
    course_years: Optional[str] = Field(None, alias="courseYears", max_length=20, description="Course years")
    education_type: Optional[EducationTypeEnum] = Field(None, alias="educationType", description="Education type")
    faculty: Optional[str] = Field(None, alias="faculty", max_length=100, description="Faculty")
    major: Optional[str] = Field(None, alias="major", max_length=100, description="Major")
    status: Optional[StatusEnum] = Field(None, alias="status", description="Student status")
    position: Optional[str] = Field(None, alias="position", max_length=50, description="Position")
    avatar: Optional[str] = Field(None, alias="avatar", max_length=255, description="Avatar URL")
    
    class Config:
        # Cho phép khởi tạo bằng cả tên trường snake_case (DB) và camelCase (alias)
        populate_by_name = True

# ==============================================================================
# CREATE SCHEMA
# ==============================================================================

class StudentCreate(StudentBase):
    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        
        # Gender mapping for different input formats
        gender_mapping = {
            "1": "Nam", "2": "Nữ", 
            "0": "Nam", "male": "Nam", "female": "Nữ",
            "nam": "Nam", "nữ": "Nữ",
            "khác": "Khác", "other": "Khác"
        }
        
        # Convert to string and normalize
        str_value = str(v).lower().strip()
        
        # Return mapped value if found, otherwise return original (let enum validation handle it)
        return gender_mapping.get(str_value, v)
    
    @field_validator(
        'class_name', 'training_program', 'course_years', 
        'faculty', 'major', 'position', 'avatar', # Thêm 'avatar' vào đây để loại bỏ chuỗi rỗng
        mode='before'
    )
    @classmethod
    def validate_string_fields(cls, v):
        # Nếu là None hoặc chuỗi rỗng, trả về None
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        # Nếu là string, loại bỏ khoảng trắng và trả về
        if isinstance(v, str):
            return v.strip()
        return v


# ==============================================================================
# UPDATE SCHEMA
# ==============================================================================

class StudentUpdate(BaseModel):
    # Các trường đều là Optional[T] vì đây là Update
    student_code: Optional[str] = Field(None, alias="studentCode", max_length=20, description="Student code")
    first_name: Optional[str] = Field(None, alias="firstName", max_length=50, description="Student first name")
    last_name: Optional[str] = Field(None, alias="lastName", max_length=100, description="Student last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[GenderEnum] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", max_length=20, description="Phone number")
    class_name: Optional[str] = Field(None, alias="className", max_length=50, description="Class name")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    training_program: Optional[str] = Field(None, alias="trainingProgram", max_length=50, description="Training program")
    course_years: Optional[str] = Field(None, alias="courseYears", max_length=20, description="Course years")
    education_type: Optional[EducationTypeEnum] = Field(None, alias="educationType", description="Education type")
    faculty: Optional[str] = Field(None, alias="faculty", max_length=100, description="Faculty")
    major: Optional[str] = Field(None, alias="major", max_length=100, description="Major")
    status: Optional[StatusEnum] = Field(None, alias="status", description="Student status")
    position: Optional[str] = Field(None, alias="position", max_length=50, description="Position")
    avatar: Optional[str] = Field(None, alias="avatar", max_length=255, description="Avatar URL")
    
    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        
        gender_mapping = {
            "1": "Nam", "2": "Nữ", 
            "0": "Nam", "male": "Nam", "female": "Nữ",
            "nam": "Nam", "nữ": "Nữ",
            "khác": "Khác", "other": "Khác"
        }
        
        str_value = str(v).lower().strip()
        return gender_mapping.get(str_value, v)
    
    @field_validator(
        'class_name', 'training_program', 'course_years', 
        'faculty', 'major', 'position', 'avatar',
        mode='before'
    )
    @classmethod
    def validate_string_fields(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        if isinstance(v, str):
            return v.strip()
        return v
    
    class Config:
        populate_by_name = True

# ==============================================================================
# RESPONSE SCHEMA
# ==============================================================================

class Student(StudentBase):
    student_id: int = Field(..., alias="studentId", description="Student ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        # Cần thiết cho SQLAlchemy ORM
        from_attributes = True 
        populate_by_name = True