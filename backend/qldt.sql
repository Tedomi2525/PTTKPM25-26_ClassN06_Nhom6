-- 2. Xóa bảng theo thứ tự phụ thuộc
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

-- 3. USERS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin','teacher','student')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Thêm 6 admin
INSERT INTO users (username, email, password, role)
VALUES
('admin1', 'admin1@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin'),
('admin2', 'admin2@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin'),
('admin3', 'admin3@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin'),
('admin4', 'admin4@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin'),
('admin5', 'admin5@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin'),
('admin6', 'admin6@example.com', '$2b$12$yWdfpKo10oIUlOeX9b4cDOKdD4iEtX8N7Tjc3fB.uxBGjS8dxm7im', 'admin');

-- 4. TEACHERS
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    teacher_code VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO teachers (user_id, teacher_code, department)
VALUES
  (1, 'GV001', 'Công nghệ thông tin'),
	(2, 'GV002', 'Kinh te'),
  (3, 'GV003', 'Toán ứng dụng');


-- 5. STUDENTS
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    student_code VARCHAR(50) UNIQUE NOT NULL,
    class VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (user_id, student_code, class)
VALUES
  (4, 'SV001', 'CNTT1'),
  (5, 'SV002', 'CNTT1'),
  (6, 'SV003', 'CNTT2');


-- 6. COURSES
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    credits INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO courses (course_code, name, credits)
VALUES
  ('CS101', 'Nhập môn Lập trình', 3),
  ('CS102', 'Cấu trúc dữ liệu và Giải thuật', 4),
  ('CS103', 'Cơ sở dữ liệu', 3),
  ('CS104', 'Mạng máy tính', 3),
  ('CS105', 'Trí tuệ nhân tạo', 3);


-- 7. COURSE_CLASSES
CREATE TABLE course_classes (
    course_class_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    teacher_id INT NOT NULL REFERENCES teachers(teacher_id) ON DELETE CASCADE,
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

-- 8. ENROLLMENTS
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
  (1, 1),
  (1, 2),
	(3, 3),
	(3, 5),
	(1, 5),
	(1, 4),
  (2, 3);


-- 9. ROOMS
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    capacity INT NOT NULL,
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


-- 10. PERIODS
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
  (4, '15:45', '18:25');


-- 11. SCHEDULES
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(room_id) ON DELETE CASCADE,
    day_of_week INT CHECK(day_of_week BETWEEN 1 AND 7),
    period_start INT NOT NULL,
    period_end INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_class_id, day_of_week, period_start, period_end)
);

-- 12. TIMETABLE_TEMPLATES
CREATE TABLE timetable_templates (
    template_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    year VARCHAR(20) NOT NULL,
    target_group VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. TIMETABLE_ITEMS
CREATE TABLE timetable_items (
    item_id SERIAL PRIMARY KEY,
    template_id INT NOT NULL REFERENCES timetable_templates(template_id) ON DELETE CASCADE,
    day_of_week INT CHECK(day_of_week BETWEEN 1 AND 7),
    period_start INT NOT NULL,
    period_end INT NOT NULL,
    course_class_id INT REFERENCES course_classes(course_class_id) ON DELETE SET NULL,
    room_id INT REFERENCES rooms(room_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(template_id, day_of_week, period_start, period_end)
);

-- 14. STUDENT_FACES
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

-- 15. ATTENDANCE_LOGS
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

-- 16. ATTENDANCES
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