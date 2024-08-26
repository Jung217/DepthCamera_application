from PIL import Image

def black_to_transparent(image_path, output_path, tolerance=30):
    def is_nearly_black(r, g, b, tolerance):
        return r < tolerance and g < tolerance and b < tolerance
    
    # 打開圖片
    img = Image.open(image_path).convert("RGBA")
    
    # 獲取圖片的像素數據
    datas = img.getdata()
    
    # 準備新的像素數據
    new_data = []
    for item in datas:
        r, g, b, a = item
        if is_nearly_black(r, g, b, tolerance):
            # 將接近黑色的像素轉為透明
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    
    # 更新圖片數據
    img.putdata(new_data)
    
    # 保存為PNG格式
    img.save(output_path, "PNG")

# 使用範例
black_to_transparent("C:/Users/alex2/Desktop/result_image.png", "output_image.png")
