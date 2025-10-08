"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2024-10-08 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. USERS table
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('password', sa.String(length=512), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("role IN ('admin','teacher','student')", name='users_role_check'),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # 2. TEACHERS table
    op.create_table('teachers',
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('teacher_code', sa.String(length=20), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('faculty', sa.String(length=100), nullable=True),
        sa.Column('specialization', sa.String(length=100), nullable=True),
        sa.Column('degree', sa.String(length=50), nullable=True),
        sa.Column('academic_rank', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("gender IN ('Nam', 'Nữ', 'Khác')", name='teachers_gender_check'),
        sa.CheckConstraint("degree IN ('Cử nhân', 'Thạc sĩ', 'Tiến sĩ')", name='teachers_degree_check'),
        sa.CheckConstraint("academic_rank IN ('Giảng viên', 'Phó Giáo sư', 'Giáo sư')", name='teachers_academic_rank_check'),
        sa.CheckConstraint("status IN ('active', 'inactive')", name='teachers_status_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('teacher_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('teacher_code')
    )

    # 3. STUDENTS table
    op.create_table('students',
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('student_code', sa.String(length=20), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('class', sa.String(length=50), nullable=True),
        sa.Column('training_program', sa.String(length=50), nullable=True),
        sa.Column('course_years', sa.String(length=20), nullable=True),
        sa.Column('education_type', sa.String(length=50), nullable=True),
        sa.Column('faculty', sa.String(length=100), nullable=True),
        sa.Column('major', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('position', sa.String(length=50), nullable=True),
        sa.Column('avatar', sa.String(length=255), nullable=True),
        sa.Column('faces', postgresql.BYTEA(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("gender IN ('Nam', 'Nữ', 'Khác')", name='students_gender_check'),
        sa.CheckConstraint("education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng')", name='students_education_type_check'),
        sa.CheckConstraint("status IN ('Đang học', 'Bảo lưu', 'Đã tốt nghiệp')", name='students_status_check'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('student_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('student_code')
    )

    # 4. COURSES table
    op.create_table('courses',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('course_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('credits', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('credits > 0', name='courses_credits_check'),
        sa.PrimaryKeyConstraint('course_id'),
        sa.UniqueConstraint('course_code')
    )

    # 5. COURSE_CLASSES table
    op.create_table('course_classes',
        sa.Column('course_class_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('section', sa.String(length=20), nullable=True),
        sa.Column('max_students', sa.Integer(), nullable=True),
        sa.Column('min_students', sa.Integer(), nullable=True),
        sa.Column('current_students', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('max_students > 0', name='course_classes_max_students_check'),
        sa.CheckConstraint('min_students >= 0', name='course_classes_min_students_check'),
        sa.CheckConstraint('current_students >= 0 AND current_students <= max_students', name='course_classes_current_students_check'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.teacher_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('course_class_id')
    )

    # 6. ENROLLMENTS table
    op.create_table('enrollments',
        sa.Column('enrollment_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_class_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['course_class_id'], ['course_classes.course_class_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('enrollment_id'),
        sa.UniqueConstraint('student_id', 'course_class_id')
    )

    # 7. ROOMS table
    op.create_table('rooms',
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('room_name', sa.String(length=50), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('camera_stream_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('capacity > 0', name='rooms_capacity_check'),
        sa.PrimaryKeyConstraint('room_id'),
        sa.UniqueConstraint('room_name')
    )

    # 8. PERIODS table
    op.create_table('periods',
        sa.Column('period_id', sa.Integer(), nullable=False),
        sa.Column('period_number', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('day', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('period_id')
    )

    # 9. SEMESTERS table
    op.create_table('semesters',
        sa.Column('semester_id', sa.Integer(), nullable=False),
        sa.Column('semester_name', sa.String(length=255), nullable=True),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('semester_id')
    )

    # 10. SCHEDULES table
    op.create_table('schedules',
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('course_class_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=True),
        sa.Column('period_start', sa.Integer(), nullable=False),
        sa.Column('period_end', sa.Integer(), nullable=False),
        sa.Column('week_number', sa.Integer(), nullable=True),
        sa.Column('specific_date', sa.Date(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint('day_of_week BETWEEN 1 AND 7', name='schedules_day_of_week_check'),
        sa.CheckConstraint('week_number BETWEEN 1 AND 20', name='schedules_week_number_check'),
        sa.ForeignKeyConstraint(['course_class_id'], ['course_classes.course_class_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['period_end'], ['periods.period_id']),
        sa.ForeignKeyConstraint(['period_start'], ['periods.period_id']),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.room_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['semester_id'], ['semesters.semester_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('schedule_id'),
        sa.UniqueConstraint('course_class_id', 'day_of_week', 'period_start', 'period_end', 'week_number')
    )

    # 11. SCHEDULE_TEMPLATES table
    op.create_table('schedule_templates',
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('course_class_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('period_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['course_class_id'], ['course_classes.course_class_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['period_id'], ['periods.period_id']),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.room_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('template_id')
    )

    # 12. STUDENT_FACES table
    op.create_table('student_faces',
        sa.Column('face_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('embedding_vector', postgresql.BYTEA(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('faiss_index', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('face_id')
    )

    # 13. PROGRAMS table
    op.create_table('programs',
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('program_name', sa.String(length=150), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('start_year', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('current_semester', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('program_id')
    )

    # 14. PROGRAM_COURSES table
    op.create_table('program_courses',
        sa.Column('program_course_id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('semester_no', sa.String(length=10), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['program_id'], ['programs.program_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('program_course_id'),
        sa.UniqueConstraint('program_id', 'course_id', 'semester_no')
    )

    # 15. ATTENDANCE_LOGS table
    op.create_table('attendance_logs',
        sa.Column('log_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('detected_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('image_path', sa.Text(), nullable=True),
        sa.Column('face_external_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedules.schedule_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('log_id')
    )

    # 16. ATTENDANCES table
    op.create_table('attendances',
        sa.Column('attendance_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('confirmed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('confirmed_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("status IN ('present','absent','late')", name='attendances_status_check'),
        sa.ForeignKeyConstraint(['confirmed_by'], ['users.user_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedules.schedule_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('attendance_id'),
        sa.UniqueConstraint('student_id', 'schedule_id', 'date')
    )

    # Create indexes
    op.create_index('idx_student_faces_student_id', 'student_faces', ['student_id'])
    op.create_index('idx_student_faces_faiss_index', 'student_faces', ['faiss_index'])
    op.create_index('idx_attendance_logs', 'attendance_logs', ['student_id', 'schedule_id', 'date'])
    op.create_index('idx_attendances', 'attendances', ['student_id', 'date'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_attendances', table_name='attendances')
    op.drop_index('idx_attendance_logs', table_name='attendance_logs')
    op.drop_index('idx_student_faces_faiss_index', table_name='student_faces')
    op.drop_index('idx_student_faces_student_id', table_name='student_faces')
    
    # Drop tables in reverse order
    op.drop_table('attendances')
    op.drop_table('attendance_logs')
    op.drop_table('program_courses')
    op.drop_table('programs')
    op.drop_table('student_faces')
    op.drop_table('schedule_templates')
    op.drop_table('schedules')
    op.drop_table('semesters')
    op.drop_table('periods')
    op.drop_table('rooms')
    op.drop_table('enrollments')
    op.drop_table('course_classes')
    op.drop_table('courses')
    op.drop_table('students')
    op.drop_table('teachers')
    op.drop_table('users')