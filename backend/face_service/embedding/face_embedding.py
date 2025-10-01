


from .models_services import net
import torch
import os
from ..face_alignment import align
import numpy as np
import random

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def fix_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

fix_seed()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

adaface_models = {
    'ir_101': os.path.join(BASE_DIR, "models_services", "adaface_ir101_webface12m.ckpt"),
}
# Load model
def load_pretrained_model(architecture='ir_101'):
    assert architecture in adaface_models.keys(), "Architecture không hợp lệ!"
    model = net.build_model(architecture)
    statedict = torch.load(adaface_models[architecture], map_location='cpu')['state_dict']

    # Bỏ prefix 'model.' trong checkpoint keys
    model_statedict = {key[6:]: val for key, val in statedict.items() if key.startswith('model.')}
    model.load_state_dict(model_statedict, strict=False)
    model.eval()
    return model

# Chuyển ảnh PIL -> tensor chuẩn hóa
def to_input(pil_rgb_image):
    np_img = np.array(pil_rgb_image)
    bgr_img = ((np_img[:, :, ::-1] / 255.0) - 0.5) / 0.5  # RGB -> BGR + normalize [-1,1]
    tensor = torch.tensor([bgr_img.transpose(2, 0, 1)]).float()  # [1,3,H,W]
    return tensor

# Hàm chính: nhận 1 ảnh, trả về 1 embedding
def get_face_embedding(image_path):
    model = load_pretrained_model('ir_101')

    # Align khuôn mặt
    aligned_rgb_img = align.get_aligned_face(image_path)
    if aligned_rgb_img is None:
        raise ValueError(f"Không tìm thấy khuôn mặt trong ảnh: {image_path}")

    # Chuẩn hóa input
    tensor_input = to_input(aligned_rgb_img)

    # Dự đoán embedding
    with torch.no_grad():
        feature, _ = model(tensor_input)  # feature shape: [1, embedding_dim]

    return feature[0]  # trả về vector embedding dạng [embedding_dim]

# # Test
# if __name__ == '__main__':
#     img_path = 'imgs/test.jpg'  # ảnh test
#     embedding = get_face_embedding(img_path)
#     print("Embedding shape:", embedding.shape)
#     print("Embedding vector:", embedding)
