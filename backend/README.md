qldt_backend/
│── app/
│   │── main.py                  # Entry FastAPI
│   │── database.py              # Kết nối PostgreSQL
│   │── __init__.py
│
│   │── core/                    # Cấu hình hệ thống
│   │   │── config.py            # Biến môi trường
│   │   │── security.py          # JWT, password hash
│   │   │── __init__.py
│
│   │── models/                  # ORM models (SQLAlchemy)
│   │   │── user.py              # users, teachers, students
│   │   │── course.py            # courses, course_classes
│   │   │── program.py           # programs, program_courses
│   │   │── semester.py          # semesters
│   │   │── timetable.py         # schedules, timetable_templates, timetable_items
│   │   │── room.py              # rooms, periods
│   │   │── attendance.py        # attendances, attendance_logs, student_faces
│   │   │── __init__.py
│
│   │── schemas/                 # Pydantic schema
│   │   │── user.py
│   │   │── course.py
│   │   │── program.py
│   │   │── semester.py
│   │   │── timetable.py
│   │   │── room.py
│   │   │── attendance.py
│   │   │── auth.py
│   │   │── __init__.py
│
│   │── services/                # Logic nghiệp vụ
│   │   │── auth_service.py
│   │   │── user_service.py
│   │   │── course_service.py
│   │   │── program_service.py
│   │   │── semester_service.py
│   │   │── timetable_service.py
│   │   │── room_service.py
│   │   │── attendance_service.py
│   │   │── __init__.py
│
│   │── routers/                 # API endpoints
│   │   │── auth.py              # Đăng nhập
│   │   │── users.py             # Quản lý user, sinh viên, giảng viên
│   │   │── courses.py           # Quản lý môn học
│   │   │── programs.py          # Chương trình đào tạo
│   │   │── semesters.py         # Kỳ học
│   │   │── timetables.py        # Thời khóa biểu
│   │   │── rooms.py             # Phòng học, tiết học
│   │   │── attendances.py       # Điểm danh
│   │   │── __init__.py
│
│   │── utils/                   # Hàm tiện ích chung
│   │   │── helpers.py
│   │   │── validators.py
│   │   │── __init__.py
│
│── migrations/                  # Alembic
│── tests/                       # Unit test
│   │── test_auth.py
│   │── test_users.py
│   │── test_courses.py
│
│── requirements.txt
│── alembic.ini
│── README.md


QLDT Backend - FastAPI

Yêu cầu
- Python 3.10+
- Git

Cài đặt
1. Clone repo

    ```git clone https://github.com/<your-username>/PTTKPM25-26_ClassN06_Nhom6.git```

    ```cd PTTKPM25-26_ClassN06_Nhom6/backend```

2. Tạo virtual environment

    ```python -m venv venv```

    ```venv\Scripts\activate```


3. Cài dependencies:

    ```pip install -r requirements.txt```

4. Chạy server

    ```uvicorn app.main:app --reload```

Kiểm tra
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs