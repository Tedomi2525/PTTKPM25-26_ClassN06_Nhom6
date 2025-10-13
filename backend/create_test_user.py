"""
Script to create test user for login performance testing
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

# Password context (same as in security.py)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_test_user():
    """Create test user SV25000002 with password 123456"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: Missing DATABASE_URL in environment variables.")
        return
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            with connection.begin() as transaction:
                
                # Check if user already exists
                result = connection.execute(text("SELECT * FROM users WHERE username = 'SV25000002'"))
                if result.fetchone():
                    print("✅ User SV25000002 already exists")
                    return
                
                # Hash password
                hashed_password = get_password_hash("123456")
                print(f"🔐 Password hashed: {hashed_password[:50]}...")
                
                # Create user
                user_sql = """
                    INSERT INTO users (username, email, password, role) 
                    VALUES ('SV25000002', 'sv25000002@test.com', :password, 'student')
                    RETURNING user_id
                """
                result = connection.execute(text(user_sql), {"password": hashed_password})
                user_id = result.fetchone()[0]
                print(f"✅ Created user with ID: {user_id}")
                
                # Create student record
                student_sql = """
                    INSERT INTO students (
                        student_code, first_name, last_name, user_id, 
                        email, class, training_program, course_years,
                        education_type, faculty, major, status, position
                    ) VALUES (
                        'SV25000002', 'Test', 'Student', :user_id,
                        'sv25000002@test.com', 'K25-CNTT_TEST', 'DH_K25.40', '2025-2029',
                        'Đại học chính quy', 'Khoa CNTT', 'Công nghệ thông tin', 'Đang học', 'Sinh viên'
                    )
                """
                connection.execute(text(student_sql), {"user_id": user_id})
                print("✅ Created student record")
                
                transaction.commit()
                print("🎉 Test user SV25000002 created successfully!")
                print("   Username: SV25000002")
                print("   Password: 123456")
                
    except Exception as e:
        print(f"❌ Error creating test user: {e}")

if __name__ == "__main__":
    create_test_user()