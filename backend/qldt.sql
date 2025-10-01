
DROP TABLE IF EXISTS attendances;
DROP TABLE IF EXISTS attendance_logs;
DROP TABLE IF EXISTS student_faces;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS semesters;
DROP TABLE IF EXISTS schedule_templates;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS course_classes;
DROP TABLE IF EXISTS program_courses;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS periods;
DROP TABLE IF EXISTS rooms;

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
		
		status VARCHAR(20) DEFAULT ('active') CHECK (status IN ('active', 'inactive')) NOT NULL,

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
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    class VARCHAR(50),                                 -- Lớp (VD: K17-CNTT_4)
    training_program VARCHAR(50),                      -- Khóa đào tạo (VD: DH_K17.40)
    course_years VARCHAR(20),                          -- Niên khóa (VD: 2023-2027)
    education_type VARCHAR(50) CHECK (education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng')),
    faculty VARCHAR(100),                              -- Khoa quản lý
    major VARCHAR(100),                                -- Ngành học
    status VARCHAR(50) CHECK (status IN ('Đang học', 'Bảo lưu', 'Đã tốt nghiệp')),
    position VARCHAR(50),                              -- Chức vụ (VD: Sinh viên, Lớp trưởng)
    avatar VARCHAR(255),                               -- Link ảnh đại diện (lưu path hoặc URL)
    faces BYTEA,                              -- Vector nhúng khuôn mặt

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (
    student_code, first_name, last_name, dob, gender, email, phone,
    class, training_program, course_years, education_type,
    faculty, major, status, position, avatar
) VALUES
('SV23010315', 'Quân', 'Hoàng Minh', '2005-03-15', 'Nam', 'quan.hm@phenikaa-uni.edu.vn', '0912345678',
 'K17-CNTT_4', 'DH_K17.40', '2023-2027', 'Đại học chính quy',
 'Khoa Công nghệ Thông tin', 'Công nghệ thông tin', 'Đang học', 'Sinh viên', '/images/students/quan.jpg'),
 
('SV23010316', 'Lan', 'Nguyen Thi', '2005-07-22', 'Nữ', 'lan.nguyen@phenikaa-uni.edu.vn', '0923456789',
 'K17-CNTT_2', 'DH_K17.40', '2023-2027', 'Đại học chính quy',
 'Khoa CNTT', 'Hệ thống thông tin', 'Đang học', 'Lớp phó', '/images/students/lan.jpg'),

('SV23010317', 'Huy', 'Tran Van', '2005-01-11', 'Nam', 'huy.tran@phenikaa-uni.edu.vn', '0934567890',
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
('CSE702028','Lập trình cho trí tuệ nhân tạo',2),
('CSE703037','Mạng nơron và học sâu',3),
('CSE702043','Phân tích dữ liệu',2),
('CSE703065','Xử lý ngôn ngữ tự nhiên',3),
('FEL704000','Tiếng Anh bổ trợ',3),
('FFS703007','Đại số tuyến tính',3),
('FFS702001','Pháp luật đại cương',2),
('CSE702040','Nhập môn Công nghệ thông tin',3),
('FBE702001','Quản trị học',2),
('FFS703008','Giải tích',3),
('FEL703001','Tiếng Anh 1',3),
('FFS703013','Vật lý 1',3),
('CSE703038','Ngôn ngữ lập trình C',3),
('FEL703002','Tiếng Anh 2',3),
('CSE703024','Toán rời rạc',3),
('EEE703044','Kỹ thuật số',3),
('CSE703029','Lập trình hướng đối tượng',3),
('FEL702003','Tiếng Anh 3',2),
('FFS703002','Triết học Mác - Lê nin',3),
('CSE703006','Cấu trúc dữ liệu và thuật toán',3),
('CSE703008','Cơ sở dữ liệu',3),
('CSE703064','Xây dựng ứng dụng web',3),
('CSE702116','Khoa học dữ liệu và trí tuệ nhân tạo',2),
('FFS703010','Lý thuyết xác suất thống kê',3),
('CSE702036','Mạng máy tính',2),
('CSE702051','Thiết kế web nâng cao',2),
('FFS702003','Kinh tế chính trị Mác - Lênin',2),
('CSE703052','Thuật toán ứng dụng',3),
('CSE703057','Tối ưu hóa',3),
('CSE703066','Xử lý tín hiệu số cho công nghệ thông tin',3),
('CSE702017','Hệ điều hành',2),
('CSE703023','Kiến trúc máy tính',3),
('CSE702025','Kỹ thuật phần mềm',2),
('FFS702004','Chủ nghĩa xã hội khoa học',2),
('CSE703004','An toàn và bảo mật thông tin',3),
('CSE702027','Lập trình cho thiết bị di động',2),
('CSE703048','Phân tích và thiết kế phần mềm',3),
('CSE702117','Kỹ năng viết và thuyết trình bằng Tiếng Anh',2),
('CSE702011','Điện toán đám mây',2),
('CSE703016','Giao diện người máy',3),
('CSE703018','Hệ nhúng',3),
('CSE702000','Tự chọn tự do 2',2),
('CSE702131','Đồ án cơ sở Công nghệ Thông tin',3),
('CSE703010','Đánh giá và kiểm định chất lượng phần mềm*',3),
('CSE702005','Bảo mật ứng dụng và hệ thống',2),
('CSE702063','Ứng dụng phân tán*',2),
('CSE703132','Lập trình C nâng cao',3),
('CSE702022','Khai phá dữ liệu',2),
('CSE702031','Lập trình phân tích dữ liệu với python',2),
('CSE702033','Lập trình trò chơi',2),
('CSE702103','Linux và phần mềm mã nguồn mở',2),
('CSE702046','Phân tích nghiệp vụ kinh doanh',2),
('CSE702049','Quản trị dự án công nghệ thông tin',2),
('CSE702060','Trực quan hoá dữ liệu',2),
('CSE702133','Ứng dụng WebGIS',2),
('CSE703014','Đồ án liên ngành',3),
('CSE703093','An toàn phần mềm',3),
('CSE703112','Bảo mật hệ thống',3),
('CSE703099','Các hệ nhúng',3),
('CSE703007','Chương trình dịch',3),
('CSE703009','Công nghệ .Net',3),
('CSE703097','Công nghệ chuỗi khối',3),
('CSE703130','Công nghệ Java',3),
('CSE703015','Đồ hoạ máy tính và thực tế ảo',3),
('CSE703110','Kiến trúc phần mềm',3),
('CSE703098','Lập trình phân tán',3),
('CSE703032','Lập trình song song',3),
('CSE703102','Thương mại điện tử',3),
('CSE703054','Tích hợp và phân tích dữ liệu lớn',3),
('FFS702005','Lịch sử Đảng cộng sản Việt Nam',2),
('CSE704000','Tự chọn tự do 4',3),
('CSE702053','Thực tập công nghiệp',3),
('FFS702006','Tư tưởng Hồ Chí Minh',2),
('FTS702003','Kỹ năng đàm phán, thương lượng',2),
('FTS702001','Kỹ năng khởi nghiệp và lãnh đạo',2),
('FTS702002','Kỹ năng quản lý dự án',2),
('FTS702004','Kỹ năng tư duy sáng tạo và phản biện',2),
('EEE703068','Thị giác máy tính',3),
('CSE703134','Xử lý dữ liệu GIS thông minh',3),
('CSE704067','Thực tập tốt nghiệp',3),
('CSE710068','Đồ án tốt nghiệp',3),
('FFS701073','Aerobic',2),
('FFS701068','Bóng chuyền',2),
('FFS701069','Bóng đá',2),
('FFS701067','Bóng rổ',2),
('FFS701070','Cầu lông',2),
('FFS701072','Chạy 1',2),
('FFS708066','Giáo dục quốc phòng - an ninh',3),
('DT00001','Kiểm tra năng lực tiếng Anh đầu khóa',2);


-- 5. COURSE_CLASSES
CREATE TABLE course_classes (
    course_class_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    teacher_id INT NOT NULL REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    section VARCHAR(20),
    max_students INT CHECK (max_students > 0),
    min_students INT CHECK (min_students >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO course_classes (course_id, teacher_id, section, max_students, min_students) VALUES
(1,1,'N01',60,15),(1,2,'N02',60,15),
(2,2,'N01',60,15),(2,3,'N02',60,15),
(3,3,'N01',60,15),(3,1,'N02',60,15),
(4,1,'N01',60,15),(4,2,'N02',60,15),
(5,2,'N01',60,15),(5,3,'N02',60,15),
(6,3,'N01',60,15),(6,1,'N02',60,15),
(7,1,'N01',60,15),(7,2,'N02',60,15),
(8,2,'N01',60,15),(8,3,'N02',60,15),
(9,3,'N01',60,15),(9,1,'N02',60,15),
(10,1,'N01',60,15),(10,2,'N02',60,15),
(11,2,'N01',60,15),(11,3,'N02',60,15),
(12,3,'N01',60,15),(12,1,'N02',60,15),
(13,1,'N01',60,15),(13,2,'N02',60,15),
(14,2,'N01',60,15),(14,3,'N02',60,15),
(15,3,'N01',60,15),(15,1,'N02',60,15),
(16,1,'N01',60,15),(16,2,'N02',60,15),
(17,2,'N01',60,15),(17,3,'N02',60,15),
(18,3,'N01',60,15),(18,1,'N02',60,15),
(19,1,'N01',60,15),(19,2,'N02',60,15),
(20,2,'N01',60,15),(20,3,'N02',60,15),
(21,3,'N01',60,15),(21,1,'N02',60,15),
(22,1,'N01',60,15),(22,2,'N02',60,15),
(23,2,'N01',60,15),(23,3,'N02',60,15),
(24,3,'N01',60,15),(24,1,'N02',60,15),
(25,1,'N01',60,15),(25,2,'N02',60,15),
(26,2,'N01',60,15),(26,3,'N02',60,15),
(27,3,'N01',60,15),(27,1,'N02',60,15),
(28,1,'N01',60,15),(28,2,'N02',60,15),
(29,2,'N01',60,15),(29,3,'N02',60,15),
(30,3,'N01',60,15),(30,1,'N02',60,15),
(31,1,'N01',60,15),(31,2,'N02',60,15),
(32,2,'N01',60,15),(32,3,'N02',60,15),
(33,3,'N01',60,15),(33,1,'N02',60,15),
(34,1,'N01',60,15),(34,2,'N02',60,15),
(35,2,'N01',60,15),(35,3,'N02',60,15),
(36,3,'N01',60,15),(36,1,'N02',60,15),
(37,1,'N01',60,15),(37,2,'N02',60,15),
(38,2,'N01',60,15),(38,3,'N02',60,15),
(39,3,'N01',60,15),(39,1,'N02',60,15),
(40,1,'N01',60,15),(40,2,'N02',60,15),
(41,2,'N01',60,15),(41,3,'N02',60,15),
(42,3,'N01',60,15),(42,1,'N02',60,15),
(43,1,'N01',60,15),(43,2,'N02',60,15),
(44,2,'N01',60,15),(44,3,'N02',60,15),
(45,3,'N01',60,15),(45,1,'N02',60,15),
(46,1,'N01',60,15),(46,2,'N02',60,15),
(47,2,'N01',60,15),(47,3,'N02',60,15),
(48,3,'N01',60,15),(48,1,'N02',60,15),
(49,1,'N01',60,15),(49,2,'N02',60,15),
(50,2,'N01',60,15),(50,3,'N02',60,15),
(51,3,'N01',60,15),(51,1,'N02',60,15),
(52,1,'N01',60,15),(52,2,'N02',60,15),
(53,2,'N01',60,15),(53,3,'N02',60,15),
(54,3,'N01',60,15),(54,1,'N02',60,15),
(55,1,'N01',60,15),(55,2,'N02',60,15),
(56,2,'N01',60,15),(56,3,'N02',60,15),
(57,3,'N01',60,15),(57,1,'N02',60,15),
(58,1,'N01',60,15),(58,2,'N02',60,15),
(59,2,'N01',60,15),(59,3,'N02',60,15),
(60,3,'N01',60,15),(60,1,'N02',60,15),
(61,1,'N01',60,15),(61,2,'N02',60,15),
(62,2,'N01',60,15),(62,3,'N02',60,15),
(63,3,'N01',60,15),(63,1,'N02',60,15),
(64,1,'N01',60,15),(64,2,'N02',60,15),
(65,2,'N01',60,15),(65,3,'N02',60,15),
(66,3,'N01',60,15),(66,1,'N02',60,15),
(67,1,'N01',60,15),(67,2,'N02',60,15),
(68,2,'N01',60,15),(68,3,'N02',60,15),
(69,3,'N01',60,15),(69,1,'N02',60,15),
(70,1,'N01',60,15),(70,2,'N02',60,15),
(71,2,'N01',60,15),(71,3,'N02',60,15),
(72,3,'N01',60,15),(72,1,'N02',60,15),
(73,1,'N01',60,15),(73,2,'N02',60,15),
(74,2,'N01',60,15),(74,3,'N02',60,15),
(75,3,'N01',60,15),(75,1,'N02',60,15),
(76,1,'N01',60,15),(76,2,'N02',60,15),
(77,2,'N01',60,15),(77,3,'N02',60,15),
(78,3,'N01',60,15),(78,1,'N02',60,15),
(79,1,'N01',60,15),(79,2,'N02',60,15),
(80,2,'N01',60,15),(80,3,'N02',60,15),
(81,3,'N01',60,15),(81,1,'N02',60,15),
(82,1,'N01',60,15),(82,2,'N02',60,15),
(83,2,'N01',60,15),(83,3,'N02',60,15),
(84,3,'N01',60,15),(84,1,'N02',60,15),
(85,1,'N01',60,15),(85,2,'N02',60,15),
(86,2,'N01',60,15),(86,3,'N02',60,15),
(87,3,'N01',60,15),(87,1,'N02',60,15),
(88,1,'N01',60,15),(88,2,'N02',60,15),
(89,2,'N01',60,15),(89,3,'N02',60,15);


-- 6. ENROLLMENTS
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_class_id)
);

-- 7. ROOMS
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) UNIQUE NOT NULL,
    capacity INT NOT NULL CHECK(capacity > 0),
    camera_stream_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO rooms (room_name, capacity, camera_stream_url)
VALUES
  ('P101', 60, 'rtsp://camera1'),
  ('P102', 70, 'rtsp://camera2'),
  ('Lab1', 70, 'rtsp://camera3'),
  ('Lab2', 70, 'rtsp://camera4'),
  ('Hall', 120, 'rtsp://camera5');

-- 8. PERIODS
CREATE TABLE periods (
    period_id SERIAL PRIMARY KEY,
    period_number INT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    day VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO periods (period_number, start_time, end_time, day)
VALUES
-- Thứ 2
(1, '06:45', '09:25', 'Mon'),
(2, '09:30', '12:10', 'Mon'),
(3, '13:00', '15:40', 'Mon'),
(4, '15:45', '18:25', 'Mon'),

-- Thứ 3
(1, '06:45', '09:25', 'Tue'),
(2, '09:30', '12:10', 'Tue'),
(3, '13:00', '15:40', 'Tue'),
(4, '15:45', '18:25', 'Tue'),

-- Thứ 4
(1, '06:45', '09:25', 'Wed'),
(2, '09:30', '12:10', 'Wed'),
(3, '13:00', '15:40', 'Wed'),
(4, '15:45', '18:25', 'Wed'),

-- Thứ 5
(1, '06:45', '09:25', 'Thu'),
(2, '09:30', '12:10', 'Thu'),
(3, '13:00', '15:40', 'Thu'),
(4, '15:45', '18:25', 'Thu'),

-- Thứ 6
(1, '06:45', '09:25', 'Fri'),
(2, '09:30', '12:10', 'Fri'),
(3, '13:00', '15:40', 'Fri'),
(4, '15:45', '18:25', 'Fri'),

-- Thứ 7
(1, '06:45', '09:25', 'Sat'),
(2, '09:30', '12:10', 'Sat'),
(3, '13:00', '15:40', 'Sat'),
(4, '15:45', '18:25', 'Sat');

-- 16. SEMESTERS
CREATE TABLE semesters (
  semester_id SERIAL PRIMARY KEY,
  semester_name VARCHAR(255),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

INSERT INTO semesters (semester_name, start_time, end_time, created_at, updated_at)
VALUES
('HK_1_2025', '2025-09-01 00:00:00', '2026-01-15 23:59:59', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 9. SCHEDULES
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(room_id) ON DELETE SET NULL,
    day_of_week INT CHECK(day_of_week BETWEEN 1 AND 7),
    period_start INT NOT NULL REFERENCES periods(period_id),
    period_end INT NOT NULL REFERENCES periods(period_id),
    week_number INT CHECK(week_number BETWEEN 1 AND 20),  
    specific_date DATE,                                   
    semester_id INT REFERENCES semesters(semester_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_class_id, day_of_week, period_start, period_end, week_number)
);

-- 10. SCHEDULE_TEMPLATES
CREATE TABLE schedule_templates (
    template_id SERIAL PRIMARY KEY,
    course_class_id INT NOT NULL REFERENCES course_classes(course_class_id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(room_id) ON DELETE SET NULL,
    period_id INT NOT NULL REFERENCES periods(period_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 11. STUDENT_FACES
CREATE TABLE student_faces (
    face_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    embedding_vector BYTEA NOT NULL,           -- Lưu vector nhị phân
    is_primary BOOLEAN DEFAULT FALSE,          -- Đánh dấu ảnh chính
    faiss_index INT,                            -- Vị trí vector trong FAISS index
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo index tối ưu cho truy vấn
CREATE INDEX idx_student_faces_student_id ON student_faces(student_id);
CREATE INDEX idx_student_faces_faiss_index ON student_faces(faiss_index);

-- 12. ATTENDANCE_LOGS
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

-- 13. ATTENDANCES
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

-- 14. PROGRAMS
CREATE TABLE programs (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(150) NOT NULL,  
    department VARCHAR(100),            
    start_year INT NOT NULL,             
    duration INT,                        
    current_semester VARCHAR(10),                  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO programs (program_name, department, start_year, duration)
VALUES
('Công nghệ thông tin 2025-2029', 'Khoa Công nghệ Thông tin', 2025, 4);

-- 15. PROGRAM_COURSES
CREATE TABLE program_courses (
    program_course_id SERIAL PRIMARY KEY,
    program_id INT NOT NULL REFERENCES programs(program_id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    semester_no VARCHAR(10) NOT NULL,              
    is_required BOOLEAN DEFAULT TRUE,       
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(program_id, course_id, semester_no)
);

INSERT INTO program_courses (program_id, course_id, semester_no, is_required) VALUES
(1,1,'HK_1_1',TRUE),(1,2,'HK_1_1',TRUE),(1,3,'HK_1_1',TRUE),(1,4,'HK_1_1',TRUE),(1,5,'HK_1_1',TRUE),(1,6,'HK_1_1',TRUE),(1,7,'HK_1_1',TRUE),
(1,8,'HK_2_1',TRUE),(1,9,'HK_2_1',TRUE),(1,10,'HK_2_1',TRUE),(1,11,'HK_2_1',TRUE),(1,12,'HK_2_1',TRUE),(1,13,'HK_2_1',TRUE),(1,14,'HK_2_1',TRUE),
(1,15,'HK_3_1',TRUE),(1,16,'HK_3_1',TRUE),(1,17,'HK_3_1',TRUE),(1,18,'HK_3_1',TRUE),(1,19,'HK_3_1',TRUE),(1,20,'HK_3_1',TRUE),(1,21,'HK_3_1',TRUE),
(1,22,'HK_1_2',TRUE),(1,23,'HK_1_2',TRUE),(1,24,'HK_1_2',TRUE),(1,25,'HK_1_2',TRUE),(1,26,'HK_1_2',TRUE),(1,27,'HK_1_2',TRUE),(1,28,'HK_1_2',TRUE),
(1,29,'HK_2_2',TRUE),(1,30,'HK_2_2',TRUE),(1,31,'HK_2_2',TRUE),(1,32,'HK_2_2',TRUE),(1,33,'HK_2_2',TRUE),(1,34,'HK_2_2',TRUE),(1,35,'HK_2_2',TRUE),
(1,36,'HK_3_2',TRUE),(1,37,'HK_3_2',TRUE),(1,38,'HK_3_2',TRUE),(1,39,'HK_3_2',TRUE),(1,40,'HK_3_2',TRUE),(1,41,'HK_3_2',TRUE),(1,42,'HK_3_2',TRUE),
(1,43,'HK_1_3',TRUE),(1,44,'HK_1_3',TRUE),(1,45,'HK_1_3',TRUE),(1,46,'HK_1_3',TRUE),(1,47,'HK_1_3',TRUE),(1,48,'HK_1_3',TRUE),(1,49,'HK_1_3',TRUE),
(1,50,'HK_2_3',TRUE),(1,51,'HK_2_3',TRUE),(1,52,'HK_2_3',TRUE),(1,53,'HK_2_3',TRUE),(1,54,'HK_2_3',TRUE),(1,55,'HK_2_3',TRUE),(1,56,'HK_2_3',TRUE),
(1,57,'HK_3_3',TRUE),(1,58,'HK_3_3',TRUE),(1,59,'HK_3_3',TRUE),(1,60,'HK_3_3',TRUE),(1,61,'HK_3_3',TRUE),(1,62,'HK_3_3',TRUE),(1,63,'HK_3_3',TRUE),
(1,64,'HK_1_4',TRUE),(1,65,'HK_1_4',TRUE),(1,66,'HK_1_4',TRUE),(1,67,'HK_1_4',TRUE),(1,68,'HK_1_4',TRUE),(1,69,'HK_1_4',TRUE),(1,70,'HK_1_4',TRUE),
(1,71,'HK_2_4',TRUE),(1,72,'HK_2_4',TRUE),(1,73,'HK_2_4',TRUE),(1,74,'HK_2_4',TRUE),(1,75,'HK_2_4',TRUE),(1,76,'HK_2_4',TRUE),(1,77,'HK_2_4',TRUE),
(1,78,'HK_3_4',TRUE),(1,79,'HK_3_4',TRUE),(1,80,'HK_3_4',TRUE),(1,81,'HK_3_4',TRUE),(1,82,'HK_3_4',TRUE),(1,83,'HK_3_4',TRUE),(1,84,'HK_3_4',TRUE);
