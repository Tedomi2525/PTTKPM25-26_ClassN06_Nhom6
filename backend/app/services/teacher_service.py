from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from typing import Optional

from app import models
from app.models.teacher import Teacher as TeacherModel
from app.models.user import User as UserModel
from app.models.schedule import Schedule
from app.models.course_class import CourseClass
from app.models.course import Course
from app.models.room import Room
from app.models.period import Period
from app.models.semester import Semester
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.schemas.user import UserCreate

from app.core.security import get_password_hash

def get_teacher_by_id(db, teacher_id: int):
    teacher = db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()
    return teacher

def generate_teacher_code(db: Session) -> str:
    year = datetime.now().year % 100  # 2 số cuối của năm
    prefix = f"GV{year}"

    # Lấy teacher_code lớn nhất từ cả bảng teachers và users (username)
    # Vì teacher_code sẽ được dùng làm username trong bảng users
    max_from_teachers = (
        db.query(TeacherModel)
        .filter(TeacherModel.teacher_code.like(f"{prefix}%"))
        .order_by(TeacherModel.teacher_code.desc())
        .first()
    )

    max_from_users = (
        db.query(UserModel)
        .filter(UserModel.username.like(f"{prefix}%"))
        .order_by(UserModel.username.desc())
        .first()
    )

    # Tìm số lớn nhất từ cả hai bảng
    max_number = 0
    
    if max_from_teachers and max_from_teachers.teacher_code:
        try:
            teacher_number = int(max_from_teachers.teacher_code[-6:])  # 6 số cuối
            max_number = max(max_number, teacher_number)
        except ValueError:
            pass
    
    if max_from_users and max_from_users.username:
        try:
            user_number = int(max_from_users.username[-6:])  # 6 số cuối
            max_number = max(max_number, user_number)
        except ValueError:
            pass

    new_number = max_number + 1
    return f"{prefix}{new_number:06d}"

def get_teachers(db: Session):
    return db.query(TeacherModel).filter(TeacherModel.status == "active").all()


def search_teachers(db: Session, q: str):
    return db.query(TeacherModel).filter(
        or_(
            func.lower(TeacherModel.first_name).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.last_name).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.email).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.teacher_code).like(func.lower(f"%{q}%"))
        ) 
    ).all()


def create_teacher(db: Session, teacher_payload: TeacherCreate):
    try:
        # 1. Sinh teacher_code
        teacher_code = generate_teacher_code(db)

        # 2. Kiểm tra email đã tồn tại chưa (chỉ khi có email)
        if teacher_payload.email and teacher_payload.email.strip():
            existing_teacher = db.query(TeacherModel).filter(TeacherModel.email == teacher_payload.email).first()
            if existing_teacher:
                raise ValueError(f"Email {teacher_payload.email} đã được sử dụng bởi giáo viên khác")

        # 3. Tạo user trước
        user_payload = UserCreate(
            username=teacher_code,
            email=f"{teacher_code}@edunera.edu",
            password=get_password_hash(f"{teacher_code}@"),
            role="teacher"
        )

        # model_dump(by_alias=False) để lấy đúng field trong model (Pydantic v2)
        new_user = UserModel(**user_payload.model_dump(by_alias=False))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 4. Tạo teacher, gán user_id
        teacher_data = teacher_payload.model_dump(by_alias=False)
        teacher_data["teacher_code"] = teacher_code
        teacher_data["user_id"] = new_user.user_id
        # Sử dụng email từ input nếu có, nếu không thì dùng email mặc định
        teacher_data["email"] = teacher_payload.email or user_payload.email
        


        new_teacher = TeacherModel(**teacher_data)
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)

        return new_teacher
    except IntegrityError as e:
        db.rollback()
        error_str = str(e).lower()
        if "unique constraint" in error_str:
            if "users_username_key" in error_str:
                raise ValueError("Mã giáo viên (username) đã tồn tại, vui lòng thử lại")
            elif "teachers_teacher_code_key" in error_str:
                raise ValueError("Mã giáo viên đã tồn tại, vui lòng thử lại")
            elif "teachers_email_key" in error_str or "users_email_key" in error_str:
                raise ValueError("Email đã được sử dụng")
            else:
                raise ValueError(f"Vi phạm ràng buộc duy nhất: {str(e)}")
        raise ValueError(f"Lỗi dữ liệu: {str(e)}")
    except Exception as e:
        db.rollback()
        raise e


def update_teacher(db: Session, teacher_id: int, payload: TeacherUpdate):
    teacher = db.query(TeacherModel).filter(TeacherModel.teacher_id == teacher_id).first()
    if not teacher:
        return None

    for key, value in payload.model_dump(exclude_unset=True, by_alias=False).items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher_id: int):
    teacher = db.query(TeacherModel).filter(TeacherModel.teacher_id == teacher_id).first()
    if not teacher:
        return None
    try:
        teacher.status = "inactive"
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False

def get_teacher_weekly_schedule(db: Session, teacher_id: int, sunday_date: str):
    """
    Lấy lịch giảng dạy của giáo viên trong tuần cụ thể
    Args:
        teacher_id: ID của giáo viên
        sunday_date: Ngày chủ nhật của tuần (format: DD/MM/YYYY hoặc YYYY-MM-DD)
    """
    # Kiểm tra giáo viên có tồn tại không
    teacher = db.query(TeacherModel).filter(TeacherModel.teacher_id == teacher_id).first()
    if not teacher:
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
    
    # Query lấy lịch trong tuần
    query = db.query(Schedule).join(
        CourseClass, Schedule.course_class_id == CourseClass.course_class_id
    ).join(
        Course, CourseClass.course_id == Course.course_id
    ).join(
        Room, Schedule.room_id == Room.room_id
    ).join(
        Period, Schedule.period_start == Period.period_id
    ).outerjoin(
        Semester, Schedule.semester_id == Semester.semester_id
    ).filter(
        CourseClass.teacher_id == teacher_id,
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
            "teacher": {
                "teacher_id": teacher.teacher_id,
                "teacher_code": teacher.teacher_code,
                "full_name": f"{teacher.last_name} {teacher.first_name}",
                "email": teacher.email,
                "department": teacher.department
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
            1: "Thứ 2",
            2: "Thứ 3",
            3: "Thứ 4",
            4: "Thứ 5",
            5: "Thứ 6",
            6: "Thứ 7",
            7: "Chủ nhật"
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
                "max_students": schedule.course_class.max_students
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
        "teacher": {
            "teacher_id": teacher.teacher_id,
            "teacher_code": teacher.teacher_code,
            "full_name": f"{teacher.last_name} {teacher.first_name}",
            "email": teacher.email,
            "department": teacher.department
        },
        "week_info": {
            "sunday_date": sunday.strftime("%d/%m/%Y"),
            "saturday_date": saturday.strftime("%d/%m/%Y"),
            "week_range": f"{sunday.strftime('%d/%m/%Y')} - {saturday.strftime('%d/%m/%Y')}"
        },
        "total_schedules": len(result),
        "schedules": result
    }