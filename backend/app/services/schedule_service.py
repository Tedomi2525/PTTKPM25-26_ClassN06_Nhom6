from app.models.room import Room
from app.models.period import Period
from app.models.course_class import CourseClass
from app.models.program_course import ProgramCourse
from app.models.program import Program
from app.models.semester import Semester
from app.models.course import Course
from app.models.schedule import Schedule
from app.models.schedule_template import ScheduleTemplate
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
import random

def get_schedule(db: Session, program_id: int):
    """Lấy lịch học hiện tại từ cơ sở dữ liệu cho một chương trình cụ thể"""
    schedules = db.query(Schedule).join(
        CourseClass, Schedule.course_class_id == CourseClass.course_class_id
    ).join(
        Course, CourseClass.course_id == Course.course_id
    ).join(
        ProgramCourse, Course.course_id == ProgramCourse.course_id
    ).filter(
        ProgramCourse.program_id == program_id
    ).all()
    
    result = []
    for sched in schedules:
        result.append({
            "schedule_id": sched.schedule_id,
            "course_class_id": sched.course_class_id,
            "room_id": sched.room_id,
            "day_of_week": sched.day_of_week,
            "period_start": sched.period_start,
            "period_end": sched.period_end,
            "created_at": sched.created_at,
            "updated_at": sched.updated_at
        })
    
    return result


def get_schedule_by_semester(db: Session, program_id: int, semester_code: str):
    """Lấy lịch học của một học kỳ cụ thể cho một chương trình"""
    schedules = db.query(Schedule).join(
        CourseClass, Schedule.course_class_id == CourseClass.course_class_id
    ).join(
        Course, CourseClass.course_id == Course.course_id
    ).join(
        ProgramCourse, Course.course_id == ProgramCourse.course_id
    ).filter(
        ProgramCourse.program_id == program_id,
        ProgramCourse.semester_no == semester_code
    ).all()
    
    result = []
    for sched in schedules:
        result.append({
            "schedule_id": sched.schedule_id,
            "course_class_id": sched.course_class_id,
            "room_id": sched.room_id,
            "day_of_week": sched.day_of_week,
            "period_start": sched.period_start,
            "period_end": sched.period_end,
            "created_at": sched.created_at,
            "updated_at": sched.updated_at,
            "semester_code": semester_code
        })
    
    return result


def get_current_semester_for_program(db: Session, program_id: int):
    """Lấy mã học kỳ hiện tại cho chương trình (không tự động cập nhật)"""
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return None
    
    # Trả về semester hiện tại mà không tự động cập nhật
    if not program.current_semester:
        return "HK_1_1"  # Default nếu chưa set
    
    return program.current_semester


def get_courses_for_current_semester(db: Session, program_id: int):
    """Lấy tất cả môn học của học kỳ hiện tại cho chương trình"""
    current_semester_code = get_current_semester_for_program(db, program_id)
    if not current_semester_code:
        return []
    
    program_courses = db.query(ProgramCourse).join(Course).filter(
        ProgramCourse.program_id == program_id,
        ProgramCourse.semester_no == current_semester_code
    ).all()

    return [pc.course for pc in program_courses]


def generate_schedule_template(db: Session, program_id: int):
    """Tạo mẫu thời khóa biểu cho 1 tuần và lưu vào schedule_templates"""
    rooms = db.query(Room).all()
    periods = db.query(Period).all()
    
    # Lọc lớp học theo chương trình và học kỳ hiện tại
    if program_id:
        current_semester_courses = get_courses_for_current_semester(db, program_id)
        if not current_semester_courses:
            return "empty"
        
        course_ids = [course.course_id for course in current_semester_courses]
        courseClasses = db.query(CourseClass).join(Course).filter(
            Course.course_id.in_(course_ids)
        ).all() if course_ids else []

    room_capacity = {r.room_id: r.capacity for r in rooms}
    day_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
    
    # Tạo mapping period_id -> (day, period_number)
    period_info = {}
    for p in periods:
        period_info[p.period_id] = (p.day, p.period_number)

    teacherSlot = {}  # teacher_id -> set(period_id)
    roomSlot = {}     # room_id -> set(period_id)
    template_schedule = []

    for cc in courseClasses:
        teacher_id = cc.teacher_id
        if teacher_id not in teacherSlot:
            teacherSlot[teacher_id] = set()

        # Xác định số ca cần thiết
        sessions_needed = 2 if cc.course and cc.course.credits >= 3 else 1

        # Kiểm tra số phòng khả dụng
        available_rooms = [room for room in rooms if cc.max_students <= room_capacity[room.room_id]]
        if len(available_rooms) < sessions_needed:
            if len(available_rooms) > 0:
                sessions_needed = min(sessions_needed, len(available_rooms))
            else:
                continue

        # Xếp lịch từng ca cho lớp học
        for session_count in range(sessions_needed):
            scoreTable = {}
            
            # Duyệt qua tất cả phòng và ca để tính điểm
            for room in rooms:
                if room.room_id not in roomSlot:
                    roomSlot[room.room_id] = set()
                    
                for period in periods:
                    key = f"{room.room_id}_{period.period_id}"
                    score = 0
                    
                    # ==========================================================
                    # SCORING RULES - Điểm cao hơn = Ưu tiên hơn
                    # ==========================================================
                    
                    # Rule 1: Phòng đủ sức chứa (HARD CONSTRAINT)
                    if cc.max_students <= room_capacity[room.room_id]:
                        score += 5
                    else:
                        score -= 1000  # Loại bỏ hoàn toàn
                    
                    # Rule 2: Giáo viên rảnh (HARD CONSTRAINT)
                    if period.period_id not in teacherSlot[teacher_id]:
                        score += 10
                    else:
                        score -= 1000  # Loại bỏ hoàn toàn
                    
                    # Rule 3: Phòng trống cơ bản (HARD CONSTRAINT)
                    if period.period_id in roomSlot[room.room_id]:
                        score -= 1000  # Phòng đã bị chiếm
                    
                    # Rule 5: Ràng buộc môn nhiều ca (SOFT CONSTRAINT)
                    existing_periods = [s['period_id'] for s in template_schedule if s['course_class_id'] == cc.course_class_id]
                    if period.period_id in existing_periods:
                        score -= 1000  # Không được trùng ca cho cùng 1 lớp
                    elif len(existing_periods) > 0 and cc.course and cc.course.credits >= 3:
                        # Môn >= 3 tín chỉ: tránh xếp quá gần nhau
                        current_day = day_order[period.day]
                        for ep in existing_periods:
                            if ep in period_info:
                                existing_day = day_order[period_info[ep][0]]
                                day_diff = abs(current_day - existing_day)
                                if day_diff < 2:
                                    score -= 500  # Penalty nếu quá gần
                    
                    # Rule 6: Ưu tiên phòng khác nhau cho cùng một lớp (SOFT CONSTRAINT)
                    existing_rooms = [s['room_id'] for s in template_schedule if s['course_class_id'] == cc.course_class_id]
                    if room.room_id in existing_rooms:
                        score -= 500  # Penalty nếu dùng lại phòng cũ
                    else:
                        score += 50   # Bonus cho phòng mới
                        unique_rooms_used = len(set(existing_rooms))
                        if unique_rooms_used < sessions_needed:
                            score += 100  # Khuyến khích đa dạng phòng
                    
                    # Rule 7: Xung đột lớp cùng môn và policy dùng chung phòng (BUSINESS RULE)
                    for existing_item in template_schedule:
                        if existing_item['period_id'] == period.period_id:
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if existing_class and existing_class.course_id == cc.course_id:
                                # Cùng môn học
                                if existing_class.teacher_id == cc.teacher_id:
                                    # Cùng giáo viên -> Tuyệt đối không được trùng slot
                                    score -= 1000
                                else:
                                    # Khác giáo viên -> Cho phép dùng chung phòng nhưng khuyến khích tách biệt
                                    if existing_item['room_id'] == room.room_id:
                                        # Cho phép dùng chung phòng nhưng không khuyến khích
                                        score -= 200  # Penalty nhẹ thay vì cấm hoàn toàn
                                    else:
                                        # Khuyến khích dùng phòng khác
                                        score += 50
                    
                    # Rule 8: Giới hạn 3 ca/ngày (SOFT CONSTRAINT)
                    current_day = period.day
                    sessions_in_day = []
                    for s in template_schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            s_day = period_info.get(s['period_id'], ('', 0))[0]
                            if s_day == current_day:
                                sessions_in_day.append(s)
                    
                    if len(sessions_in_day) >= 3:
                        score -= 10000  # Cấm hoàn toàn
                    elif len(sessions_in_day) == 2:
                        score -= 500    # Penalty mạnh
                    
                    # Rule 9: Ưu tiên ngày nghỉ (OPTIMIZATION)
                    days_with_classes = set()
                    for s in template_schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            day = period_info.get(s['period_id'], ('', 0))[0]
                            if day:
                                days_with_classes.add(day)
                    
                    potential_days_count = len(days_with_classes | {current_day})
                    
                    if potential_days_count <= 4:
                        score += 100      # Khuyến khích tập trung 4 ngày/tuần
                    elif potential_days_count == 5:
                        score += 50       # Chấp nhận được 5 ngày/tuần
                    else:
                        score -= 50       # Penalty nhẹ cho 6+ ngày/tuần
                        
                    scoreTable[key] = score

            # Chọn slot với yếu tố ngẫu nhiên
            if scoreTable:
                valid_slots = [(k, v) for k, v in scoreTable.items() if v > -1000]
                
                if valid_slots:
                    valid_slots.sort(key=lambda x: x[1], reverse=True)
                    top_count = max(1, len(valid_slots) // 5)  # Top 20%
                    top_slots = valid_slots[:top_count]
                    
                    # Ưu tiên phòng mới
                    existing_rooms = [s['room_id'] for s in template_schedule if s['course_class_id'] == cc.course_class_id]
                    preferred_slots = []
                    for slot_key, score in top_slots:
                        r_id, p_id = map(int, slot_key.split("_"))
                        if len(existing_rooms) == 0 or r_id not in existing_rooms:
                            preferred_slots.append((slot_key, score))
                    
                    if preferred_slots:
                        best_slot_key, best_score = random.choice(preferred_slots)
                    else:
                        best_slot_key, best_score = random.choice(top_slots)
                    
                    room_id, period_id = map(int, best_slot_key.split("_"))
                    
                    # Cập nhật slots đã dùng
                    teacherSlot[teacher_id].add(period_id)
                    roomSlot[room_id].add(period_id)

                    template_schedule.append({
                        "course_class_id": cc.course_class_id,
                        "room_id": room_id,
                        "period_id": period_id
                    })
                else:
                    continue
    
    # Lưu template vào database
    try:
        # Xóa template cũ của học kỳ hiện tại
        current_semester_code = get_current_semester_for_program(db, program_id)
        if current_semester_code and current_semester_code != "empty":
            current_course_ids = [course.course_id for course in current_semester_courses]
            current_class_ids = [cc.course_class_id for cc in courseClasses]
            
            existing_templates = db.query(ScheduleTemplate).filter(
                ScheduleTemplate.course_class_id.in_(current_class_ids)
            ).all()
            for template_item in existing_templates:
                db.delete(template_item)
        
        # Lưu template mới
        for item in template_schedule:
            new_template = ScheduleTemplate(
                course_class_id=item['course_class_id'],
                room_id=item['room_id'],
                period_id=item['period_id']
            )
            db.add(new_template)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to save schedule template: {str(e)}"}
    
    return {
        "template": [{"index": i+1, **item} for i, item in enumerate(template_schedule)]
    }


def generate_semester_schedule(db: Session, program_id: int, semester_id: int, total_weeks: int = 10, force_recreate_template: bool = False):
    """Tạo lịch học cho cả học kỳ (10 tuần) từ template"""
    
    # Lấy thông tin học kỳ
    semester = db.query(Semester).filter(Semester.semester_id == semester_id).first()
    if not semester:
        return {"error": "Semester not found"}
    
    # Lấy template schedule
    current_semester_courses = get_courses_for_current_semester(db, program_id)
    if not current_semester_courses:
        return {"error": "No courses found for current semester"}
    
    course_ids = [course.course_id for course in current_semester_courses]
    courseClasses = db.query(CourseClass).join(Course).filter(
        Course.course_id.in_(course_ids)
    ).all() if course_ids else []
    
    current_class_ids = [cc.course_class_id for cc in courseClasses]
    templates = db.query(ScheduleTemplate).filter(
        ScheduleTemplate.course_class_id.in_(current_class_ids)
    ).all()
    
    # Nếu không có template hoặc force recreate, tạo template mới
    if not templates or force_recreate_template:
        print("No templates found or force recreate requested. Creating new template...")
        template_result = generate_schedule_template(db, program_id)
        
        if isinstance(template_result, str) and template_result == "empty":
            return {"error": "No courses found for current semester"}
        
        if "error" in template_result:
            return template_result
        
        # Lấy lại templates sau khi tạo mới
        templates = db.query(ScheduleTemplate).filter(
            ScheduleTemplate.course_class_id.in_(current_class_ids)
        ).all()
        
        if not templates:
            return {"error": "Failed to create schedule template"}
    
    try:
        # Xóa schedule cũ của học kỳ này
        existing_schedules = db.query(Schedule).filter(
            Schedule.semester_id == semester_id
        ).all()
        for schedule_item in existing_schedules:
            db.delete(schedule_item)
        
        # Tạo mapping period_id -> day_of_week
        periods = db.query(Period).all()
        period_mapping = {}
        for period in periods:
            day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
            period_mapping[period.period_id] = {
                'day_of_week': day_map.get(period.day, 1),
                'period_number': period.period_number
            }
        
        # Tính ngày bắt đầu học kỳ (thứ 2 đầu tiên)
        semester_start = semester.start_time.date()
        # Tìm thứ 2 đầu tiên
        days_ahead = 0 - semester_start.weekday()  # 0 = Monday
        if days_ahead < 0:
            days_ahead += 7
        first_monday = semester_start + timedelta(days=days_ahead)
        
        # Generate lịch cho từng tuần
        schedules_created = []
        for week in range(1, total_weeks + 1):
            week_start_date = first_monday + timedelta(weeks=week-1)
            
            for template in templates:
                period_info = period_mapping.get(template.period_id)
                if period_info:
                    # Tính ngày cụ thể
                    day_offset = period_info['day_of_week'] - 1  # Monday = 0
                    specific_date = week_start_date + timedelta(days=day_offset)
                    
                    new_schedule = Schedule(
                        course_class_id=template.course_class_id,
                        room_id=template.room_id,
                        day_of_week=period_info['day_of_week'],
                        period_start=template.period_id,
                        period_end=template.period_id,
                        week_number=week,
                        specific_date=specific_date,
                        semester_id=semester_id
                    )
                    db.add(new_schedule)
                    schedules_created.append({
                        "week": week,
                        "course_class_id": template.course_class_id,
                        "room_id": template.room_id,
                        "day_of_week": period_info['day_of_week'],
                        "period_id": template.period_id,
                        "specific_date": specific_date.isoformat()
                    })
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to generate semester schedule: {str(e)}"}
    
    return {
        "message": f"Successfully generated schedule for {total_weeks} weeks",
        "total_schedules": len(schedules_created),
        "schedules": schedules_created[:50]  # Chỉ trả về 50 schedule đầu để tránh quá tải
    }
def generate_schedule_legacy(db, program_id: int):
    """[LEGACY] Tạo thời khóa biểu tự động với các ràng buộc và quy tắc tối ưu cho 1 tuần"""
    rooms = db.query(Room).all()
    periods = db.query(Period).all()
    
    # Lọc lớp học theo chương trình và học kỳ hiện tại
    if program_id:
        current_semester_courses = get_courses_for_current_semester(db, program_id)
        if not current_semester_courses:
            return "empty"
        
        course_ids = [course.course_id for course in current_semester_courses]
        courseClasses = db.query(CourseClass).join(Course).filter(
            Course.course_id.in_(course_ids)
        ).all() if course_ids else []

    room_capacity = {r.room_id: r.capacity for r in rooms}
    day_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
    
    # Tạo mapping period_id -> (day, period_number)
    period_info = {}
    for p in periods:
        period_info[p.period_id] = (p.day, p.period_number)

    teacherSlot = {}  # teacher_id -> set(period_id)
    roomSlot = {}     # room_id -> set(period_id)
    schedule = []

    for cc in courseClasses:
        teacher_id = cc.teacher_id
        if teacher_id not in teacherSlot:
            teacherSlot[teacher_id] = set()

        # Xác định số ca cần thiết
        sessions_needed = 2 if cc.course and cc.course.credits >= 3 else 1

        # Kiểm tra số phòng khả dụng
        available_rooms = [room for room in rooms if cc.max_students <= room_capacity[room.room_id]]
        if len(available_rooms) < sessions_needed:
            if len(available_rooms) > 0:
                sessions_needed = min(sessions_needed, len(available_rooms))
            else:
                continue

        # Xếp lịch từng ca cho lớp học
        for session_count in range(sessions_needed):
            scoreTable = {}
            
            # Duyệt qua tất cả phòng và ca để tính điểm
            for room in rooms:
                if room.room_id not in roomSlot:
                    roomSlot[room.room_id] = set()
                    
                for period in periods:
                    key = f"{room.room_id}_{period.period_id}"
                    score = 0
                    
                    # ==========================================================
                    # SCORING RULES - Điểm cao hơn = Ưu tiên hơn
                    # ==========================================================
                    
                    # Rule 1: Phòng đủ sức chứa (HARD CONSTRAINT)
                    if cc.max_students <= room_capacity[room.room_id]:
                        score += 5
                    else:
                        score -= 1000  # Loại bỏ hoàn toàn
                    
                    # Rule 2: Giáo viên rảnh (HARD CONSTRAINT)
                    if period.period_id not in teacherSlot[teacher_id]:
                        score += 10
                    else:
                        score -= 1000  # Loại bỏ hoàn toàn
                    
                    # Rule 3: Phòng trống cơ bản (HARD CONSTRAINT)
                    if period.period_id in roomSlot[room.room_id]:
                        score -= 1000  # Phòng đã bị chiếm
                    
                    # Rule 5: Ràng buộc môn nhiều ca (SOFT CONSTRAINT)
                    existing_periods = [s['period_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if period.period_id in existing_periods:
                        score -= 1000  # Không được trùng ca cho cùng 1 lớp
                    elif len(existing_periods) > 0 and cc.course and cc.course.credits >= 3:
                        # Môn >= 3 tín chỉ: tránh xếp quá gần nhau
                        current_day = day_order[period.day]
                        for ep in existing_periods:
                            if ep in period_info:
                                existing_day = day_order[period_info[ep][0]]
                                day_diff = abs(current_day - existing_day)
                                if day_diff < 2:
                                    score -= 500  # Penalty nếu quá gần
                    
                    # Rule 6: Ưu tiên phòng khác nhau cho cùng một lớp (SOFT CONSTRAINT)
                    existing_rooms = [s['room_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if room.room_id in existing_rooms:
                        score -= 500  # Penalty nếu dùng lại phòng cũ
                    else:
                        score += 50   # Bonus cho phòng mới
                        unique_rooms_used = len(set(existing_rooms))
                        if unique_rooms_used < sessions_needed:
                            score += 100  # Khuyến khích đa dạng phòng
                    
                    # Rule 7: Xung đột lớp cùng môn và policy dùng chung phòng (BUSINESS RULE)
                    for existing_item in schedule:
                        if existing_item['period_id'] == period.period_id:
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if existing_class and existing_class.course_id == cc.course_id:
                                # Cùng môn học
                                if existing_class.teacher_id == cc.teacher_id:
                                    # Cùng giáo viên -> Tuyệt đối không được trùng slot
                                    score -= 1000
                                else:
                                    # Khác giáo viên -> Cho phép dùng chung phòng nhưng khuyến khích tách biệt
                                    if existing_item['room_id'] == room.room_id:
                                        # Cho phép dùng chung phòng nhưng không khuyến khích
                                        score -= 200  # Penalty nhẹ thay vì cấm hoàn toàn
                                    else:
                                        # Khuyến khích dùng phòng khác
                                        score += 50
                    
                    # Rule 8: Giới hạn 3 ca/ngày (SOFT CONSTRAINT)
                    current_day = period.day
                    sessions_in_day = []
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            s_day = period_info.get(s['period_id'], ('', 0))[0]
                            if s_day == current_day:
                                sessions_in_day.append(s)
                    
                    if len(sessions_in_day) >= 3:
                        score -= 10000  # Cấm hoàn toàn
                    elif len(sessions_in_day) == 2:
                        score -= 500    # Penalty mạnh
                    
                    # Rule 9: Ưu tiên ngày nghỉ (OPTIMIZATION)
                    days_with_classes = set()
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            day = period_info.get(s['period_id'], ('', 0))[0]
                            if day:
                                days_with_classes.add(day)
                    
                    potential_days_count = len(days_with_classes | {current_day})
                    
                    if potential_days_count <= 4:
                        score += 100      # Khuyến khích tập trung 4 ngày/tuần
                    elif potential_days_count == 5:
                        score += 50       # Chấp nhận được 5 ngày/tuần
                    else:
                        score -= 50       # Penalty nhẹ cho 6+ ngày/tuần
                        
                    scoreTable[key] = score

            # Chọn slot với yếu tố ngẫu nhiên
            if scoreTable:
                valid_slots = [(k, v) for k, v in scoreTable.items() if v > -1000]
                
                if valid_slots:
                    valid_slots.sort(key=lambda x: x[1], reverse=True)
                    top_count = max(1, len(valid_slots) // 5)  # Top 20%
                    top_slots = valid_slots[:top_count]
                    
                    # Ưu tiên phòng mới
                    existing_rooms = [s['room_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    preferred_slots = []
                    for slot_key, score in top_slots:
                        r_id, p_id = map(int, slot_key.split("_"))
                        if len(existing_rooms) == 0 or r_id not in existing_rooms:
                            preferred_slots.append((slot_key, score))
                    
                    if preferred_slots:
                        best_slot_key, best_score = random.choice(preferred_slots)
                    else:
                        best_slot_key, best_score = random.choice(top_slots)
                    
                    room_id, period_id = map(int, best_slot_key.split("_"))
                    
                    # Cập nhật slots đã dùng
                    teacherSlot[teacher_id].add(period_id)
                    roomSlot[room_id].add(period_id)

                    schedule.append({
                        "course_class_id": cc.course_class_id,
                        "room_id": room_id,
                        "period_id": period_id
                    })
                else:
                    continue
    
    # Lưu schedule vào database
    try:
        # Tạo mapping period_id -> day_of_week và period_number
        period_mapping = {}
        for period in periods:
            day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
            period_mapping[period.period_id] = {
                'day_of_week': day_map.get(period.day, 1),
                'period_number': period.period_number
            }
        
        # Lưu schedule mới
        for item in schedule:
            period_info = period_mapping.get(item['period_id'])
            if period_info:
                new_schedule = Schedule(
                    course_class_id=item['course_class_id'],
                    room_id=item['room_id'],
                    day_of_week=period_info['day_of_week'],
                    period_start=item['period_id'],
                    period_end=item['period_id']  # Assuming single period for now
                )
                db.add(new_schedule)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to save schedule: {str(e)}"}
    
def generate_schedule(db: Session, program_id: int, semester_id: int = None, total_weeks: int = 10):
    """
    Tạo thời khóa biểu hoàn chỉnh cho học kỳ:
    1. Tự động tạo template nếu cần
    2. Generate lịch cho 10 tuần từ template
    """
    
    # Bước 1: Lấy semester_id nếu không được cung cấp
    if not semester_id:
        latest_semester = db.query(Semester).order_by(desc(Semester.semester_id)).first()
        if not latest_semester:
            return {"error": "No semester found"}
        semester_id = latest_semester.semester_id
    
    # Bước 2: Generate lịch cho cả học kỳ (sẽ tự động tạo template nếu cần)
    print(f"Generating complete semester schedule for {total_weeks} weeks...")
    semester_result = generate_semester_schedule(db, program_id, semester_id, total_weeks, force_recreate_template=True)
    
    if "error" in semester_result:
        return semester_result
    
    return {
        "message": "Successfully generated complete semester schedule",
        "semester_info": semester_result
    }


def get_schedule_by_week(db: Session, program_id: int, semester_id: int, week_number: int):
    """Lấy lịch học của một tuần cụ thể"""
    
    # Lấy courses của chương trình hiện tại
    current_semester_courses = get_courses_for_current_semester(db, program_id)
    if not current_semester_courses:
        return []
    
    course_ids = [course.course_id for course in current_semester_courses]
    courseClasses = db.query(CourseClass).join(Course).filter(
        Course.course_id.in_(course_ids)
    ).all() if course_ids else []
    
    current_class_ids = [cc.course_class_id for cc in courseClasses]
    
    schedules = db.query(Schedule).filter(
        Schedule.semester_id == semester_id,
        Schedule.week_number == week_number,
        Schedule.course_class_id.in_(current_class_ids)
    ).all()
    
    result = []
    for sched in schedules:
        result.append({
            "schedule_id": sched.schedule_id,
            "course_class_id": sched.course_class_id,
            "room_id": sched.room_id,
            "day_of_week": sched.day_of_week,
            "period_start": sched.period_start,
            "period_end": sched.period_end,
            "week_number": sched.week_number,
            "specific_date": sched.specific_date.isoformat() if sched.specific_date else None,
            "semester_id": sched.semester_id
        })
    
    return result