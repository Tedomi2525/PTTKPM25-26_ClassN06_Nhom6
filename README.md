```
qldt_backend/ 
│── app/ 
│   │── main.py                  # Điểm vào chính của FastAPI, khởi tạo app và include tất cả router
│   │── database.py              # Kết nối PostgreSQL, định nghĩa SessionLocal và Base cho SQLAlchemy
│   │── __init__.py              # Đánh dấu app là package Python
│
│   │── core/                    # Cấu hình hệ thống và các helper chung
│   │   │── config.py            # Biến môi trường, cấu hình database, JWT, các setting chung
│   │   │── security.py          # Xử lý JWT token, hash password, kiểm tra quyền hạn (role/permission)
│   │   │── __init__.py          # Package init
│
│   │── models/                  # Các ORM models, mapping với bảng trong database
│   │   │── user.py              # Bảng người dùng: sinh viên, giảng viên, admin
│   │   │── course.py            # Bảng môn học và lớp học
│   │   │── program.py           # Bảng chương trình đào tạo và môn học thuộc chương trình
│   │   │── semester.py          # Bảng học kỳ
│   │   │── timetable.py         # Bảng thời khóa biểu, mẫu thời khóa biểu, các tiết học
│   │   │── room.py              # Bảng phòng học và tiết học
│   │   │── attendance.py        # Bảng điểm danh, logs, khuôn mặt học sinh
│   │   │── __init__.py
│
│   │── schemas/                 # Các schema Pydantic dùng để validate request và response
│   │   │── user.py
│   │   │── course.py
│   │   │── program.py
│   │   │── semester.py
│   │   │── timetable.py
│   │   │── room.py
│   │   │── attendance.py
│   │   │── auth.py              # Schema cho đăng nhập và JWT token
│   │   │── __init__.py
│
│   │── services/                # Xử lý nghiệp vụ, logic giữa routers và database
│   │   │── auth_service.py      # Xử lý đăng nhập, JWT, đăng ký user
│   │   │── user_service.py      # CRUD người dùng, sinh viên, giảng viên
│   │   │── course_service.py    # CRUD môn học, lớp học
│   │   │── program_service.py   # CRUD chương trình đào tạo và môn học thuộc chương trình
│   │   │── semester_service.py  # CRUD học kỳ
│   │   │── timetable_service.py # Tạo và sinh thời khóa biểu tự động
│   │   │── room_service.py      # CRUD phòng học và tiết học
│   │   │── attendance_service.py# Quản lý điểm danh, logs
│   │   │── __init__.py
│
│   │── routers/                 # Các endpoint API
│   │   │── auth.py              # Routes đăng nhập, lấy token
│   │   │── users.py             # Quản lý người dùng, sinh viên, giảng viên
│   │   │── courses.py           # Quản lý môn học
│   │   │── programs.py          # Quản lý chương trình đào tạo
│   │   │── semesters.py         # Quản lý học kỳ
│   │   │── timetables.py        # Quản lý thời khóa biểu
│   │   │── rooms.py             # Quản lý phòng học và tiết học
│   │   │── attendances.py       # Điểm danh học sinh
│   │   │── __init__.py
│
│   │── utils/                   # Các hàm tiện ích dùng chung
│   │   │── helpers.py           # Các hàm hỗ trợ xử lý logic chung
│   │   │── validators.py        # Hàm validate dữ liệu, kiểm tra định dạng
│   │   │── __init__.py
│
│── migrations/                  # Thư mục Alembic quản lý version của database
│── tests/                       # Unit test cho các module
│   │── test_auth.py             # Test các chức năng đăng nhập
│   │── test_users.py            # Test CRUD người dùng
│   │── test_courses.py          # Test CRUD môn học
│
│── requirements.txt             # Liệt kê các package Python cần cài
│── alembic.ini                  # Cấu hình Alembic
│── README.md                    # Hướng dẫn cài đặt, cấu hình, chạy project, mô tả cấu trúc
```

# QLDT Backend - FastAPI

## Yêu cầu
- Python 3.10+
- Git
- Postgresql 17.6

## Cài đặt
### 1. Clone repo

```bash
git clone https://github.com/<your-username>/PTTKPM25-26_ClassN06_Nhom6.git
```
```bash
cd PTTKPM25-26_ClassN06_Nhom6/backend
```

### 2. Tạo virtual environment

```bash 
python -m venv venv
```

```bash 
venv\Scripts\activate
```

### 3. Tạo database dùng PostgreSQL
- Tạo database mới tên `qldt` trong PostgreSQL
- Cấu hình connection string trong project:

    `DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/qldt"`

    Mẫu `DATABASE_URL = "postgresql://postgres:123321@localhost:5432/qldt"`

### 4. Tạo bảng và đổ dữ liệu test
- Cách 1: Dùng SQL raw
    - Chạy file sau trong hệ quản trị cơ sở dữ liệu
        [qldt.sql](backend/qldt.sql)

- Cách 2 (Chưa dùng được): Sử dụng Alembic để tạo các bảng từ models đã định nghĩa:

```bash
alembic revision --autogenerate -m "create initial tables"
```
```bash
alembic upgrade head
```
### 5. Cài dependencies:

```bash 
pip install -r requirements.txt
```
### 6. Chạy server

```bash 
uvicorn app.main:app --reload
```
## Kiểm tra
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs