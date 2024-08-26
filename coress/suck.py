from PIL import Image
import numpy as np

# 讀取圖片
image = Image.open('C:/Users/alex2/Desktop/depth_output.png')

# 確保圖片是灰階模式
image = image.convert('L')

# 獲取圖片尺寸
width, height = image.size

# 提取所有像素的灰階值
pixels = np.array(image)

# 將像素數值儲存在文本文件中
with open('pixel_values.txt', 'w') as f:
    for y in range(height):
        for x in range(width):
            value = pixels[y, x]
            f.write(f'Pixel ({x}, {y}) - Value: {value}\n')

print('Pixel values have been saved to pixel_values.txt')
