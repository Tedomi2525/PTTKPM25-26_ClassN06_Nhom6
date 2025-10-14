# shared/image.py
import numpy as np
import cv2

def read_imagefile(file_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # BGR
    if img is None:
        raise ValueError("Không đọc được file ảnh")
    return img
