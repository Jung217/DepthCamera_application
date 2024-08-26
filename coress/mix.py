import cv2
import numpy as np
import matplotlib.pyplot as plt

# 讀取彩色影像和黑白影像
color_image_path = 'C:/Users/alex2/Desktop/result_image.png'
depth_image_path = 'C:/Users/alex2/Desktop/depth_output.png'

color_image = cv2.imread(color_image_path)
depth_image = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)

# 創建修復遮罩（黑色部分的像素值接近0）
mask = cv2.threshold(depth_image, 10, 255, cv2.THRESH_BINARY_INV)[1]

# 使用影像修復方法來填補彩色影像中的缺口
inpainted_image = cv2.inpaint(color_image, mask, 3, cv2.INPAINT_TELEA)

# 顯示修復後的影像
plt.imshow(cv2.cvtColor(inpainted_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# 儲存修復後的影像
inpainted_image_path = './inpainted_color_image.png'
cv2.imwrite(inpainted_image_path, inpainted_image)

inpainted_image_path
