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

from app.models.teacher import Teacher

def get_schedules(db: Session, program_id: int):
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

def get_current_semester_for_program(db: Session, program_id: int) -> str | None:
    try:
        program = db.query(Program).filter(Program.program_id == program_id).first()
        if not program:
            print(f"Program with ID {program_id} not found")
            return None
        if not program.current_semester:
            program.current_semester = "HK_1_1"
            db.commit()
            db.refresh(program)
            return program.current_semester

        return program.current_semester
    except Exception as e:
        print(f"Error in get_current_semester_for_program: {e}")
        db.rollback()
        return None
# if not program.current_semester:
#     program.current_semester = "HK_1_1"
# else:
def advance_semester_after_schedule(db: Session, program_id: int):
    try:
        program = db.query(Program).filter(Program.program_id == program_id).first()
        if not program:
            print(f"Program with ID {program_id} not found")
            return False
        
        current_semester = program.current_semester
        if not current_semester:
            print(f"Current semester for program {program_id} is not set")
            return False
        
        parts = current_semester.split('_')
        if len(parts) != 3:
            print(f"Invalid semester format: {current_semester}")
            return False

        hk, semester, year = parts
        semester = int(semester)
        year = int(year)

        if semester < 3:
            new_semester = f'HK_{semester + 1}_{year}'
        elif semester == 3:
            new_semester = f'HK_1_{year + 1}'
        else:
            print(f"error")
            return False
        
        program.current_semester = new_semester
        db.commit()
        print(f"Advanced program {program_id} to new semester {new_semester}")
        return True
    except Exception as e:
        print(f"Error in advance_semester_after_schedule: {e}")
        db.rollback()
        return False
def get_courses_for_current_semester(db: Session, program_id: int):
    try:
        current_semester_code = get_current_semester_for_program(db, program_id)
        if not current_semester_code:
            print(f"No current semester found for program {program_id}")
            return []
        
        program_courses = db.query(ProgramCourse).join(Course).filter(
            ProgramCourse.program_id == program_id,
            ProgramCourse.semester_no == current_semester_code
        ).all()

        print(f"Current semester code: {current_semester_code}, Found {len(program_courses)} courses.")
        
        valid_courses = []
        for pc in program_courses:
            if pc.course:
                print(f"Course ID: {pc.course_id}, Course Name: {pc.course.name}")
                valid_courses.append(pc.course)
            else:
                print(f"Warning: ProgramCourse {pc.program_course_id} has no associated course")

        return valid_courses
    except Exception as e:
        print(f"Error in get_courses_for_current_semester: {e}")
        return []

def generate_schedule_template(db: Session, program_id: int):
    rooms = db.query(Room).all()
    periods = db.query(Period).all()
    teachers = db.query(Teacher).all()
    print(teachers)
    if program_id:
        current_semester_courses = get_courses_for_current_semester(db, program_id)
        
        if not current_semester_courses:
            return "empty"
        
        course_ids = [course.course_id for course in current_semester_courses]
        courseClasses = db.query(CourseClass).join(Course).filter(
            Course.course_id.in_(course_ids)
        ).all() if course_ids else []

    room_capacity = {r.room_id: r.capacity for r in rooms}
    day_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    
    period_info = {}
    for p in periods:
        period_info[p.period_id] = (p.day, p.period_number)

    teacherSlot = {}
    for teacher in teachers:
        teacherSlot[teacher.teacher_id] = set()
    roomSlot = {}
    template_schedule = []

    for cc in courseClasses:
        if not cc or not cc.teacher_id:
            continue
            
        teacher_id = cc.teacher_id
        if teacher_id not in teacherSlot:
            teacherSlot[teacher_id] = set()

        sessions_needed = 2 if (cc.course and hasattr(cc.course, 'credits') and cc.course.credits >= 3) else 1

        if not cc.max_students:
            continue
            
        available_rooms = [room for room in rooms if cc.max_students <= room_capacity[room.room_id]]
        
        if len(available_rooms) < sessions_needed:
            if len(available_rooms) > 0:
                sessions_needed = min(sessions_needed, len(available_rooms))
            else:
                continue

        for session_count in range(sessions_needed):
            scoreTable = {}
            
            for room in rooms:
                if room.room_id not in roomSlot:
                    roomSlot[room.room_id] = set()
                    
                for period in periods:
                    key = f"{room.room_id}_{period.period_id}"
                    score = 0
                    
                    if cc.max_students <= room_capacity[room.room_id]:
                        score += 5
                    else:
                        score -= 1000
                    
                    if period.period_id not in teacherSlot[teacher_id]:
                        score += 10
                    else:
                        score -= 1000
                    
                    if period.period_id in roomSlot[room.room_id]:
                        score -= 1000
                    
                    existing_periods = [s['period_id'] for s in template_schedule if s['course_class_id'] == cc.course_class_id]
                    if period.period_id in existing_periods:
                        score -= 1000
                    elif len(existing_periods) > 0 and cc.course and hasattr(cc.course, 'credits') and cc.course.credits >= 3:
                        current_day = day_order[period.day]
                        for ep in existing_periods:
                            if ep in period_info:
                                existing_day = day_order[period_info[ep][0]]
                                day_diff = abs(current_day - existing_day)
                                if day_diff < 2:
                                    score -= 500
                    
                    existing_rooms = [s['room_id'] for s in template_schedule if s['course_class_id'] == cc.course_class_id]
                    if room.room_id in existing_rooms:
                        score -= 500
                    else:
                        score += 50
                        unique_rooms_used = len(set(existing_rooms))
                        if unique_rooms_used < sessions_needed:
                            score += 100
                    
                    for existing_item in template_schedule:
                        if existing_item['period_id'] == period.period_id:
                            existing_class = next((c for c in courseClasses if c.course_class_id == existing_item['course_class_id']), None)
                            if existing_class and existing_class.course_id == cc.course_id:
                                if existing_class.teacher_id == cc.teacher_id:
                                    score -= 1000
                                else:
                                    if existing_item['room_id'] == room.room_id:
                                        score -= 200
                                    else:
                                        score += 50
                    
                    current_day = period.day
                    sessions_in_day = []
                    for s in template_schedule:
                        if s['course_class_id'] == cc.course_class_id:
                            s_day = period_info.get(s['period_id'], ('', 0))[0]
                            if s_day == current_day:
                                sessions_in_day.append(s)
                    
                    if len(sessions_in_day) >= 3:
                        score -= 10000
                    elif len(sessions_in_day) == 2:
                        score -= 500
                    
                    days_with_classes = set()
                    for s in template_schedule:
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

            if scoreTable:
                valid_slots = [(k, v) for k, v in scoreTable.items() if v > -1000]
                
                if valid_slots:
                    valid_slots.sort(key=lambda x: x[1], reverse=True)
                    top_count = max(1, len(valid_slots) // 5) if len(valid_slots) >= 5 else len(valid_slots)
                    top_slots = valid_slots[:top_count]
                    
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
                    
                    teacherSlot[teacher_id].add(period_id)
                    roomSlot[room_id].add(period_id)

                    template_schedule.append({
                        "course_class_id": cc.course_class_id,
                        "room_id": room_id,
                        "period_id": period_id
                    })
                else:
                    continue
    
    try:
        current_semester_code = get_current_semester_for_program(db, program_id)
        if current_semester_code and current_semester_code != "empty":
            current_course_ids = [course.course_id for course in current_semester_courses]
            current_class_ids = [cc.course_class_id for cc in courseClasses]
            
            existing_templates = db.query(ScheduleTemplate).filter(
                ScheduleTemplate.course_class_id.in_(current_class_ids)
            ).all()
            for template_item in existing_templates:
                db.delete(template_item)
        
        print(f"Creating {len(template_schedule)} templates in database")
        for item in template_schedule:
            new_template = ScheduleTemplate(
                course_class_id=item['course_class_id'],
                room_id=item['room_id'],
                period_id=item['period_id']
            )
            db.add(new_template)
            print(f"Added template: course_class_id={item['course_class_id']}, room_id={item['room_id']}, period_id={item['period_id']}")
        
        db.commit()
        print("Templates committed to database")
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to save schedule template: {str(e)}"}
    
    return {
        "template": [{"index": i+1, **item} for i, item in enumerate(template_schedule)],
        "semester_code": current_semester_code
    }

def generate_semester_schedule(db: Session, program_id: int, total_weeks: int = 10, force_recreate_template: bool = False):
    semester = db.query(Semester).first()
    semester_id = semester.semester_id if semester else None
    if not semester:
        return {"error": "Semester not found"}

    current_semester_courses = get_courses_for_current_semester(db, program_id)
    if not current_semester_courses:
        return {"error": "No courses found for current semester"}
    
    print(f"Generating schedule for program {semester} for {current_semester_courses} weeks")
    
    course_ids = [course.course_id for course in current_semester_courses]
    courseClasses = db.query(CourseClass).join(Course).filter(
        Course.course_id.in_(course_ids)
    ).all() if course_ids else []
    
    current_class_ids = [cc.course_class_id for cc in courseClasses]
    templates = db.query(ScheduleTemplate).filter(
        ScheduleTemplate.course_class_id.in_(current_class_ids)
    ).all()
    
    if not templates or force_recreate_template:
        template_result = generate_schedule_template(db, program_id)
        
        if isinstance(template_result, str) and template_result == "empty":
            return {"error": "No courses found for current semester"}
        
        if isinstance(template_result, dict) and "error" in template_result:
            return template_result
        
        templates = db.query(ScheduleTemplate).filter(
            ScheduleTemplate.course_class_id.in_(current_class_ids)
        ).all()
        
        if not templates:
            return {"error": "Failed to create schedule template"}
    
    try:
        # Delete existing schedules for this semester and these course classes
        existing_schedules = db.query(Schedule).filter(
            Schedule.semester_id == semester_id,
            Schedule.course_class_id.in_(current_class_ids)
        ).all()
        for schedule_item in existing_schedules:
            db.delete(schedule_item)
        
        # Commit the deletions before creating new ones
        db.commit()
        
        periods = db.query(Period).all()
        period_mapping = {}
        for period in periods:
            day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
            period_mapping[period.period_id] = {
                'day_of_week': day_map.get(period.day, 1),
                'period_number': period.period_number
            }
        
        if not semester.start_time:
            return {"error": "Semester start time is not set"}
            
        semester_start = semester.start_time.date()
        days_ahead = 0 - semester_start.weekday()
        if days_ahead < 0:
            days_ahead += 7
        first_monday = semester_start + timedelta(days=days_ahead)
        
        schedules_created = []
        for week in range(1, total_weeks + 1):
            week_start_date = first_monday + timedelta(weeks=week-1)
            
            for template in templates:
                if not template or not template.period_id or not template.course_class_id or not template.room_id:
                    continue
                    
                period_info = period_mapping.get(template.period_id)
                if period_info:
                    day_offset = period_info['day_of_week'] - 1
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
        # Comment out auto-advance semester to keep students registered in current semester
        # advance_semester_after_schedule(db, program_id)
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to generate semester schedule: {str(e)}"}
    
    return {
        "message": f"Successfully generated schedule for {total_weeks} weeks",
        "total_schedules": len(schedules_created),
        "schedules": schedules_created[:50]
    }

def generate_schedule(db: Session, program_id: int, semester_id: int = None, total_weeks: int = 10):
    if not semester_id:
        latest_semester = db.query(Semester).order_by(desc(Semester.semester_id)).first()
        if not latest_semester:
            return {"error": "No semester found"}
        semester_id = latest_semester.semester_id
    
    print(f"Generating complete semester schedule for {total_weeks} weeks...")
    semester_result = generate_semester_schedule(db, program_id, total_weeks, force_recreate_template=True)
    
    if "error" in semester_result:
        return semester_result
    
    return {
        "message": "Successfully generated complete semester schedule",
        "semester_info": semester_result
    }

def get_schedule_by_week(db: Session, program_id: int, semester_id: int, week_number: int):
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