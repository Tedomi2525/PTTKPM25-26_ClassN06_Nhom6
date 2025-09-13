-- Xóa bảng theo thứ tự phụ thuộc
DROP TABLE IF EXISTS attendances CASCADE;
DROP TABLE IF EXISTS attendance_logs CASCADE;
DROP TABLE IF EXISTS student_faces CASCADE;
DROP TABLE IF EXISTS timetable_items CASCADE;
DROP TABLE IF EXISTS timetable_templates CASCADE;
DROP TABLE IF EXISTS schedules CASCADE;
DROP TABLE IF EXISTS periods CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS course_classes CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. USERS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) UNIQUE,
    password VARCHAR(512) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin','teacher','student')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password, role)
VALUES
('admin1', 'admin1@example.com', '$2b$12$yWdfpKo...', 'admin'),
('admin2', 'admin2@example.com', '$2b$12$yWdfpKo...', 'admin'),
('admin3', 'admin3@example.com', '$2b$12$yWdfpKo...', 'admin'),
('admin4', 'admin4@example.com', '$2b$12$yWdfpKo...', 'admin'),
('admin5', 'admin5@example.com', '$2b$12$yWdfpKo...', 'admin'),
('admin6', 'admin6@example.com', '$2b$12$yWdfpKo...', 'admin');

-- 2. TEACHERS
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,              -- Mã số tự tăng
    teacher_code VARCHAR(20) UNIQUE NOT NULL,   -- Mã GV (VD: GV2301)
    first_name VARCHAR(50) NOT NULL,            -- Tên
    last_name VARCHAR(100) NOT NULL,            -- Họ và đệm
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    dob DATE,                                   -- Ngày sinh
    gender VARCHAR(10) CHECK (gender IN ('Nam', 'Nữ', 'Khác')), -- Giới tính
    email VARCHAR(100) UNIQUE,                  -- Email
    phone VARCHAR(20),                          -- Số điện thoại

    department VARCHAR(100),                    -- Khoa quản lý
    faculty VARCHAR(100),                       -- Bộ môn
    specialization VARCHAR(100),                -- Chuyên ngành

    degree VARCHAR(50) CHECK (degree IN ('Cử nhân', 'Thạc sĩ', 'Tiến sĩ')), 
    academic_rank VARCHAR(50) CHECK (academic_rank IN ('Giảng viên', 'Phó Giáo sư', 'Giáo sư')), 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO teachers (
    teacher_code, first_name, last_name, dob, gender, email, phone, 
    department, faculty, specialization, degree, academic_rank
) VALUES
  ('GV2301', 'An', 'Nguyen Van', '1980-05-10', 'Nam', 'an.nguyen@univ.edu', '0912345678',
   'Công nghệ thông tin', 'Khoa học máy tính', 'Trí tuệ nhân tạo', 'Tiến sĩ', 'Giảng viên'),

  ('GV2302', 'Binh', 'Tran Thi', '1975-09-21', 'Nữ', 'binh.tran@univ.edu', '0987654321',
   'Kinh tế', 'Tài chính - Ngân hàng', 'Kế toán', 'Thạc sĩ', 'Phó Giáo sư'),

  ('GV2303', 'Cuong', 'Le Van', '1982-12-01', 'Nam', 'cuong.le@univ.edu', '0905123456',
   'Toán ứng dụng', 'Xác suất - Thống kê', 'Toán tính toán', 'Tiến sĩ', 'Giáo sư');

-- 3. STUDENTS
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,                     -- Mã tự tăng
    student_code VARCHAR(20) UNIQUE NOT NULL,          -- Mã SV (VD: 23010315)
    first_name VARCHAR(50) NOT NULL,                   -- Tên
    last_name VARCHAR(100) NOT NULL,                   -- Họ và đệm
    dob DATE,                                          -- Ngày sinh
    gender VARCHAR(10) CHECK (gender IN ('Nam', 'Nữ', 'Khác')),
    email VARCHAR(100) UNIQUE,                         -- Email
    phone VARCHAR(20),                                 -- Số điện thoại

    class VARCHAR(50),                                 -- Lớp (VD: K17-CNTT_4)
    training_program VARCHAR(50),                      -- Khóa đào tạo (VD: DH_K17.40)
    course_years VARCHAR(20),                          -- Niên khóa (VD: 2023-2027)
    education_type VARCHAR(50) CHECK (education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng')),
    faculty VARCHAR(100),                              -- Khoa quản lý
    major VARCHAR(100),                                -- Ngành học
    status VARCHAR(50) CHECK (status IN ('Đang học', 'Bảo lưu', 'Đã tốt nghiệp')),
    position VARCHAR(50),                              -- Chức vụ (VD: Sinh viên, Lớp trưởng)
    avatar VARCHAR(255),                               -- Link ảnh đại diện (lưu path hoặc URL)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (
    student_code, first_name, last_name, dob, gender, email, phone,
    class, training_program, course_years, education_type,
    faculty, major, status, position, avatar
) VALUES
('23010315', 'Quân', 'Hoàng Minh', '2005-03-15', 'Nam', 'quan.hm@phenikaa-uni.edu.vn', '0912345678',
 'K17-CNTT_4', 'DH_K17.40', '2023-2027', 'Đại học chính quy',
 'Khoa Công nghệ Thông tin', 'Công nghệ thông tin', 'Đang học', 'Sinh viên', '/images/students/quan.jpg'),
 
('23010316', 'Lan', 'Nguyen Thi', '2005-07-22', 'Nữ', 'lan.nguyen@phenikaa-uni.edu.vn', '0923456789',
 'K17-CNTT_2', 'DH_K17.40', '2023-2027', 'Đại học chính quy',
 'Khoa CNTT', 'Hệ thống thông tin', 'Đang học', 'Lớp phó', '/images/students/lan.jpg'),

('23010317', 'Huy', 'Tran Van', '2005-01-11', 'Nam', 'huy.tran@phenikaa-uni.edu.vn', '0934567890',
 'K17-CNTT_1', 'DH_K17.40', '2023-2027', 'Đại học chính quy',
 'Khoa CNTT', 'Khoa học máy tính', 'Đang học', 'Sinh viên', '/images/students/huy.jpg');

-- 4. COURSES
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    credits INT NOT NULL CHECK (credits > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO courses (course_code, name, credits)
VALUES
  ('CS101', 'Nhập môn Lập trình', 3),
  ('CS102', 'Cấu trúc dữ liệu', 4),
  ('CS103', 'Cơ sở dữ liệu', 3),
  ('CS104', 'Mạng máy tính', 3),
  ('CS105', 'Trí tuệ nhân tạo', 3);

-- 5. COURSE_CLASSES
CREATE TABLE course_classes (
    course_class_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    teacher_id INT NOT NULL REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    semester VARCHAR(20) NOT NULL,
    year VARCHAR(20) NOT NULL,
    section VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO course_classes (course_id, teacher_id, semester, year, section)
VALUES
  (1, 1, 'Fall', '2025', 'A'),
  (2, 1, 'Fall', '2025', 'B'),
  (3, 2, 'Fall', '2025', 'A'),
  (4, 2, 'Fall', '2025', 'A'),
  (5, 3, 'Fall', '2025', 'A');

-- 6. ENROLLMENTS
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_class_id)
);

INSERT INTO enrollments (student_id, course_class_id)
VALUES
  (1, 1), (1, 2), (3, 3), (3, 5), (1, 5), (1, 4), (2, 3);

-- 7. ROOMS
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    capacity INT NOT NULL CHECK(capacity > 0),
    camera_stream_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO rooms (name, capacity, camera_stream_url)
VALUES
  ('P101', 60, 'rtsp://camera1'),
  ('P102', 45, 'rtsp://camera2'),
  ('Lab1', 30, 'rtsp://camera3'),
  ('Lab2', 35, 'rtsp://camera4'),
  ('Hall', 120, 'rtsp://camera5');

-- 8. PERIODS
CREATE TABLE periods (
    period_id SERIAL PRIMARY KEY,
    period_number INT UNIQUE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO periods (period_number, start_time, end_time)
VALUES
  (1, '06:45', '09:25'),
  (2, '09:30', '12:10'),
  (3, '13:00', '15:40'),
  (4, '15:45', '18:25'),
	
	(5, '06:45', '08:30'),
	(6, '09:30', '11:15'),
	(7, '13:00', '14:45'),
	(8, '15:45', '17:30');

-- 9. SCHEDULES
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(room_id) ON DELETE SET NULL,
    day_of_week INT CHECK(day_of_week BETWEEN 1 AND 7),
    period_start INT NOT NULL REFERENCES periods(period_number),
    period_end INT NOT NULL REFERENCES periods(period_number),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_class_id, day_of_week, period_start, period_end)
);

-- 10. TIMETABLE_TEMPLATES
CREATE TABLE timetable_templates (
    template_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    year VARCHAR(20) NOT NULL,
    target_group VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. TIMETABLE_ITEMS
CREATE TABLE timetable_items (
    item_id SERIAL PRIMARY KEY,
    template_id INT NOT NULL REFERENCES timetable_templates(template_id) ON DELETE CASCADE,
    day_of_week INT CHECK(day_of_week BETWEEN 1 AND 7),
    period_start INT NOT NULL REFERENCES periods(period_number),
    period_end INT NOT NULL REFERENCES periods(period_number),
    course_class_id INT REFERENCES course_classes(course_class_id) ON DELETE SET NULL,
    room_id INT REFERENCES rooms(room_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(template_id, day_of_week, period_start, period_end)
);

-- 12. STUDENT_FACES
CREATE TABLE student_faces (
    face_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    image_path TEXT NOT NULL,
    embedding_vector JSONB NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_student_faces_student_id ON student_faces(student_id);
CREATE INDEX idx_student_faces_vector ON student_faces USING GIN (embedding_vector);

-- 13. ATTENDANCE_LOGS
CREATE TABLE attendance_logs (
    log_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    schedule_id INT NOT NULL REFERENCES schedules(schedule_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    image_path TEXT,
    face_external_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_attendance_logs ON attendance_logs(student_id, schedule_id, date);

-- 14. ATTENDANCES
CREATE TABLE attendances (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    schedule_id INT NOT NULL REFERENCES schedules(schedule_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('present','absent','late')) NOT NULL,
    confirmed_at TIMESTAMP,
    confirmed_by INT REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, schedule_id, date)
);

CREATE INDEX idx_attendances ON attendances(student_id, date);