import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from typing import Optional

from app.models.student import Student as StudentModel
from app.models.user import User as UserModel
from app.models.enrollment import Enrollment
from app.models.schedule import Schedule
from app.models.course_class import CourseClass
from app.models.course import Course
from app.models.room import Room
from app.models.period import Period
from app.models.semester import Semester
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.user import UserCreate

from app.core.security import get_password_hash

def generate_student_code(db: Session) -> str:
    # Lấy student_code lớn nhất trong DB
    last_student = (
        db.query(StudentModel)
        .order_by(StudentModel.student_id.desc())
        .first()
    ) 
    if not last_student or not last_student.student_code:
        new_number = 1
    else:
        # Bóc số từ student_code, ví dụ SV000123 -> 123
        last_number = int(last_student.student_code.replace("SV", ""))
        new_number = last_number + 1

    return f"SV{new_number:06d}"  # padding 6 chữ số

def get_students(db: Session):
    return db.query(StudentModel).all()

def search_students(db: Session, q: str):
    return db.query(StudentModel).filter(
        or_(
            func.lower(StudentModel.first_name).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.last_name).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.email).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.student_code).like(func.lower(f"%{q}%"))
        ) 
    ).all()

def create_student(db: Session, student_payload: StudentCreate):
    try:
        # 1. Sinh student_code
        student_code = generate_student_code(db)

        # 2. Tạo user trước
        user_payload = UserCreate(
            username=student_code,
            school_email=f"{student_code}@edunera.edu",
            password=get_password_hash(f"{student_code}@"),
            role="student"
        )

        user_data = user_payload.model_dump(by_alias=False)
        new_user = UserModel(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 3. Tạo student, gán user_id - xử lý các field đặc biệt
        student_data = student_payload.model_dump(by_alias=False, exclude_unset=True)
        student_data["student_code"] = student_code
        student_data["user_id"] = new_user.user_id
        
        # Xử lý field class_name nếu có
        if "class_name" in student_data and student_data["class_name"] is None:
            student_data.pop("class_name")

        new_student = StudentModel(**student_data)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student
    
    except Exception as e:
        db.rollback()
        print(f"Error creating student: {e}")
        print(f"Student payload: {student_payload}")
        print(f"Student data: {student_data if 'student_data' in locals() else 'Not created yet'}")
        raise e
    
def update_student(db: Session, student_id: int, payload: StudentUpdate):
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None

    for key, value in payload.dict(exclude_unset=True, by_alias=False).items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error updating student: {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Error updating student: {e}")
        return None
    
def delete_student(db: Session, student_id: int):
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None
    try:
        db.delete(student)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False

def get_student_weekly_schedule(db: Session, student_id: int, sunday_date: str):
    """
    Lấy lịch học của sinh viên trong tuần cụ thể
    Args:
        student_id: ID của sinh viên
        sunday_date: Ngày chủ nhật của tuần (format: DD/MM/YYYY hoặc YYYY-MM-DD)
    """
    # Kiểm tra sinh viên có tồn tại không
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None
    
    try:
        # Parse ngày Chủ nhật
        if '/' in sunday_date:
            sunday = datetime.strptime(sunday_date, "%d/%m/%Y").date()
        else:
            sunday = datetime.strptime(sunday_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD")
    
    # Tính ngày cuối tuần (thứ 7)
    saturday = sunday + timedelta(days=6)
    
    # Query lấy lịch trong tuần qua enrollment
    query = db.query(Schedule).join(
        CourseClass, Schedule.course_class_id == CourseClass.course_class_id
    ).join(
        Enrollment, CourseClass.course_class_id == Enrollment.course_class_id
    ).join(
        Course, CourseClass.course_id == Course.course_id
    ).join(
        Room, Schedule.room_id == Room.room_id
    ).join(
        Period, Schedule.period_start == Period.period_id
    ).outerjoin(
        Semester, Schedule.semester_id == Semester.semester_id
    ).filter(
        Enrollment.student_id == student_id,
        Schedule.specific_date >= sunday,
        Schedule.specific_date <= saturday
    )
    
    # Order by day, period để dễ xem
    schedules = query.order_by(
        Schedule.specific_date,
        Schedule.day_of_week,
        Schedule.period_start
    ).all()
    
    # Nếu lịch trống thì trả về rỗng
    if not schedules:
        return {
            "student": {
                "student_id": student.student_id,
                "student_code": student.student_code,
                "full_name": f"{student.last_name} {student.first_name}",
                "email": student.email,
                "class_name": student.class_name,
                "major": student.major
            },
            "week_info": {
                "sunday_date": sunday.strftime("%d/%m/%Y"),
                "saturday_date": saturday.strftime("%d/%m/%Y"),
                "week_range": f"{sunday.strftime('%d/%m/%Y')} - {saturday.strftime('%d/%m/%Y')}"
            },
            "total_schedules": 0,
            "schedules": []
        }
    
    # Format dữ liệu trả về
    result = []
    for schedule in schedules:
        # Lấy thông tin period end
        period_end = db.query(Period).filter(Period.period_id == schedule.period_end).first()
        
        # Map day_of_week to Vietnamese
        day_names = {
            1: "Chủ nhật",
            2: "Thứ 2", 
            3: "Thứ 3",
            4: "Thứ 4",
            5: "Thứ 5",
            6: "Thứ 6",
            7: "Thứ 7"
        }
        
        schedule_info = {
            "schedule_id": schedule.schedule_id,
            "day_of_week": schedule.day_of_week,
            "day_name": day_names.get(schedule.day_of_week, "Unknown"),
            "specific_date": schedule.specific_date.strftime("%d/%m/%Y") if schedule.specific_date else None,
            "course": {
                "course_id": schedule.course_class.course.course_id,
                "course_code": schedule.course_class.course.course_code,
                "course_name": schedule.course_class.course.name,
                "credits": schedule.course_class.course.credits
            },
            "course_class": {
                "course_class_id": schedule.course_class.course_class_id,
                "section": schedule.course_class.section,
                "min_students": schedule.course_class.min_students,
                "max_students": schedule.course_class.max_students,
                "teacher": {
                    "teacher_id": schedule.course_class.teacher.teacher_id if schedule.course_class.teacher else None,
                    "teacher_code": schedule.course_class.teacher.teacher_code if schedule.course_class.teacher else None,
                    "full_name": f"{schedule.course_class.teacher.last_name} {schedule.course_class.teacher.first_name}" if schedule.course_class.teacher else None
                }
            },
            "room": {
                "room_id": schedule.room.room_id,
                "room_name": schedule.room.room_name,
                "capacity": schedule.room.capacity
            },
            "time": {
                "period_start": {
                    "period_id": schedule.period_start,
                    "start_time": db.query(Period).filter(Period.period_id == schedule.period_start).first().start_time.strftime("%H:%M") if db.query(Period).filter(Period.period_id == schedule.period_start).first().start_time else None,
                    "end_time": db.query(Period).filter(Period.period_id == schedule.period_start).first().end_time.strftime("%H:%M") if db.query(Period).filter(Period.period_id == schedule.period_start).first().end_time else None
                },
                "period_end": {
                    "period_id": schedule.period_end,
                    "start_time": period_end.start_time.strftime("%H:%M") if period_end and period_end.start_time else None,
                    "end_time": period_end.end_time.strftime("%H:%M") if period_end and period_end.end_time else None
                }
            },
            "semester": {
                "semester_id": schedule.semester.semester_id if schedule.semester else None,
                "semester_name": schedule.semester.semester_name if schedule.semester else None
            } if schedule.semester else None
        }
        result.append(schedule_info)
    
    return {
        "student": {
            "student_id": student.student_id,
            "student_code": student.student_code,
            "full_name": f"{student.last_name} {student.first_name}",
            "email": student.email,
            "class_name": student.class_name,
            "major": student.major
        },
        "week_info": {
            "sunday_date": sunday.strftime("%d/%m/%Y"),
            "saturday_date": saturday.strftime("%d/%m/%Y"),
            "week_range": f"{sunday.strftime('%d/%m/%Y')} - {saturday.strftime('%d/%m/%Y')}"
        },
        "total_schedules": len(result),
        "schedules": result
    }
