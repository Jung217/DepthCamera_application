import cv2
import numpy as np
import matplotlib.pyplot as plt

# 讀取影像
image_path = 'C:/Users/alex2/Desktop/result_image.png'
image = cv2.imread(image_path)

# 轉換為灰階，並創建遮罩（黑色部分為缺口）
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)

# 影像修復
inpainted_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

# 顯示修復後的影像
plt.imshow(cv2.cvtColor(inpainted_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# 儲存修復後的影像
inpainted_image_path = './inpainted_image.png'
cv2.imwrite(inpainted_image_path, inpainted_image)

inpainted_image_path