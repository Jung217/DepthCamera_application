import cv2
import numpy as np
import matplotlib.pyplot as plt

# 讀取深度影像
depth_image_path = 'C:/Users/alex2/Desktop/depth_output.png'
depth_image = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)

# 增強影像對比度（選擇性，根據需要增強細節）
depth_image = cv2.equalizeHist(depth_image)

# 使用 Canny 邊緣檢測（調整參數以提取更多邊緣）
edges = cv2.Canny(depth_image, 30, 100)

# 尋找輪廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 創建空白影像以畫出輪廓
contour_image = np.zeros_like(depth_image)

# 畫出輪廓
cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 1)

# 顯示結果
plt.imshow(contour_image, cmap='gray')
plt.axis('off')
plt.show()

# 儲存結果
contour_image_path = '/mnt/data/contour_image.png'
cv2.imwrite(contour_image_path, contour_image)
