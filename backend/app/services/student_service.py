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

# ==============================================================================
# UTILITY FUNCTIONS
# (Logic generate_student_code giữ nguyên)
# ==============================================================================

def generate_student_code(db: Session) -> str:
    year = datetime.now().year % 100 
    prefix = f"SV{year}"
    max_from_students = (
        db.query(StudentModel)
        .filter(StudentModel.student_code.like(f"{prefix}%"))
        .order_by(StudentModel.student_code.desc())
        .first()
    )
    max_from_users = (
        db.query(UserModel)
        .filter(UserModel.username.like(f"{prefix}%"))
        .order_by(UserModel.username.desc())
        .first()
    )
    max_number = 0
    if max_from_students and max_from_students.student_code:
        try:
            student_number = int(max_from_students.student_code[-6:])
            max_number = max(max_number, student_number)
        except ValueError:
            pass
    if max_from_users and max_from_users.username:
        try:
            user_number = int(max_from_users.username[-6:])
            max_number = max(max_number, user_number)
        except ValueError:
            pass
    new_number = max_number + 1
    return f"{prefix}{new_number:06d}"

# ==============================================================================
# CRUD OPERATIONS
# ==============================================================================

def get_student(db: Session, student_id: int) -> Optional[StudentModel]:
    return db.query(StudentModel).filter(StudentModel.student_id == student_id).first()

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

        # 2. Kiểm tra email
        if student_payload.email and student_payload.email.strip():
            existing_student = db.query(StudentModel).filter(StudentModel.email == student_payload.email).first()
            if existing_student:
                raise ValueError(f"Email {student_payload.email} đã được sử dụng bởi sinh viên khác")

        # 3. Tạo user cho sinh viên
        user_payload = UserCreate(
            username=student_code,
            email=student_payload.email or f"{student_code}@edunera.edu",
            password=get_password_hash(f"{student_code}@"),
            role="student"
        )

        user_data = user_payload.model_dump(by_alias=False)
        new_user = UserModel(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 4. Tạo student, gán user_id và AVATAR URL
        student_data = student_payload.model_dump(by_alias=False, exclude_unset=True)
        student_data["student_code"] = student_code
        student_data["user_id"] = new_user.user_id
        student_data["email"] = student_payload.email or user_payload.email
        
        # Xử lý trường avatar: đã được chuẩn hóa là URL string từ endpoint
        if not student_data.get("avatar"):
            student_data.pop("avatar", None)
        
        # Xử lý field class_name
        if "class_name" in student_data and student_data["class_name"] is None:
            student_data.pop("class_name")

        new_student = StudentModel(**student_data)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student
    
    except IntegrityError as e:
        db.rollback()
        error_str = str(e).lower()
        if "unique constraint" in error_str:
            if "users_username_key" in error_str:
                raise ValueError("Mã sinh viên (username) đã tồn tại, vui lòng thử lại")
            elif "students_student_code_key" in error_str:
                raise ValueError("Mã sinh viên đã tồn tại, vui lòng thử lại")
            elif "students_email_key" in error_str or "users_email_key" in error_str:
                raise ValueError("Email đã được sử dụng")
            else:
                raise ValueError(f"Vi phạm ràng buộc duy nhất: {str(e)}")
        elif "check constraint" in error_str:
            if "gender_check" in error_str:
                raise ValueError("Giá trị giới tính không hợp lệ. Chỉ chấp nhận 'Nam', 'Nữ' hoặc 'Khác'")
        raise ValueError(f"Lỗi dữ liệu: {str(e)}")
    except Exception as e:
        db.rollback()
        print(f"Lỗi tạo sinh viên không mong đợi: {str(e)}")
        raise e
    
def update_student(db: Session, student_id: int, payload: StudentUpdate):
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None

    update_data = payload.model_dump(exclude_unset=True, by_alias=False)
    
    for key, value in update_data.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as e:
        db.rollback()
        error_str = str(e).lower()
        if "unique constraint" in error_str:
            if "email" in error_str:
                raise ValueError("Email đã được sử dụng")
        elif "check constraint" in error_str:
            if "gender_check" in error_str:
                raise ValueError("Giá trị giới tính không hợp lệ. Chỉ chấp nhận 'Nam', 'Nữ' hoặc 'Khác'")
        raise ValueError(f"Lỗi cập nhật dữ liệu: {str(e)}")
    except Exception as e:
        db.rollback()
        raise e
    
def delete_student(db: Session, student_id: int) -> bool:
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.") 
    
    try:
        user = db.query(UserModel).filter(UserModel.user_id == student.user_id).first()
        db.delete(student)
        if user:
            db.delete(user)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Cannot delete student {student_id} because of related records (e.g., Enrollment).") 
    except Exception as e:
        db.rollback()
        raise Exception(f"Unexpected error during deletion of student {student_id}: {str(e)}")

def get_student_weekly_schedule(db: Session, student_id: int, sunday_date: str):
    # Logic lịch học (giữ nguyên)
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None
    
    try:
        if '/' in sunday_date:
            sunday = datetime.strptime(sunday_date, "%d/%m/%Y").date()
        else:
            sunday = datetime.strptime(sunday_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD")
    
    saturday = sunday + timedelta(days=6)
    
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
    
    schedules = query.order_by(
        Schedule.specific_date,
        Schedule.day_of_week,
        Schedule.period_start
    ).all()
    
    # ... (Phần formatting dữ liệu trả về giữ nguyên)
    
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
    
    result = []
    for schedule in schedules:
        period_end = db.query(Period).filter(Period.period_id == schedule.period_end).first()
        day_names = {
            1: "Chủ nhật", 2: "Thứ 2", 3: "Thứ 3", 4: "Thứ 4", 5: "Thứ 5", 6: "Thứ 6", 7: "Thứ 7"
        }
        
        def get_period_time(period_id, attr):
            period = db.query(Period).filter(Period.period_id == period_id).first()
            if period and getattr(period, attr):
                return getattr(period, attr).strftime("%H:%M")
            return None
        
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
                    "start_time": get_period_time(schedule.period_start, 'start_time'),
                    "end_time": get_period_time(schedule.period_start, 'end_time')
                },
                "period_end": {
                    "period_id": schedule.period_end,
                    "start_time": get_period_time(schedule.period_end, 'start_time'),
                    "end_time": get_period_time(schedule.period_end, 'end_time')
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