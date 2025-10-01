from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProgramBase(BaseModel):
    program_name: str = Field(..., alias="programName", max_length=150, description="Program name")
    department: Optional[str] = Field(None, alias="department", max_length=100, description="Department offering the program")
    start_year: int = Field(..., alias="startYear", ge=1900, le=2100, description="Start year of the program")
    duration: Optional[int] = Field(None, alias="duration", ge=1, le=10, description="Duration of the program in years")
    current_semester: Optional[str] = Field(None, alias="currentSemester", max_length=10, description="Current semester code")
    
    class Config:
        populate_by_name = True

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    program_name: Optional[str] = Field(None, alias="programName", max_length=150, description="Program name")
    department: Optional[str] = Field(None, alias="department", max_length=100, description="Department offering the program")
    start_year: Optional[int] = Field(None, alias="startYear", ge=1900, le=2100, description="Start year of the program")
    duration: Optional[int] = Field(None, alias="duration", ge=1, le=10, description="Duration of the program in years")
    current_semester: Optional[str] = Field(None, alias="currentSemester", max_length=10, description="Current semester code")
    
    class Config:
        populate_by_name = True

class Program(ProgramBase):
    program_id: int = Field(..., alias="programId", description="Program ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True