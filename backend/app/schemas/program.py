from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProgramBase(BaseModel):
    program_name: str = Field(..., max_length=150, description="Program name", alias="programName")
    department: Optional[str] = Field(None, max_length=100, description="Department offering the program", alias="department")
    start_year: int = Field(..., ge=1900, le=2100, description="Start year of the program", alias="startYear")
    duration: Optional[int] = Field(None, ge=1, le=10, description="Duration of the program in years", alias="duration")
    current_semester: Optional[str] = Field(None, max_length=10, description="Current semester code", alias="currentSemester")

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    program_name: Optional[str] = Field(None, max_length=150, description="Program name", alias="programName")
    department: Optional[str] = Field(None, max_length=100, description="Department offering the program", alias="department")
    start_year: Optional[int] = Field(None, ge=1900, le=2100, description="Start year of the program", alias="startYear")
    duration: Optional[int] = Field(None, ge=1, le=10, description="Duration of the program in years", alias="duration")
    current_semester: Optional[str] = Field(None, max_length=10, description="Current semester code", alias="currentSemester")

class Program(ProgramBase):
    program_id: int = Field(..., alias="programId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True