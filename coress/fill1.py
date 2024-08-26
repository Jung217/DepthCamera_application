import cv2
import numpy as np

# 讀取彩色影像
#image = cv2.imread('C:/Users/alex2/Desktop/result_image.png')
image = cv2.imread('filled_image.png')
# 將影像轉換為灰階以便識別黑色像素
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 找出所有黑色像素的位置
black_pixels = np.where((gray_image == 0))

# 創建一個用於結果的影像，初始化為原彩色影像
result_image = image.copy()

# 定義方向偏移列表，用於檢查鄰近的像素
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# 對於每個黑色像素，找到最近的非黑色像素
for y, x in zip(black_pixels[0], black_pixels[1]):
    radius = 1
    found = False

    while not found:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                ny, nx = y + dy, x + dx

                # 確保搜尋像素在影像範圍內
                if 0 <= ny < result_image.shape[0] and 0 <= nx < result_image.shape[1]:
                    # 檢查是否為非黑色像素
                    if not (result_image[ny, nx] == [0, 0, 0]).all():
                        # 使用該像素的顏色替換黑色像素
                        result_image[y, x] = result_image[ny, nx]
                        found = True
                        break
            if found:
                break

        # 增加半徑
        radius += 1

# 顯示並保存結果
cv2.imshow('Filled Image', result_image)
cv2.imwrite('filled_image.png', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()