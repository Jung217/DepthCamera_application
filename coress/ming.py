import cv2
import numpy as np

# 讀取兩張圖像
image1 = cv2.imread('C:/Users/alex2/Desktop/result_image.png')
image2 = cv2.imread('C:/Users/alex2/Desktop/depth_output.png')

# 確保圖像大小相同
image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# 將圖像轉換為灰階
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# 混合灰階圖像
mixed_gray = cv2.addWeighted(gray1, 0.5, gray2, 0.5, 0)

# 將混合的灰階圖像應用於第一張圖像
hsv_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2YUV)
hsv_image1[:, :, 2] = mixed_gray  # 替換亮度通道

# 將 HSV 圖像轉換回 BGR
final_image = cv2.cvtColor(hsv_image1, cv2.COLOR_HSV2BGR)

# 顯示結果
cv2.imshow('Mixed Image', final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
