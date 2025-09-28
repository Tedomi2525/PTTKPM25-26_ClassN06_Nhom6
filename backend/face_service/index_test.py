import os
import sys
import faiss
import numpy as np

# ====== Fix đường dẫn gốc ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

FAISS_INDEX_PATH = os.path.join(BASE_DIR, "face_service", "face.index")

def inspect_faiss_index():
    if not os.path.exists(FAISS_INDEX_PATH):
        print(f"❌ Không tìm thấy file FAISS index tại: {FAISS_INDEX_PATH}")
        return

    print(f"📂 Đang load FAISS index từ: {FAISS_INDEX_PATH}")
    index = faiss.read_index(FAISS_INDEX_PATH)

    # Số vector đã lưu trong index
    total_vectors = index.ntotal
    print(f"✅ Số lượng vector trong index: {total_vectors}")

    # Kiểm tra dimension của từng vector
    d = index.d
    print(f"✅ Số chiều mỗi vector (embedding size): {d}")

    if total_vectors > 0:
        print("\n=== Xem một vài vector đầu tiên ===")
        # reconstruct các vector đầu tiên
        sample_count = min(5, total_vectors)
        for i in range(sample_count):
            vector = index.reconstruct(i)
            print(f"[{i}] Vector: {np.round(vector[:10], 4)} ...")  # chỉ in 10 giá trị đầu

    print("\n=== Kiểm tra index xong ===")

if __name__ == "__main__":
    inspect_faiss_index()
