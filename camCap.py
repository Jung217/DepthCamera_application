import cv2
import torch
import numpy as np
import os

from depth_anything_v2.dpt import DepthAnythingV2

# 選擇裝置
DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

# 模型配置
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

encoder = 'vitl' # 或 'vits', 'vitb', 'vitg'

# 加載模型
model = DepthAnythingV2(**model_configs[encoder])
model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
model = model.to(DEVICE).eval()

# 創建保存資料夾
image_folder = "D:/depAny/captured_images"
depth_folder = "D:/depAny/depth_maps"

os.makedirs(image_folder, exist_ok=True)
os.makedirs(depth_folder, exist_ok=True)

# 開啟攝影機
cap = cv2.VideoCapture(0)  # 0 表示第一個攝影機設備

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

frame_count = 0  # 計數器，用於保存影像和深度圖

# 即時處理攝影機影像
while True:
    ret, frame = cap.read()  # 捕捉一幀
    if not ret:
        print("Error: Failed to capture image")
        break

    # 推理獲得深度圖
    depth = model.infer_image(frame)  # HxW raw depth map in numpy

    # 將深度圖數據標準化到 0-255 範圍
    depth_normalized = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)

    # 轉換為 8 位格式
    depth_uint8 = depth_normalized.astype(np.uint8)

    # 生成文件名
    image_filename = os.path.join(image_folder, f'image_{frame_count:04d}.png')
    depth_filename = os.path.join(depth_folder, f'depth_{frame_count:04d}.png')

    # 保存影像和深度圖
    cv2.imwrite(image_filename, frame)
    cv2.imwrite(depth_filename, depth_uint8)

    # 顯示影像和深度圖
    cv2.imshow('Original', frame)
    cv2.imshow('Depth Map', depth_uint8)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1  # 更新計數器

# 釋放攝影機和關閉所有視窗
cap.release()
cv2.destroyAllWindows()
