import sys
import os

# 👉 Thêm thư mục gốc (school_management) vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import cv2
from services.detector.face_detector import detect_faces, crop_faces

def test_face_detection(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Không thể đọc ảnh:", image_path)
        return

    boxes = detect_faces(image)
    print(f"✅ Phát hiện {len(boxes)} khuôn mặt.")

    # Vẽ các bounding boxes
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Hiển thị ảnh với bounding boxes
    cv2.imshow("Detected Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Cắt và lưu thử khuôn mặt đầu tiên (nếu có)
    faces = crop_faces(image, boxes)
    if faces:
        cv2.imwrite("face_crop.jpg", faces[0])
        print("✅ Đã lưu khuôn mặt đầu tiên vào 'face_crop.jpg'.")

# 📌 Gọi hàm test
if __name__ == "__main__":
    test_face_detection("C:/WORKSPACE/fastAPI/school_management/services/detector/abc.jpg")  # 🔁 Thay bằng đường dẫn ảnh của bạn
