from app.models.room import Room

course_classes = []

def get_timetables(db):
    rooms = db.query(Room).all()

    print(rooms)

    # periods = [
    #     {"id": 1, "slot": "Mon AM", "day": 1},
    #     {"id": 2, "slot": "Mon PM", "day": 1},
    #     {"id": 3, "slot": "Tue AM", "day": 2},
    #     {"id": 4, "slot": "Tue PM", "day": 2},
    #     {"id": 5, "slot": "Wed AM", "day": 3},
    #     {"id": 6, "slot": "Wed PM", "day": 3},
    #     {"id": 7, "slot": "Thu AM", "day": 4},
    #     {"id": 8, "slot": "Thu PM", "day": 4},
    # ]

    # schedule = []
    # teacher_slot = {}
    # room_slot = {}
    # teacher_day_count = {}  # số ca/giáo viên mỗi ngày
    # course_days = {}        # lưu ngày đã xếp cho môn (để cách ngày)

    # def score(course_class, room, period):
    #     s = 0
    #     if room['capacity'] >= course_class['max_students']:
    #         s += 10
    #     if 'AM' in period['slot']:
    #         s += 1
    #     return s

    # for c in course_classes:
    #     sessions_needed = c["sessions_per_week"]
    #     assigned_days = []
    #     while sessions_needed > 0:
    #         best_score = -1
    #         best_assignment = None
    #         for p in periods:
    #             day = p['day']
    #             # Giới hạn 3 ca/ngày
    #             if teacher_day_count.get((c['teacher'], day), 0) >= 3:
    #                 continue
    #             # Kiểm tra cách ngày nếu cần
    #             if c["sessions_per_week"] > 1 and any(abs(day - d) < 2 for d in assigned_days):
    #                 continue
    #             for r in rooms:
    #                 if teacher_slot.get((c['teacher'], p['id'])):
    #                     continue
    #                 if room_slot.get((r['id'], p['id'])):
    #                     continue
    #                 s = score(c, r, p)
    #                 if s > best_score:
    #                     best_score = s
    #                     best_assignment = {"course_class_id": c['id'], "room_id": r['id'], "period_id": p['id'], "day": day}
    #         if best_assignment:
    #             schedule.append(best_assignment)
    #             day = best_assignment['day']
    #             teacher_slot[(c['teacher'], best_assignment['period_id'])] = True
    #             room_slot[(best_assignment['room_id'], best_assignment['period_id'])] = True
    #             teacher_day_count[(c['teacher'], day)] = teacher_day_count.get((c['teacher'], day), 0) + 1
    #             assigned_days.append(day)
    #             sessions_needed -= 1
    #         else:
    #             print(f"Không xếp được môn {c['course']}, còn {sessions_needed} ca cần xếp")
    #             break

    # # Hiển thị kết quả
    # for s in schedule:
    #     course = next(c for c in course_classes if c['id']==s['course_class_id'])
    #     room = next(r for r in rooms if r['id']==s['room_id'])
    #     period = next(p for p in periods if p['id']==s['period_id'])
    #     print(f"Course {course['course']} -> Room {room['name']} @ {period['slot']}")
