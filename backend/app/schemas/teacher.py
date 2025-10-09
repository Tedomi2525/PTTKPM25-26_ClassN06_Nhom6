from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional

class TeacherBase(BaseModel):
    first_name: str = Field(..., alias="firstName", description="Teacher first name")
    last_name: str = Field(..., alias="lastName", description="Teacher last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[str] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", description="Phone number")
    department: Optional[str] = Field(None, alias="department", description="Department")
    faculty: Optional[str] = Field(None, alias="faculty", description="Faculty")
    specialization: Optional[str] = Field(None, alias="specialization", description="Specialization")
    degree: Optional[str] = Field(None, alias="degree", description="Academic degree")
    academic_rank: Optional[str] = Field(None, alias="academicRank", description="Academic rank")
    status: Optional[str] = Field("active", description="Status of the teacher, e.g., active or inactive")
    teacher_code: Optional[str] = Field(None, alias="teacherCode", description="Teacher code")
    
    class Config:
        populate_by_name = True

class TeacherCreate(TeacherBase):
    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        
        # Gender mapping for different input formats
        gender_mapping = {
            "1": "Nam",
            "2": "Nữ", 
            "0": "Nam",  # fallback
            "male": "Nam",
            "female": "Nữ",
            "nam": "Nam",
            "nữ": "Nữ"
        }
        
        # Convert to string and normalize
        str_value = str(v).lower().strip()
        
        # Return mapped value if found, otherwise return original
        return gender_mapping.get(str_value, v)
    
    @field_validator('degree', mode='before')
    @classmethod
    def validate_degree(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v.strip()
    
    @field_validator('academic_rank', mode='before')
    @classmethod
    def validate_academic_rank(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v.strip()
    
    @field_validator('department', 'faculty', 'specialization', mode='before')
    @classmethod
    def validate_string_fields(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v.strip()

class TeacherUpdate(BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName", description="Teacher first name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Teacher last name")
    dob: Optional[date] = Field(None, alias="dob", description="Date of birth")
    gender: Optional[str] = Field(None, alias="gender", description="Gender")
    email: Optional[EmailStr] = Field(None, alias="email", description="Email address")
    phone: Optional[str] = Field(None, alias="phone", description="Phone number")
    department: Optional[str] = Field(None, alias="department", description="Department")
    faculty: Optional[str] = Field(None, alias="faculty", description="Faculty")
    specialization: Optional[str] = Field(None, alias="specialization", description="Specialization")
    degree: Optional[str] = Field(None, alias="degree", description="Academic degree")
    academic_rank: Optional[str] = Field(None, alias="academicRank", description="Academic rank")
    status: Optional[str] = Field(None, description="Status of the teacher, e.g., active or inactive")
    teacher_code: Optional[str] = Field(None, alias="teacherCode", description="Teacher code")
    
    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        
        # Gender mapping for different input formats
        gender_mapping = {
            "1": "Nam",
            "2": "Nữ", 
            "0": "Nam",  # fallback
            "male": "Nam",
            "female": "Nữ",
            "nam": "Nam",
            "nữ": "Nữ"
        }
        
        # Convert to string and normalize
        str_value = str(v).lower().strip()
        
        # Return mapped value if found, otherwise return original
        return gender_mapping.get(str_value, v)
    
    @field_validator('degree', mode='before')
    @classmethod
    def validate_degree(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v.strip()
    
    @field_validator('academic_rank', mode='before')
    @classmethod
    def validate_academic_rank(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None
        return v.strip()
    
    class Config:
        populate_by_name = True

class Teacher(TeacherBase):
    teacher_id: int = Field(..., alias="teacherId", description="Teacher ID")
    user_id: Optional[int] = Field(None, alias="userId", description="Associated user ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True
