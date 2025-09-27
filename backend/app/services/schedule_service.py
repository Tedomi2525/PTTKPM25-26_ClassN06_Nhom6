"""
SCHEDULE SERVICE - Dịch vụ quản lý và tạo thời khóa biểu tự động

Module này chứa các function xử lý logic tạo thời khóa biểu tự động cho hệ thống quản lý đào tạo.

ARCHITECTURE OVERVIEW:
======================
1. TEMPLATE-BASED APPROACH:
   - Tạo template cho 1 tuần học (schedule_templates table)
   - Nhân bản template cho toàn bộ học kỳ (schedules table)
   - Cho phép tùy chỉnh từng tuần riêng biệt

2. INTELLIGENT SCHEDULING ALGORITHM:
   - Sử dụng scoring system với hard/soft constraints
   - Tự động xử lý xung đột về phòng học, giáo viên, thời gian
   - Tối ưu hóa việc phân bổ phòng và thời gian học

3. MAIN FUNCTIONS:
   - generate_schedule(): Entry point chính để tạo lịch hoàn chỉnh
   - generate_schedule_template(): Tạo template 1 tuần
   - generate_semester_schedule(): Tạo lịch cho toàn bộ học kỳ
   - get_schedule_*(): Các function lấy lịch theo điều kiện

BUSINESS RULES:
===============
- Môn ≥3 tín chỉ: 2 ca/tuần, môn <3 tín chỉ: 1 ca/tuần
- Giáo viên không thể dạy 2 lớp cùng lúc
- Phòng học phải đủ sức chứa
- Ưu tiên tập trung lịch trong 4-5 ngày/tuần
- Tránh xếp quá nhiều ca trong 1 ngày
"""

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
    """
    Lấy tất cả lịch học hiện tại của một chương trình đào tạo.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        
    Returns:
        List[dict]: Danh sách các lịch học với thông tin chi tiết
        - schedule_id: ID của lịch học
        - course_class_id: ID của lớp học phần  
        - room_id: ID phòng học
        - day_of_week: Thứ trong tuần (1=Thứ 2, 7=Chủ nhật)
        - period_start/end: Ca học bắt đầu/kết thúc
        - created_at/updated_at: Thời gian tạo/cập nhật
    """
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
    """
    Lấy lịch học của một học kỳ cụ thể trong chương trình đào tạo.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        semester_code: Mã học kỳ (ví dụ: "HK_1_1", "HK_2_1")
        
    Returns:
        List[dict]: Danh sách lịch học có thêm thông tin semester_code
    """
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
    """
    Lấy mã học kỳ hiện tại của chương trình đào tạo.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        
    Returns:
        str: Mã học kỳ hiện tại (ví dụ: "HK_1_1") hoặc "HK_1_1" nếu chưa được thiết lập
        None: Nếu không tìm thấy chương trình
        
    Note:
        - Không tự động cập nhật học kỳ hiện tại
        - Trả về giá trị mặc định "HK_1_1" nếu chưa được thiết lập
    """
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return None
    
    # Trả về semester hiện tại mà không tự động cập nhật
    if not program.current_semester:
        return "HK_1_1"  # Default nếu chưa set
    
    return program.current_semester


def get_courses_for_current_semester(db: Session, program_id: int):
    """
    Lấy danh sách tất cả môn học thuộc học kỳ hiện tại của chương trình.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        
    Returns:
        List[Course]: Danh sách các môn học trong học kỳ hiện tại
        []: Danh sách rỗng nếu không tìm thấy môn học hoặc học kỳ
        
    Process:
        1. Lấy mã học kỳ hiện tại của chương trình
        2. Tìm các môn học trong chương trình có semester_no tương ứng
        3. In log để debug số lượng môn học tìm được
    """
    current_semester_code = get_current_semester_for_program(db, program_id)
    if not current_semester_code:
        return []
    
    program_courses = db.query(ProgramCourse).join(Course).filter(
        ProgramCourse.program_id == program_id,
        ProgramCourse.semester_no == current_semester_code
    ).all()

    print(f"Current semester code: {current_semester_code}, Found {len(program_courses)} courses.")
    for pc in program_courses:
        print(f"Course ID: {pc.course_id}, Course Name: {pc.course.name}")

    return [pc.course for pc in program_courses]


def generate_schedule_template(db: Session, program_id: int):
    """
    Tạo mẫu thời khóa biểu tối ưu cho 1 tuần học và lưu vào bảng schedule_templates.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        
    Returns:
        dict: {"template": [list_of_schedule_items]} nếu thành công
        str: "empty" nếu không có môn học trong học kỳ hiện tại
        dict: {"error": "message"} nếu có lỗi
        
    Algorithm:
        Sử dụng thuật toán xếp lịch dựa trên điểm số (scoring algorithm):
        
        1. PREPARATION PHASE:
           - Lấy danh sách phòng học, ca học, lớp học phần
           - Tính toán số ca cần thiết cho mỗi lớp (2 ca cho môn ≥3 tín chỉ, 1 ca cho môn <3 tín chỉ)
           - Khởi tạo tracking slots cho giáo viên và phòng học
           
        2. SCORING PHASE (cho mỗi lớp học phần):
           Tính điểm cho từng cặp (phòng, ca) dựa trên các rules:
           
           HARD CONSTRAINTS (Điểm âm lớn = loại bỏ hoàn toàn):
           - Rule 1: Phòng đủ sức chứa (+5 nếu đủ, -1000 nếu không đủ)
           - Rule 2: Giáo viên rảnh (+10 nếu rảnh, -1000 nếu bận)
           - Rule 3: Phòng trống (-1000 nếu phòng đã bị chiếm)
           - Rule 5: Không trùng ca cho cùng lớp (-1000 nếu trùng)
           
           SOFT CONSTRAINTS (Điểm âm nhỏ = không khuyến khích):
           - Rule 6: Ưu tiên phòng khác nhau (+50 phòng mới, -500 phòng cũ)
           - Rule 7: Xử lý xung đột lớp cùng môn (-200 dùng chung phòng, +50 phòng khác)
           - Rule 8: Giới hạn 3 ca/ngày (-10000 nếu ≥3 ca, -500 nếu 2 ca)
           
           OPTIMIZATION RULES (Cải thiện chất lượng):
           - Rule 9: Ưu tiên tập trung lịch (+100 cho ≤4 ngày/tuần)
           - Tránh xếp các ca quá gần nhau cho môn nhiều tín chỉ
           
        3. SELECTION PHASE:
           - Chọn top 20% slots có điểm cao nhất
           - Ưu tiên slots sử dụng phòng mới
           - Random selection trong nhóm tốt nhất để tránh bias
           
        4. PERSISTENCE PHASE:
           - Xóa template cũ của học kỳ hiện tại
           - Lưu template mới vào database
    """
    # Bước 1: Lấy dữ liệu cơ bản từ database
    rooms = db.query(Room).all()  # Tất cả phòng học
    periods = db.query(Period).all()  # Tất cả ca học trong tuần
    
    # Bước 2: Lọc lớp học theo chương trình và học kỳ hiện tại
    if program_id:
        current_semester_courses = get_courses_for_current_semester(db, program_id)
        if not current_semester_courses:
            return "empty"  # Không có môn học trong học kỳ hiện tại
        
        # Lấy danh sách lớp học phần của các môn trong học kỳ hiện tại
        course_ids = [course.course_id for course in current_semester_courses]
        courseClasses = db.query(CourseClass).join(Course).filter(
            Course.course_id.in_(course_ids)
        ).all() if course_ids else []

    # Bước 3: Chuẩn bị dữ liệu mapping và tracking
    room_capacity = {r.room_id: r.capacity for r in rooms}  # Map room_id -> capacity
    day_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}  # Thứ tự các ngày
    
    # Tạo mapping period_id -> (day, period_number) để tra cứu nhanh
    period_info = {}
    for p in periods:
        period_info[p.period_id] = (p.day, p.period_number)

    # Bước 4: Khởi tạo tracking slots đã sử dụng
    teacherSlot = {}  # teacher_id -> set(period_id): Track ca học của từng giáo viên
    roomSlot = {}     # room_id -> set(period_id): Track ca học của từng phòng
    template_schedule = []  # Kết quả template cuối cùng

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
    
    # Bước 6: Lưu template vào database
    try:
        # Bước 6.1: Xóa template cũ của học kỳ hiện tại để tránh duplicate
        current_semester_code = get_current_semester_for_program(db, program_id)
        if current_semester_code and current_semester_code != "empty":
            current_course_ids = [course.course_id for course in current_semester_courses]
            current_class_ids = [cc.course_class_id for cc in courseClasses]
            
            # Tìm và xóa tất cả template cũ của các lớp trong học kỳ hiện tại
            existing_templates = db.query(ScheduleTemplate).filter(
                ScheduleTemplate.course_class_id.in_(current_class_ids)
            ).all()
            for template_item in existing_templates:
                db.delete(template_item)
        
        # Bước 6.2: Lưu template mới vào database
        for item in template_schedule:
            new_template = ScheduleTemplate(
                course_class_id=item['course_class_id'],
                room_id=item['room_id'],
                period_id=item['period_id']
            )
            db.add(new_template)
        
        db.commit()  # Commit tất cả thay đổi
        
    except Exception as e:
        db.rollback()  # Rollback nếu có lỗi
        return {"error": f"Failed to save schedule template: {str(e)}"}
    
    # Bước 7: Trả về kết quả template với index để dễ debug
    return {
        "template": [{"index": i+1, **item} for i, item in enumerate(template_schedule)]
    }


def generate_semester_schedule(db: Session, program_id: int, semester_id: int, total_weeks: int = 10, force_recreate_template: bool = False):
    """
    Tạo lịch học hoàn chỉnh cho cả học kỳ (mặc định 10 tuần) từ template.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        semester_id: ID của học kỳ
        total_weeks: Tổng số tuần học (mặc định 10)
        force_recreate_template: Có bắt buộc tạo lại template hay không
        
    Returns:
        dict: {"message": ..., "total_schedules": ..., "schedules": [...]} nếu thành công
        dict: {"error": "message"} nếu có lỗi
        
    Process:
        1. Validate semester existence
        2. Get or create schedule template (1 tuần mẫu)
        3. Calculate first Monday of semester
        4. Generate schedule for each week by replicating template
        5. Save all schedules to database with specific dates
    """
    
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
        
        # Bước 3: Tính toán ngày bắt đầu học kỳ (thứ 2 đầu tiên)
        semester_start = semester.start_time.date()
        # Tìm thứ 2 đầu tiên từ ngày bắt đầu học kỳ
        days_ahead = 0 - semester_start.weekday()  # 0 = Monday trong Python
        if days_ahead < 0:  # Nếu ngày bắt đầu không phải thứ 2
            days_ahead += 7  # Tìm thứ 2 tuần tiếp theo
        first_monday = semester_start + timedelta(days=days_ahead)
        
        # Bước 4: Generate lịch cho từng tuần bằng cách nhân bản template
        schedules_created = []
        for week in range(1, total_weeks + 1):
            week_start_date = first_monday + timedelta(weeks=week-1)  # Thứ 2 của tuần thứ week
            
            # Bước 4.1: Tạo lịch cho tuần hiện tại từ template
            for template in templates:
                period_info = period_mapping.get(template.period_id)
                if period_info:
                    # Tính ngày cụ thể trong tuần (ví dụ: thứ 3 của tuần thứ 2)
                    day_offset = period_info['day_of_week'] - 1  # Monday = 0, Tuesday = 1, ...
                    specific_date = week_start_date + timedelta(days=day_offset)
                    
                    # Tạo record lịch học cho ngày cụ thể
                    new_schedule = Schedule(
                        course_class_id=template.course_class_id,
                        room_id=template.room_id,
                        day_of_week=period_info['day_of_week'],
                        period_start=template.period_id,
                        period_end=template.period_id,  # Hiện tại 1 period = 1 ca học
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
    
    # Bước 5: Trả về kết quả tạo lịch
    return {
        "message": f"Successfully generated schedule for {total_weeks} weeks",
        "total_schedules": len(schedules_created),
        "schedules": schedules_created[:50]  # Chỉ trả về 50 schedule đầu để tránh response quá lớn
    }
def generate_schedule_legacy(db, program_id: int):
    """
    [LEGACY - DEPRECATED] Tạo thời khóa biểu tự động cho 1 tuần học.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        
    Returns:
        dict: {"error": "message"} nếu có lỗi
        Không return gì nếu thành công (chỉ lưu vào database)
        
    Warning:
        Function này đã được thay thế bởi generate_schedule_template().
        Chỉ giữ lại để tương thích ngược.
        Logic tương tự generate_schedule_template() nhưng lưu trực tiếp vào bảng Schedule.
    """
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
    [MAIN ENTRY POINT] Tạo thời khóa biểu hoàn chỉnh cho học kỳ.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        semester_id: ID của học kỳ (optional, sẽ dùng học kỳ mới nhất nếu None)
        total_weeks: Tổng số tuần học (mặc định 10)
        
    Returns:
        dict: {"message": ..., "semester_info": {...}} nếu thành công
        dict: {"error": "message"} nếu có lỗi
        
    Process:
        1. Tự động lấy semester_id mới nhất nếu không được cung cấp
        2. Gọi generate_semester_schedule() với force_recreate_template=True
        3. Function này sẽ tự động tạo template nếu cần và generate lịch 10 tuần
        
    Note:
        Đây là function chính được gọi từ API để tạo lịch học hoàn chỉnh.
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
    """
    Lấy lịch học của một tuần cụ thể trong học kỳ.
    
    Args:
        db: Database session
        program_id: ID của chương trình đào tạo
        semester_id: ID của học kỳ
        week_number: Số thứ tự tuần (1, 2, 3, ..., 10)
        
    Returns:
        List[dict]: Danh sách lịch học trong tuần với các thông tin:
        - schedule_id: ID của lịch học
        - course_class_id: ID của lớp học phần
        - room_id: ID phòng học
        - day_of_week: Thư trong tuần (1=Thứ 2, 7=Chủ nhật)
        - period_start/end: Ca học bắt đầu/kết thúc
        - week_number: Số tuần
        - specific_date: Ngày cụ thể (ISO format)
        - semester_id: ID học kỳ
        
    Process:
        1. Lấy danh sách môn học của chương trình trong học kỳ hiện tại
        2. Filter lịch theo semester_id, week_number và course_class_id
        3. Trả về danh sách lịch học với đầy đủ thông tin
    """
    
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