import cv2
import numpy as np

# 讀取影像
image = cv2.imread('E:/NTUST DATA/bag/conD/depth/2885.png')


# 設定一個結構元素（kernel）
# 可以調整 kernel 的大小，例如 (3, 3), (5, 5) 等
kernel = np.ones((5, 5), np.uint8)
dilated_image = cv2.dilate(image, kernel, iterations=1)
dilated_image1 = cv2.dilate(dilated_image, kernel, iterations=1)
dilated_image2 = cv2.dilate(dilated_image1, kernel, iterations=1)
dilated_image3 = cv2.dilate(dilated_image2, kernel, iterations=1)
dilated_image4 = cv2.dilate(dilated_image3, kernel, iterations=1)

# 顯示原始影像和膨脹後的影像
cv2.imshow('Original Image', image)
cv2.imshow('Dilated Image', dilated_image)
cv2.imshow('Dilated Image2', dilated_image1)
cv2.waitKey(0)
cv2.destroyAllWindows()