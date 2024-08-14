import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import torch
import argparse
import cv2
import glob
import matplotlib
import numpy as np
import os
import torch

from depth_anything_v2.dpt import DepthAnythingV2

def cut_function(image_path, scale_factor=3.02):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    enlarged_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    start_x = (new_width - 640) // 2
    start_y = (new_height - 480) // 2
    
    result_image = enlarged_image[start_y:start_y + 480, start_x:start_x + 640]

    cv2.imwrite('result_image.png', result_image)
    return result_image

def con_function(img_path, encoder='vitl'):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

    model_configs = {
        'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
        'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
        'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
        'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
    }

    model = DepthAnythingV2(**model_configs[encoder])
    model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
    model = model.to(DEVICE).eval()

    raw_img = cv2.imread(img_path)
    depth = model.infer_image(raw_img) # HxW raw depth map in numpy

    depth_normalized = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)

    depth_uint8 = depth_normalized.astype(np.uint8)

    output_path = "pic/depth_output.png"
    cv2.imwrite(output_path, depth_uint8)

def open_image1():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        label1.config(image=img_tk)
        label1.image = img_tk
    pass

def open_image1():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        label1.config(image=img_tk)
        label1.image = img_tk

        con_function(file_path)
        img1 = Image.open("pic/depth_output.png")
        img_tk1 = ImageTk.PhotoImage(img1)
        label3.config(image=img_tk1)
        label3.image = img_tk1


def open_image2():
    file_path = filedialog.askopenfilename()
    if file_path:
        processed_image = cut_function(file_path)
        img = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(img)
        label2.config(image=img_tk)
        label2.image = img_tk

        img1 = Image.open("pic/riler.png")
        img_tk1 = ImageTk.PhotoImage(img1)
        label4.config(image=img_tk1)
        label4.image = img_tk1

# 創建主窗口
root = tk.Tk()
root.title("Image Processing")

# 創建框架來放置按鈕和標籤
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# 創建打開圖片1的按鈕
button1 = tk.Button(frame, text="Predict Depth", command=open_image1)
button1.grid(row=0, column=0, padx=5, pady=5)

# 創建打開圖片2的按鈕
button2 = tk.Button(frame, text="Crop Image", command=open_image2)
button2.grid(row=0, column=1, padx=5, pady=5)

# 創建標籤來顯示圖片1
label1 = tk.Label(frame)
label1.grid(row=1, column=0, padx=5, pady=5)

# 創建標籤來顯示圖片2
label2 = tk.Label(frame)
label2.grid(row=1, column=1, padx=5, pady=5)

# 創建標籤來顯示圖片4
label4 = tk.Label(frame)
label4.grid(row=1, column=2, padx=5, pady=5)

# 創建標籤來顯示圖片3
label3 = tk.Label(frame)
label3.grid(row=1, column=3, padx=5, pady=5)

# 運行主循環
root.mainloop()
