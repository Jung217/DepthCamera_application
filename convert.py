import os
from PIL import Image

def crop_and_convert_images(input_folder, output_folder, crop_size=(640, 480)):
    # 確認輸出資料夾存在，如果不存在則建立
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍歷資料夾中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            # 構建完整的文件路徑
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                width, height = img.size
                if width == 1280 and height == 480:
                    # 設定兩個區塊的座標
                    boxes = [
                        (0, 0, 640, 480),       # 左半部
                        (640, 0, 1280, 480),    # 右半部
                    ]
                    for i, box in enumerate(boxes):
                        cropped_img = img.crop(box)
                        # 取得新的文件名並改變副檔名
                        new_filename = os.path.splitext(filename)[0] + f'_{i}.jpg'
                        new_img_path = os.path.join(output_folder, new_filename)
                        # 儲存成 JPG 格式
                        cropped_img.save(new_img_path, 'JPEG')
                        print(f"已處理圖片: {new_img_path}")
                else:
                    print(f"圖片 {filename} 不是 1280x480 尺寸，已跳過。")

# 使用範例
input_folder = 'C:/Users/alex2/Desktop/NTUST/CameraTest/data/T4'  # 替換成你的資料夾路徑
output_folder = 'C:/Users/alex2/Desktop/NTUST/CameraTest/data/T4/T4-1'  # 替換成你想要的輸出資料夾路徑
crop_and_convert_images(input_folder, output_folder)
