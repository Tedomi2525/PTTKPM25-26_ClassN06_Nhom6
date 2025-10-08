"""Insert sample data

Revision ID: 002
Revises: 001
Create Date: 2024-10-08 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert sample teachers
    op.execute("""
        INSERT INTO teachers (
            teacher_code, first_name, last_name, dob, gender, email, phone, 
            department, faculty, specialization, degree, academic_rank
        ) VALUES
        ('GV2301', 'An', 'Nguyen Van', '1980-05-10', 'Nam', 'an.nguyen@univ.edu', '0912345678',
         'Công nghệ thông tin', 'Khoa học máy tính', 'Trí tuệ nhân tạo', 'Tiến sĩ', 'Giảng viên'),
        
        ('GV2302', 'Binh', 'Tran Thi', '1975-09-21', 'Nữ', 'binh.tran@univ.edu', '0987654321',
         'Kinh tế', 'Tài chính - Ngân hàng', 'Kế toán', 'Thạc sĩ', 'Phó Giáo sư'),
        
        ('GV2303', 'Cuong', 'Le Van', '1982-12-01', 'Nam', 'cuong.le@univ.edu', '0905123456',
         'Toán ứng dụng', 'Xác suất - Thống kê', 'Toán tính toán', 'Tiến sĩ', 'Giáo sư')
    """)

    # Insert sample students
    op.execute("""
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
         'Khoa CNTT', 'Khoa học máy tính', 'Đang học', 'Sinh viên', '/images/students/huy.jpg')
    """)

    # Insert all courses
    courses_data = """
        INSERT INTO courses (course_code, name, credits) VALUES
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
        ('DT00001','Kiểm tra năng lực tiếng Anh đầu khóa',2)
    """
    op.execute(courses_data)

    # Insert rooms
    op.execute("""
        INSERT INTO rooms (room_name, capacity, camera_stream_url) VALUES
        ('P101', 60, 'rtsp://camera1'),
        ('P102', 70, 'rtsp://camera2'),
        ('Lab1', 70, 'rtsp://camera3'),
        ('Lab2', 70, 'rtsp://camera4'),
        ('Hall', 120, 'rtsp://camera5')
    """)

    # Insert periods
    periods_data = """
        INSERT INTO periods (period_number, start_time, end_time, day) VALUES
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
        (4, '15:45', '18:25', 'Sat')
    """
    op.execute(periods_data)

    # Insert sample semester
    op.execute("""
        INSERT INTO semesters (semester_name, start_time, end_time, created_at, updated_at)
        VALUES ('HK_1_2025', '2025-09-01 00:00:00', '2026-01-15 23:59:59', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)

    # Insert sample program
    op.execute("""
        INSERT INTO programs (program_name, department, start_year, duration)
        VALUES ('Công nghệ thông tin 2025-2029', 'Khoa Công nghệ Thông tin', 2025, 4)
    """)


def downgrade() -> None:
    # Delete sample data in reverse order
    op.execute("DELETE FROM programs")
    op.execute("DELETE FROM semesters")
    op.execute("DELETE FROM periods")
    op.execute("DELETE FROM rooms")
    op.execute("DELETE FROM courses")
    op.execute("DELETE FROM students")
    op.execute("DELETE FROM teachers")