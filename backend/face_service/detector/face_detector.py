from ultralytics import YOLO
import numpy as np
import cv2
from typing import List, Tuple

# Load YOLOv8n-face model (đường dẫn đến file .pt của bạn)
model = YOLO("models_services/yolov8n-face.pt")


def detect_faces(image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Phát hiện bounding box các khuôn mặt trong ảnh sử dụng YOLOv8.

    Args:
        image (np.ndarray): Ảnh đầu vào (BGR).

    Returns:
        List[Tuple[int, int, int, int]]: Danh sách các bounding box (x1, y1, x2, y2).
    """
    results = model.predict(source=image, verbose=False)[0]

    faces = []
    if results.boxes is None or len(results.boxes) == 0:
        return faces

    for box in results.boxes.xyxy:
        x1, y1, x2, y2 = box.tolist()
        faces.append((int(x1), int(y1), int(x2), int(y2)))

    return faces


def crop_faces(image: np.ndarray, boxes: List[Tuple[int, int, int, int]], size: int = 112) -> List[np.ndarray]:
    """
    Cắt các khuôn mặt từ ảnh gốc dựa trên bounding boxes và resize về kích thước chuẩn.

    Args:
        image (np.ndarray): Ảnh gốc.
        boxes (List[Tuple[int, int, int, int]]): Danh sách bounding boxes.
        size (int): Kích thước ảnh đầu ra (mặc định: 112x112).

    Returns:
        List[np.ndarray]: Danh sách ảnh khuôn mặt đã cắt và resize.
    """
    faces = []
    for x1, y1, x2, y2 in boxes:
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)

        face = image[y1:y2, x1:x2]
        if face.size == 0:
            continue

        face_resized = cv2.resize(face, (size, size))
        faces.append(face_resized)

    return faces





