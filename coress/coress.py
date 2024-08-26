import cv2
import numpy as np

# 讀取左邊的影像
left_image = cv2.imread("C:/Users/alex2/Desktop/result_image.png")

# 讀取右邊的深度影像
depth_image = cv2.imread("C:/Users/alex2/Desktop/depth_output.png")

# 確保深度影像和左邊影像尺寸一致
if depth_image.shape != left_image.shape:
    depth_image = cv2.resize(depth_image, (left_image.shape[1], left_image.shape[0]))

# 將深度影像轉換為灰度圖
depth_gray = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)

# 尋找輪廓
# 使用 cv2.Canny 進行邊緣檢測，或者使用 cv2.threshold 和 cv2.findContours 來獲取輪廓
edges = cv2.Canny(depth_gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 複製左邊的影像以便於畫出輪廓
result_image = left_image.copy()

# 將輪廓畫在左邊的影像上
cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

# 顯示結果
cv2.imshow('Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
