from app.models.room import Room
from app.models.period import Period
from app.models.course_class import CourseClass
from app.models.program_course import ProgramCourse
from app.models.program import Program
from app.models.semester import Semester
from app.models.course import Course
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
import random

def analyze_room_distribution(schedule):
    """
    Phân tích chất lượng phân bổ phòng trong lịch học
    """
    if not schedule:
        return {"total_classes": 0, "classes_with_multiple_rooms": 0, "distribution_score": 0}
    
    # Nhóm theo course_class_id
    class_rooms = {}
    for item in schedule:
        class_id = item['course_class_id']
        room_id = item['room_id']
        
        if class_id not in class_rooms:
            class_rooms[class_id] = set()
        class_rooms[class_id].add(room_id)
    
    # Thống kê
    total_classes = len(class_rooms)
    classes_with_multiple_rooms = sum(1 for rooms in class_rooms.values() if len(rooms) > 1)
    
    # Tính điểm phân bổ (% lớp có nhiều phòng khác nhau)
    distribution_score = (classes_with_multiple_rooms / total_classes * 100) if total_classes > 0 else 0
    
    return {
        "total_classes": total_classes,
        "classes_with_multiple_rooms": classes_with_multiple_rooms,
        "distribution_score": round(distribution_score, 2),
        "class_room_details": {class_id: list(rooms) for class_id, rooms in class_rooms.items()}
    }

def analyze_daily_schedule_distribution(schedule, courseClasses):
    """
    Phân tích phân bổ lịch học theo ngày
    """
    if not schedule:
        return {"total_classes": 0, "daily_analysis": {}, "rest_day_analysis": {}}
    
    # Tạo period_info để lấy thông tin ngày
    periods = []  # Cần lấy từ database, tạm thời dùng mapping cứng
    day_mapping = {
        1: 'Mon', 2: 'Mon', 3: 'Mon', 4: 'Mon',
        5: 'Tue', 6: 'Tue', 7: 'Tue', 8: 'Tue',
        9: 'Wed', 10: 'Wed', 11: 'Wed', 12: 'Wed',
        13: 'Thu', 14: 'Thu', 15: 'Thu', 16: 'Thu',
        17: 'Fri', 18: 'Fri', 19: 'Fri', 20: 'Fri',
        21: 'Sat', 22: 'Sat', 23: 'Sat', 24: 'Sat'
    }
    
    # Nhóm theo class_id và ngày
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
    
    # Phân tích
    daily_analysis = {}
    rest_day_analysis = {}
    classes_over_3_sessions = 0
    classes_with_rest_day = 0
    
    for class_id, daily_count in class_daily_count.items():
        max_sessions_per_day = max(daily_count.values()) if daily_count else 0
        days_count = len(class_days_used[class_id])
        rest_days = 6 - days_count  # Assuming 6 working days (Mon-Sat)
        
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
        
        rest_day_analysis[class_id] = rest_days
    
    total_classes = len(class_daily_count)
    
    return {
        "total_classes": total_classes,
        "classes_over_3_sessions": classes_over_3_sessions,
        "classes_with_rest_day": classes_with_rest_day,
        "rest_day_rate": (classes_with_rest_day / total_classes * 100) if total_classes > 0 else 0,
        "daily_analysis": daily_analysis,
        "rest_day_analysis": rest_day_analysis
    }
    """
    Phân tích các xung đột và phân bổ của các lớp cùng môn học
    """
    if not schedule or not courseClasses:
        return {"same_course_pairs": [], "conflicts": [], "valid_arrangements": []}
    
    # Tạo dict course_id -> list course_classes
    course_groups = {}
    for cc in courseClasses:
        if cc.course_id not in course_groups:
            course_groups[cc.course_id] = []
        course_groups[cc.course_id].append(cc)
    
    same_course_pairs = []
    conflicts = []
    valid_arrangements = []
    
    # Phân tích từng môn có nhiều lớp
    for course_id, classes in course_groups.items():
        if len(classes) > 1:
            # Tìm các cặp lớp cùng thời gian
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
                                
                                # Kiểm tra xung đột
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

def analyze_same_course_conflicts(schedule, courseClasses):
    """
    Phân tích các xung đột và phân bổ của các lớp cùng môn học
    """
    if not schedule or not courseClasses:
        return {"same_course_pairs": [], "conflicts": [], "valid_arrangements": []}
    
    # Tạo dict course_id -> list course_classes
    course_groups = {}
    for cc in courseClasses:
        if cc.course_id not in course_groups:
            course_groups[cc.course_id] = []
        course_groups[cc.course_id].append(cc)
    
    same_course_pairs = []
    conflicts = []
    valid_arrangements = []
    
    # Phân tích từng môn có nhiều lớp
    for course_id, classes in course_groups.items():
        if len(classes) > 1:
            # Tìm các cặp lớp cùng thời gian
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
                                
                                # Kiểm tra xung đột
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
    """
    Determine current semester code for a program based on program creation date
    and the latest semester start time.
    
    Logic:
    - Get the latest semester (highest semester_id)
    - Calculate months difference between program creation and latest semester start
    - If <= 4 months: semester 1, 5-8 months: semester 2, 9-12 months: semester 3
    - Format: HK_1_X where X is the semester number (1, 2, or 3)
    """
    # Get the program
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return None
    
    # Get the latest semester (highest semester_id)
    latest_semester = db.query(Semester).order_by(desc(Semester.semester_id)).first()
    if not latest_semester:
        return None
    
    # Set current semester based on existing value or default to semester 1
    if not program.current_semester:
        current_semester = "HK_1_1"
    elif program.current_semester == f"HK_3_{program.duration}":
        # Already at final semester
        current_semester = "final"
    elif program.current_semester == "final":
        return "final"
    else:
        # Parse current semester: HK_{semester_num}_{year}
        parts = program.current_semester.split('_')
        current_semester_num = int(parts[1])
        current_year = int(parts[2])
        
        if current_semester_num < 3:
            # Move to next semester in same year
            current_semester_num += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"
        else:
            # Move to semester 1 of next year
            current_semester_num = 1
            current_year += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"

    program.current_semester = current_semester
    db.add(program)
    db.commit()
    db.refresh(program)
    
    return current_semester

def get_current_semester_for_program(db: Session, program_id: int):
    """
    Determine current semester code for a program based on program creation date
    and the latest semester start time.
    
    Logic:
    - Get the latest semester (highest semester_id)
    - Calculate months difference between program creation and latest semester start
    - If <= 4 months: semester 1, 5-8 months: semester 2, 9-12 months: semester 3
    - Format: HK_1_X where X is the semester number (1, 2, or 3)
    """
    # Get the program
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return None
    
    # Get the latest semester (highest semester_id)
    latest_semester = db.query(Semester).order_by(desc(Semester.semester_id)).first()
    if not latest_semester:
        return None
    
    # Set current semester based on existing value or default to semester 1
    if not program.current_semester:
        current_semester = "HK_1_1"
    elif program.current_semester == f"HK_3_{program.duration}":
        # Already at final semester
        current_semester = "final"
    elif program.current_semester == "final":
        return "final"
    else:
        # Parse current semester: HK_{semester_num}_{year}
        parts = program.current_semester.split('_')
        current_semester_num = int(parts[1])
        current_year = int(parts[2])
        
        if current_semester_num < 3:
            # Move to next semester in same year
            current_semester_num += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"
        else:
            # Move to semester 1 of next year
            current_semester_num = 1
            current_year += 1
            current_semester = f"HK_{current_semester_num}_{current_year}"

    program.current_semester = current_semester
    db.add(program)
    db.commit()
    db.refresh(program)
    
    return current_semester
    
def get_courses_for_current_semester(db: Session, program_id: int):
    """
    Get all courses that should be in the current semester for a given program.
    """
    
    
    current_semester_code = get_current_semester_for_program(db, program_id)
    if not current_semester_code:
        return []
    
    # Get courses for the current semester
    program_courses = db.query(ProgramCourse).join(Course).filter(
        ProgramCourse.program_id == program_id,
        ProgramCourse.semester_no == current_semester_code
    ).all()

    return [pc.course for pc in program_courses]

def get_timetables(db, program_id: int):
    rooms = db.query(Room).all()
    periods = db.query(Period).all()
    
    # Filter course classes based on program and current semester
    if program_id:
        # Get courses for current semester of the program
        current_semester_courses = get_courses_for_current_semester(db, program_id)
        if not current_semester_courses:
            return "empty"
        else:
            course_ids = [course.course_id for course in current_semester_courses]

        # Filter course classes to only include current semester courses
        courseClasses = db.query(CourseClass).join(Course).filter(
            Course.course_id.in_(course_ids)
        ).all() if course_ids else []

    # return courseClasses

    room_capacity = {r.room_id: r.capacity for r in rooms}
    
    # Tạo mapping từ day string sang số thứ tự (để tính khoảng cách ngày)
    day_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
    
    # Tạo mapping period_id -> (day, period_number)
    period_info = {}
    for p in periods:
        period_info[p.period_id] = (p.day, p.period_number)

    teacherSlot = {}   # teacher_id -> set(period_id)
    roomSlot = {}      # room_id -> set(period_id)
    schedule = []

    for cc in courseClasses:
        teacher_id = cc.teacher_id
        if teacher_id not in teacherSlot:
            teacherSlot[teacher_id] = set()

        # Xác định số ca cần thiết cho môn học này
        sessions_needed = 1  # mặc định 1 ca
        if cc.course:
            if cc.course.credits >= 3:
                sessions_needed = 2  # môn 3+ tín chỉ cần 2 ca/tuần
            else:
                sessions_needed = 1  # môn 2 tín chỉ cần 1 ca/tuần

        # Kiểm tra số phòng khả dụng trước khi xếp lịch
        available_rooms = [room for room in rooms if cc.max_students <= room_capacity[room.room_id]]
        if len(available_rooms) < sessions_needed:
            print(f"Cảnh báo: Lớp {cc.course_class_id} cần {sessions_needed} ca nhưng chỉ có {len(available_rooms)} phòng phù hợp")
            print(f"Gợi ý: Cần tăng sức chứa phòng hoặc tạo thêm lớp học phần với sĩ số nhỏ hơn")
            
            # Tùy chọn: có thể tự động điều chỉnh số ca hoặc đề xuất tách lớp
            if len(available_rooms) > 0:
                print(f"Sẽ sử dụng {len(available_rooms)} phòng khả dụng, có thể một số ca sẽ dùng chung phòng")
                sessions_needed = min(sessions_needed, len(available_rooms))
            else:
                print(f"Không có phòng nào phù hợp cho lớp {cc.course_class_id}")
                continue  # bỏ qua lớp này

        # Lặp để tìm đủ số ca cần thiết
        for session_count in range(sessions_needed):
            # Tính score cho tất cả slot
            scoreTable = {}
            for room in rooms:
                if room.room_id not in roomSlot:
                    roomSlot[room.room_id] = set()
                for period in periods:
                    key = f"{room.room_id}_{period.period_id}"
                    score = 0
                    # Rule 1: phòng đủ sức chứa
                    if cc.max_students <= room_capacity[room.room_id]:
                        score += 5
                    else:
                        score -= 1000  # phòng không đủ sức chứa
                    # Rule 2: giáo viên rảnh
                    if period.period_id not in teacherSlot[teacher_id]:
                        score += 10
                    else:
                        score -= 1000  # slot giáo viên bận
                    # Rule 3: phòng trống hoặc chỉ có lớp cùng môn nhưng khác giáo viên
                    if period.period_id in roomSlot[room.room_id]:
                        # Kiểm tra xem có lớp nào cùng môn và khác giáo viên đang dùng phòng này không
                        room_conflict = True
                        for existing_item in schedule:
                            if (existing_item['period_id'] == period.period_id and 
                                existing_item['room_id'] == room.room_id):
                                # Tìm lớp đang dùng phòng này trong cùng thời gian
                                existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                                if (existing_class and existing_class.course_id == cc.course_id and 
                                    existing_class.teacher_id != cc.teacher_id):
                                    # Cùng môn nhưng khác giáo viên - không xung đột phòng
                                    room_conflict = False
                                    break
                        
                        if room_conflict:
                            score -= 1000  # slot phòng bận
                    # Rule 4: Bỏ ưu tiên slot đầu ngày để tạo sự random
                    # (Rule cũ: if period.period_number == 1: score += 3)
                    
                    # Rule 5: kiểm tra ràng buộc cho môn có nhiều ca
                    existing_periods = [s['period_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if period.period_id in existing_periods:
                        score -= 1000  # trùng ca
                    elif len(existing_periods) > 0 and cc.course:
                        if cc.course.credits == 2:
                            # Môn 2 tín chỉ: chỉ có 1 ca, không cần kiểm tra thêm
                            pass
                        elif cc.course.credits >= 3:
                            # Môn 3+ tín chỉ: 2 ca phải cách nhau ít nhất 1 ngày
                            current_day = day_order[period.day]
                            for ep in existing_periods:
                                if ep in period_info:
                                    existing_day = day_order[period_info[ep][0]]
                                    day_diff = abs(current_day - existing_day)
                                    # Nếu khoảng cách < 2 ngày (ít nhất 1 ngày) thì trừ điểm
                                    if day_diff < 2:
                                        score -= 500  # vi phạm quy tắc cách ít nhất 1 ngày
                    
                    # Rule 6: Ưu tiên phòng khác nhau cho các ca của cùng môn học
                    existing_rooms = [s['room_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    if room.room_id in existing_rooms:
                        score -= 500  # trùng phòng, trừ điểm nặng
                    else:
                        # Bonus cho phòng chưa được sử dụng bởi lớp này
                        score += 50
                    
                    # Rule 6b: Bonus thêm nếu đây là phòng hoàn toàn mới cho lớp này
                    unique_rooms_used = len(set(existing_rooms))
                    if room.room_id not in existing_rooms and unique_rooms_used < sessions_needed:
                        score += 100  # bonus lớn cho phòng mới
                    
                    # Rule 7: Kiểm tra xung đột với các lớp cùng môn học khác
                    for existing_item in schedule:
                        if existing_item['period_id'] == period.period_id:
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if existing_class and existing_class.course_id == cc.course_id:
                                # Cùng môn học
                                if existing_class.teacher_id == cc.teacher_id:
                                    # Cùng giáo viên - không được trùng thời gian
                                    score -= 1000
                                else:
                                    # Khác giáo viên - phải khác phòng
                                    if existing_item['room_id'] == room.room_id:
                                        score -= 800  # trùng phòng với lớp cùng môn
                                    else:
                                        score += 30  # bonus cho việc phân tách tốt
                    
                    # Rule 8: Giới hạn CỨNG không quá 3 ca trong một ngày
                    current_day = period.day
                    sessions_in_day = []
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            s_day = period_info.get(s['period_id'], ('', 0))[0]
                            if s_day == current_day:
                                sessions_in_day.append(s)
                    
                    # Áp dụng ràng buộc cứng
                    if len(sessions_in_day) >= 3:
                        score -= 10000  # CẤM hoàn toàn (tăng penalty lên 10000)
                    elif len(sessions_in_day) == 2:
                        score -= 500   # Trừ điểm nặng cho ca thứ 3
                    
                    # Rule 9: Ưu tiên tạo ngày nghỉ trong tuần
                    # Đếm số ngày đã có lịch học
                    days_with_classes = set()
                    for s in schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            day = period_info.get(s['period_id'], ('', 0))[0]
                            if day:
                                days_with_classes.add(day)
                    
                    # Nếu thêm ngày hiện tại, có bao nhiêu ngày học
                    potential_days_count = len(days_with_classes | {current_day})
                    
                    # Ưu tiên ít ngày học hơn (để có nhiều ngày nghỉ)
                    if potential_days_count <= 4:  # <= 4 ngày học = >= 1 ngày nghỉ
                        score += 100  # bonus lớn cho việc tạo ngày nghỉ
                    elif potential_days_count == 5:
                        score += 50   # bonus nhỏ
                    else:
                        score -= 50   # trừ điểm nếu học quá nhiều ngày
                        
                    scoreTable[key] = score

            # Chọn slot với yếu tố ngẫu nhiên
            if scoreTable:
                # Lọc các slot không vi phạm ràng buộc cứng (score > -1000)
                valid_slots = [(k, v) for k, v in scoreTable.items() if v > -1000]
                
                if valid_slots:
                    # Sắp xếp theo score giảm dần
                    valid_slots.sort(key=lambda x: x[1], reverse=True)
                    
                    # Thêm yếu tố ngẫu nhiên: chọn từ top 20% slots tốt nhất
                    top_count = max(1, len(valid_slots) // 5)  # Lấy 20% top slots, tối thiểu 1
                    top_slots = valid_slots[:top_count]
                    
                    # Random chọn từ top slots
                    best_slot_key, best_score = random.choice(top_slots)
                    room_id, period_id = map(int, best_slot_key.split("_"))
                    
                    # Kiểm tra ưu tiên phòng khác nhau (có thể override random choice)
                    existing_rooms = [s['room_id'] for s in schedule if s['course_class_id'] == cc.course_class_id]
                    
                    # Nếu có slot trong top với phòng mới, ưu tiên chọn slot đó
                    preferred_slots = []
                    for slot_key, score in top_slots:
                        r_id, p_id = map(int, slot_key.split("_"))
                        if len(existing_rooms) == 0 or r_id not in existing_rooms:
                            preferred_slots.append((slot_key, score))
                    
                    if preferred_slots:
                        # Chọn random từ các slot có phòng ưu tiên
                        best_slot_key, best_score = random.choice(preferred_slots)
                        room_id, period_id = map(int, best_slot_key.split("_"))
                else:
                    best_slot_key = None
                    best_score = -float('inf')
                
                # Thực hiện xếp lịch nếu tìm được slot phù hợp
                if best_slot_key and best_score > -1000:
                    room_id, period_id = map(int, best_slot_key.split("_"))
                    
                    # Cập nhật slot đã dùng
                    teacherSlot[teacher_id].add(period_id)
                    
                    # Chỉ cập nhật roomSlot nếu không có lớp cùng môn khác giáo viên
                    room_available_for_same_course = True
                    for existing_item in schedule:
                        if (existing_item['period_id'] == period_id and 
                            existing_item['room_id'] == room_id):
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if (existing_class and existing_class.course_id == cc.course_id and 
                                existing_class.teacher_id != cc.teacher_id):
                                # Cùng môn khác giáo viên - phòng vẫn có thể dùng chung
                                room_available_for_same_course = False
                                break
                    
                    if room_available_for_same_course:
                        roomSlot[room_id].add(period_id)

                    # Thêm vào schedule
                    schedule.append({
                        "course_class_id": cc.course_class_id,
                        "room_id": room_id,
                        "period_id": period_id
                    })
                else:
                    print(f"Không thể xếp lịch cho lớp {cc.course_class_id}, ca {session_count + 1}")
            else:
                print(f"Không có slot khả dụng cho lớp {cc.course_class_id}, ca {session_count + 1}")

    # Phân tích chất lượng phân bổ phòng
    room_analysis = analyze_room_distribution(schedule)
    print(f"Phân tích phân bổ phòng: {room_analysis['classes_with_multiple_rooms']}/{room_analysis['total_classes']} lớp có nhiều phòng khác nhau ({room_analysis['distribution_score']}%)")
    
    # Phân tích các lớp cùng môn
    same_course_analysis = analyze_same_course_conflicts(schedule, courseClasses)
    if same_course_analysis['same_course_pairs']:
        print(f"Phân tích lớp cùng môn: {len(same_course_analysis['valid_arrangements'])}/{len(same_course_analysis['same_course_pairs'])} cặp hợp lệ ({same_course_analysis['valid_rate']:.1f}%)")
        if same_course_analysis['conflicts']:
            print(f"Cảnh báo: {same_course_analysis['total_conflicts']} xung đột được phát hiện")
    
    # Phân tích phân bổ ngày và ngày nghỉ
    daily_analysis = analyze_daily_schedule_distribution(schedule, courseClasses)
    print(f"Phân tích ngày nghỉ: {daily_analysis['classes_with_rest_day']}/{daily_analysis['total_classes']} lớp có ít nhất 1 ngày nghỉ ({daily_analysis['rest_day_rate']:.1f}%)")
    if daily_analysis['classes_over_3_sessions'] > 0:
        print(f"Cảnh báo: {daily_analysis['classes_over_3_sessions']} lớp có hơn 3 ca/ngày")
    
    # Debug: Kiểm tra Rule 8 hoạt động
    debug_rule8_violations = []
    for class_id, analysis in daily_analysis['daily_analysis'].items():
        if analysis['max_sessions_per_day'] > 3:
            debug_rule8_violations.append({
                'class_id': class_id,
                'max_sessions_per_day': analysis['max_sessions_per_day'],
                'daily_breakdown': analysis['daily_breakdown']
            })
    
    if debug_rule8_violations:
        print(f"DEBUG Rule 8: Phát hiện {len(debug_rule8_violations)} lớp vi phạm >3 ca/ngày:")
        for violation in debug_rule8_violations:
            print(f"  Lớp {violation['class_id']}: {violation['max_sessions_per_day']} ca/ngày, chi tiết: {violation['daily_breakdown']}")
    
    return {
        "schedule": [{"index": i+1, **item} for i, item in enumerate(schedule)]
    }
