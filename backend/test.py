import psycopg2
from PIL import Image
import os

# Kết nối DB
conn = psycopg2.connect(
    dbname="qldt",
    user="postgres",
    password="luonghongquan",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Lấy đường dẫn avatar từ DB
cur.execute("SELECT avatar FROM students WHERE student_code = '23010315';")
avatar_path = cur.fetchone()[0]
print("Đường dẫn ảnh trong DB:", avatar_path)

# Nếu avatar là đường dẫn tương đối, ghép với thư mục gốc của project
project_root = "C:/WORKSPACE/fastAPI/learn_python/PTTKPM25-26_ClassN06_Nhom6/backend"
full_path = os.path.join(project_root, avatar_path.lstrip('/'))  # loại bỏ dấu '/' đầu
print("Full path:", full_path)

# Kiểm tra file tồn tại trước khi mở
if os.path.exists(full_path):
    img = Image.open(full_path)
    img.show()
else:
    print("❌ File không tồn tại tại:", full_path)

# Đóng kết nối
cur.close() 
conn.close()
