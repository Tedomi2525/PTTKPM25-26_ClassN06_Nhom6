from app.models.room import Room
from app.models.period import Period
from app.models.course_class import CourseClass
from app.models.program_course import ProgramCourse
from app.models.program import Program
from app.models.semester import Semester
from app.models.course import Course
from app.models.schedule import Schedule
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

def analyze_room_distribution(schedule):
    """Phân tích chất lượng phân bổ phòng trong lịch học"""
    if not schedule:
        return {"total_classes": 0, "classes_with_multiple_rooms": 0, "distribution_score": 0}
    
    class_rooms = {}
    for item in schedule:
        class_id = item['course_class_id']
        room_id = item['room_id']
        
        if class_id not in class_rooms:
            class_rooms[class_id] = set()
        class_rooms[class_id].add(room_id)
    
    total_classes = len(class_rooms)
    classes_with_multiple_rooms = sum(1 for rooms in class_rooms.values() if len(rooms) > 1)
    distribution_score = (classes_with_multiple_rooms / total_classes * 100) if total_classes > 0 else 0
    
    return {
        "total_classes": total_classes,
        "classes_with_multiple_rooms": classes_with_multiple_rooms,
        "distribution_score": round(distribution_score, 2),
        "class_room_details": {class_id: list(rooms) for class_id, rooms in class_rooms.items()}
    }


def analyze_daily_schedule_distribution(schedule, courseClasses):
    """Phân tích phân bổ lịch học theo ngày"""
    if not schedule:
        return {"total_classes": 0, "daily_analysis": {}, "rest_day_analysis": {}}
    
    # Mapping period_id -> day
    day_mapping = {
        1: 'Mon', 2: 'Mon', 3: 'Mon', 4: 'Mon',
        5: 'Tue', 6: 'Tue', 7: 'Tue', 8: 'Tue',
        9: 'Wed', 10: 'Wed', 11: 'Wed', 12: 'Wed',
        13: 'Thu', 14: 'Thu', 15: 'Thu', 16: 'Thu',
        17: 'Fri', 18: 'Fri', 19: 'Fri', 20: 'Fri',
        21: 'Sat', 22: 'Sat', 23: 'Sat', 24: 'Sat'
    }
    
    class_daily_count = {}
    class_days_used = {}
    
    for item in schedule:
        class_id = item['course_class_id']
        period_id = item['period_id']
        day = day_mapping.get(period_id, 'Unknown')
        
        if class_id not in class_daily_count:
            class_daily_count[class_id] = {}
            class_days_used[class_id] = set()
        
        if day not in class_daily_count[class_id]:
            class_daily_count[class_id][day] = 0
        
        class_daily_count[class_id][day] += 1
        class_days_used[class_id].add(day)
    
    daily_analysis = {}
    classes_over_3_sessions = 0
    classes_with_rest_day = 0
    
    for class_id, daily_count in class_daily_count.items():
        max_sessions_per_day = max(daily_count.values()) if daily_count else 0
        days_count = len(class_days_used[class_id])
        rest_days = 6 - days_count  # 6 working days (Mon-Sat)
        
        daily_analysis[class_id] = {
            "max_sessions_per_day": max_sessions_per_day,
            "days_with_classes": days_count,
            "rest_days": rest_days,
            "daily_breakdown": daily_count
        }
        
        if max_sessions_per_day > 3:
            classes_over_3_sessions += 1
        
        if rest_days >= 1:
            classes_with_rest_day += 1
    
    total_classes = len(class_daily_count)
    
    return {
        "total_classes": total_classes,
        "classes_over_3_sessions": classes_over_3_sessions,
        "classes_with_rest_day": classes_with_rest_day,
        "rest_day_rate": (classes_with_rest_day / total_classes * 100) if total_classes > 0 else 0,
        "daily_analysis": daily_analysis,
        "rest_day_analysis": {class_id: daily_analysis[class_id]["rest_days"] for class_id in daily_analysis}
    }


def analyze_same_course_conflicts(schedule, courseClasses):
    """Phân tích các xung đột và phân bổ của các lớp cùng môn học"""
    if not schedule or not courseClasses:
        return {"same_course_pairs": [], "conflicts": [], "valid_arrangements": []}
    
    course_groups = {}
    for cc in courseClasses:
        if cc.course_id not in course_groups:
            course_groups[cc.course_id] = []
        course_groups[cc.course_id].append(cc)
    
    same_course_pairs = []
    conflicts = []
    valid_arrangements = []
    
    for course_id, classes in course_groups.items():
        if len(classes) > 1:
            for i, class1 in enumerate(classes):
                for class2 in classes[i+1:]:
                    class1_periods = [s for s in schedule if s['course_class_id'] == class1.course_class_id]
                    class2_periods = [s for s in schedule if s['course_class_id'] == class2.course_class_id]
                    
                    for p1 in class1_periods:
                        for p2 in class2_periods:
                            if p1['period_id'] == p2['period_id']:
                                pair_info = {
                                    "course_id": course_id,
                                    "class1_id": class1.course_class_id,
                                    "class2_id": class2.course_class_id,
                                    "period_id": p1['period_id'],
                                    "class1_room": p1['room_id'],
                                    "class2_room": p2['room_id'],
                                    "class1_teacher": class1.teacher_id,
                                    "class2_teacher": class2.teacher_id,
                                }
                                same_course_pairs.append(pair_info)
                                
                                if class1.teacher_id == class2.teacher_id:
                                    conflicts.append({**pair_info, "conflict_type": "same_teacher"})
                                elif p1['room_id'] == p2['room_id']:
                                    conflicts.append({**pair_info, "conflict_type": "same_room"})
                                else:
                                    valid_arrangements.append(pair_info)
    
    return {
        "same_course_pairs": same_course_pairs,
        "conflicts": conflicts,
        "valid_arrangements": valid_arrangements,
        "total_conflicts": len(conflicts),
        "valid_rate": len(valid_arrangements) / len(same_course_pairs) * 100 if same_course_pairs else 100
    }


def get_current_semester_for_program(db: Session, program_id: int):
    """Xác định mã học kỳ hiện tại cho chương trình"""
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return None
    
    latest_semester = db.query(Semester).order_by(desc(Semester.semester_id)).first()
    if not latest_semester:
        return None
    
    if not program.current_semester:
        current_semester = "HK_1_1"
    elif program.current_semester == f"HK_3_{program.duration}":
        current_semester = "final"
    elif program.current_semester == "final":
        return "final"
    else:
        parts = program.current_semester.split('_')
        current_semester_num = int(parts[1])
        current_year = int(parts[2])
        
        if current_semester_num < 3:
            current_semester_num += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"
        else:
            current_semester_num = 1
            current_year += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"

    program.current_semester = current_semester
    db.add(program)
    db.commit()
    db.refresh(program)
    
    return current_semester


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


def generate_schedule(db, program_id: int):
    """Tạo thời khóa biểu tự động với các ràng buộc và quy tắc tối ưu"""
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

        # Xếp lịch từng ca
        for session_count in range(sessions_needed):
            scoreTable = {}
            
            for room in rooms:
                if room.room_id not in roomSlot:
                    roomSlot[room.room_id] = set()
                    
                for period in periods:
                    key = f"{room.room_id}_{period.period_id}"
                    score = 0
                    
                    # Rule 1: Phòng đủ sức chứa
                    if cc.max_students <= room_capacity[room.room_id]:
                        score += 5
                    else:
                        score -= 1000
                    
                    # Rule 2: Giáo viên rảnh
                    if period.period_id not in teacherSlot[teacher_id]:
                        score += 10
                    else:
                        score -= 1000
                    
                    # Rule 3: Phòng trống (trừ lớp cùng môn khác GV)
                    if period.period_id in roomSlot[room.room_id]:
                        room_conflict = True
                        for existing_item in schedule:
                            if (existing_item['period_id'] == period.period_id and 
                                existing_item['room_id'] == room.room_id):
                                existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                                if (existing_class and existing_class.course_id == cc.course_id and 
                                    existing_class.teacher_id != cc.teacher_id):
                                    room_conflict = False
                                    break
                        
                        if room_conflict:
                            score -= 1000
                    
                    # Rule 5: Ràng buộc môn nhiều ca
                    existing_periods = [s['period_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if period.period_id in existing_periods:
                        score -= 1000
                    elif len(existing_periods) > 0 and cc.course and cc.course.credits >= 3:
                        current_day = day_order[period.day]
                        for ep in existing_periods:
                            if ep in period_info:
                                existing_day = day_order[period_info[ep][0]]
                                day_diff = abs(current_day - existing_day)
                                if day_diff < 2:
                                    score -= 500
                    
                    # Rule 6: Ưu tiên phòng khác nhau
                    existing_rooms = [s['room_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if room.room_id in existing_rooms:
                        score -= 500
                    else:
                        score += 50
                        unique_rooms_used = len(set(existing_rooms))
                        if unique_rooms_used < sessions_needed:
                            score += 100
                    
                    # Rule 7: Xung đột lớp cùng môn
                    for existing_item in schedule:
                        if existing_item['period_id'] == period.period_id:
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if existing_class and existing_class.course_id == cc.course_id:
                                if existing_class.teacher_id == cc.teacher_id:
                                    score -= 1000
                                else:
                                    if existing_item['room_id'] == room.room_id:
                                        score -= 800
                                    else:
                                        score += 30
                    
                    # Rule 8: Giới hạn 3 ca/ngày
                    current_day = period.day
                    sessions_in_day = []
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            s_day = period_info.get(s['period_id'], ('', 0))[0]
                            if s_day == current_day:
                                sessions_in_day.append(s)
                    
                    if len(sessions_in_day) >= 3:
                        score -= 10000
                    elif len(sessions_in_day) == 2:
                        score -= 500
                    
                    # Rule 9: Ưu tiên ngày nghỉ
                    days_with_classes = set()
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            day = period_info.get(s['period_id'], ('', 0))[0]
                            if day:
                                days_with_classes.add(day)
                    
                    potential_days_count = len(days_with_classes | {current_day})
                    
                    if potential_days_count <= 4:
                        score += 100
                    elif potential_days_count == 5:
                        score += 50
                    else:
                        score -= 50
                        
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
                    
                    # Kiểm tra roomSlot cho lớp cùng môn
                    room_available_for_same_course = True
                    for existing_item in schedule:
                        if (existing_item['period_id'] == period_id and 
                            existing_item['room_id'] == room_id):
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if (existing_class and existing_class.course_id == cc.course_id and 
                                existing_class.teacher_id != cc.teacher_id):
                                room_available_for_same_course = False
                                break
                    
                    if room_available_for_same_course:
                        roomSlot[room_id].add(period_id)

                    schedule.append({
                        "course_class_id": cc.course_class_id,
                        "room_id": room_id,
                        "period_id": period_id
                    })
                else:
                    continue

    # Phân tích kết quả
    room_analysis = analyze_room_distribution(schedule)
    same_course_analysis = analyze_same_course_conflicts(schedule, courseClasses)
    daily_analysis = analyze_daily_schedule_distribution(schedule, courseClasses)
    
    # Lưu schedule vào database
    try:
        # Xóa schedule cũ của học kỳ hiện tại (không xóa học kỳ cũ)
        current_semester_code = get_current_semester_for_program(db, program_id)
        if current_semester_code and current_semester_code != "empty":
            # Lấy danh sách course_class_id của học kỳ hiện tại
            current_course_ids = [course.course_id for course in current_semester_courses]
            current_class_ids = [cc.course_class_id for cc in courseClasses]
            
            # Chỉ xóa schedule của các lớp trong học kỳ hiện tại
            existing_schedules = db.query(Schedule).filter(
                Schedule.course_class_id.in_(current_class_ids)
            ).all()
            for schedule_item in existing_schedules:
                db.delete(schedule_item)
        
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
    
    return {
        "schedule": [{"index": i+1, **item} for i, item in enumerate(schedule)],
        "analysis": {
            "room_distribution": room_analysis,
            "same_course_analysis": same_course_analysis,
            "daily_distribution": daily_analysis
        },
        "saved_to_db": True
    }