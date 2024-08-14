import cv2

def enlarge_and_crop(image_path, scale_factor):
    # 讀取圖片
    image = cv2.imread(image_path)
    
    # 獲取圖片尺寸
    height, width = image.shape[:2]
    
    # 計算放大後的尺寸
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    
    # 放大圖片
    enlarged_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # 計算裁剪範圍的起始點
    start_x = (new_width - 640) // 2
    start_y = (new_height - 480) // 2
    
    # 裁剪出中間的640x480區域
    cropped_image = enlarged_image[start_y:start_y + 480, start_x:start_x + 640]
    
    return cropped_image

# 使用範例
image_path = "D:/Downloda/01_Depth.png"
scale_factor = 3.02# 放大倍數 1.51
result_image = enlarge_and_crop(image_path, scale_factor)

# 儲存結果圖片
cv2.imwrite('result_image.png', result_image)
