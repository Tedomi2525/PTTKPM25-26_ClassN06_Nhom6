#!/usr/bin/env python3
"""
Script để chạy Alembic migrations và tạo database từ schema

Sử dụng:
python run_migrations.py
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from alembic import command
from alembic.config import Config
from app.database import engine
from app.core.config import settings

def run_migrations():
    """Chạy tất cả migrations để tạo database"""
    
    print("🚀 Đang khởi tạo database schema với Alembic...")
    print(f"📊 Database URL: {settings.DATABASE_URL}")
    
    # Đường dẫn đến file alembic.ini
    alembic_ini_path = backend_dir / "alembic.ini"
    
    if not alembic_ini_path.exists():
        print(f"❌ Không tìm thấy file alembic.ini tại: {alembic_ini_path}")
        return False
    
    # Tạo Alembic config
    alembic_cfg = Config(str(alembic_ini_path))
    
    # Set database URL
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    
    try:
        # Kiểm tra kết nối database
        print("🔗 Kiểm tra kết nối database...")
        with engine.connect() as connection:
            print("✅ Kết nối database thành công!")
        
        # Chạy migration lên phiên bản mới nhất
        print("📦 Đang chạy migrations...")
        command.upgrade(alembic_cfg, "head")
        
        print("✅ Migrations hoàn thành thành công!")
        print("🎉 Database đã được tạo với đầy đủ schema và dữ liệu mẫu!")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy migrations: {str(e)}")
        return False

def check_tables():
    """Kiểm tra các bảng đã được tạo"""
    from sqlalchemy import text
    
    try:
        with engine.connect() as connection:
            # Lấy danh sách tất cả các bảng
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            
            print(f"\n📋 Các bảng đã được tạo ({len(tables)} bảng):")
            for table in tables:
                print(f"  ✓ {table}")
                
            # Kiểm tra một số dữ liệu mẫu
            print("\n📊 Dữ liệu mẫu:")
            
            # Kiểm tra số lượng courses
            result = connection.execute(text("SELECT COUNT(*) FROM courses"))
            course_count = result.scalar()
            print(f"  📚 Courses: {course_count} môn học")
            
            # Kiểm tra số lượng teachers
            result = connection.execute(text("SELECT COUNT(*) FROM teachers"))
            teacher_count = result.scalar()
            print(f"  👨‍🏫 Teachers: {teacher_count} giảng viên")
            
            # Kiểm tra số lượng students
            result = connection.execute(text("SELECT COUNT(*) FROM students"))
            student_count = result.scalar()
            print(f"  👨‍🎓 Students: {student_count} sinh viên")
            
            # Kiểm tra số lượng rooms
            result = connection.execute(text("SELECT COUNT(*) FROM rooms"))
            room_count = result.scalar()
            print(f"  🏢 Rooms: {room_count} phòng học")
            
            return True
            
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra database: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🗃️  ALEMBIC DATABASE MIGRATION TOOL")
    print("=" * 60)
    
    # Chạy migrations
    if run_migrations():
        # Kiểm tra kết quả
        check_tables()
        print("\n" + "=" * 60)
        print("🎯 Hoàn thành! Database đã sẵn sàng sử dụng.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("💥 Có lỗi xảy ra. Vui lòng kiểm tra lại cấu hình.")
        print("=" * 60)
        sys.exit(1)