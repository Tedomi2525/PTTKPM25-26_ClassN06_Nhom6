from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import schedule_service
from typing import Optional

router = APIRouter()

@router.get("/debug/{program_id}")
def debug_schedule_data(
    program_id: int,
    db: Session = Depends(get_db)
):
    """Debug endpoint để kiểm tra dữ liệu cho schedule generation"""
    try:
        from app.models.program import Program
        from app.models.course import Course
        from app.models.course_class import CourseClass
        from app.models.room import Room
        from app.models.period import Period
        from app.models.semester import Semester
        from app.models.program_course import ProgramCourse
        
        debug_info = {}
        
        # 1. Kiểm tra program
        program = db.query(Program).filter(Program.program_id == program_id).first()
        debug_info["program"] = {
            "exists": program is not None,
            "current_semester": program.current_semester if program else None,
            "program_name": program.program_name if program else None
        }
        
        # 2. Kiểm tra current semester
        current_semester = schedule_service.get_current_semester_for_program(db, program_id)
        debug_info["current_semester"] = current_semester
        
        # 3. Kiểm tra courses cho semester hiện tại
        courses = schedule_service.get_courses_for_current_semester(db, program_id)
        debug_info["courses"] = {
            "count": len(courses),
            "course_ids": [c.course_id for c in courses] if courses else [],
            "course_names": [c.name for c in courses] if courses else []
        }
        
        # 4. Kiểm tra course classes
        if courses:
            course_ids = [course.course_id for course in courses]
            course_classes = db.query(CourseClass).join(Course).filter(
                Course.course_id.in_(course_ids)
            ).all()
            debug_info["course_classes"] = {
                "count": len(course_classes),
                "class_ids": [cc.course_class_id for cc in course_classes],
                "with_teachers": [cc for cc in course_classes if cc.teacher_id]
            }
        else:
            debug_info["course_classes"] = {"count": 0, "class_ids": [], "with_teachers": []}
        
        # 5. Kiểm tra rooms
        rooms = db.query(Room).all()
        debug_info["rooms"] = {
            "count": len(rooms),
            "room_ids": [r.room_id for r in rooms]
        }
        
        # 6. Kiểm tra periods
        periods = db.query(Period).all()
        debug_info["periods"] = {
            "count": len(periods),
            "period_ids": [p.period_id for p in periods]
        }
        
        # 7. Kiểm tra semesters
        semesters = db.query(Semester).all()
        debug_info["semesters"] = {
            "count": len(semesters),
            "semester_ids": [s.semester_id for s in semesters]
        }
        
        # 8. Kiểm tra program_courses
        program_courses = db.query(ProgramCourse).filter(
            ProgramCourse.program_id == program_id
        ).all()
        debug_info["program_courses"] = {
            "count": len(program_courses),
            "semester_codes": list(set([pc.semester_no for pc in program_courses])),
            "courses_for_current": [pc.course_id for pc in program_courses if pc.semester_no == current_semester]
        }
        
        return {
            "success": True,
            "program_id": program_id,
            "debug_info": debug_info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "program_id": program_id
        }

@router.post("/generate")
def generate_schedule(
    program_id: int = Query(..., description="Program ID to generate schedule for"),
    semester_id: Optional[int] = Query(None, description="Semester ID (if not provided, uses latest semester)"),
    total_weeks: int = Query(10, description="Total weeks for the semester", ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Tự động tạo thời khóa biểu hoàn chỉnh cho học kỳ:
    1. Tạo template cho 1 tuần
    2. Generate lịch cho toàn bộ học kỳ (10 tuần mặc định)
    """
    try:
        result = schedule_service.generate_schedule(db, program_id, semester_id, total_weeks)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "success": True,
            "message": f"Successfully generated schedule for {total_weeks} weeks",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate schedule: {str(e)}")
