import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

try:
    for _ in range(30): pipeline.wait_for_frames()

    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame: raise Exception("未捕捉")

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    images = np.hstack((color_image, depth_colormap))

    plt.imshow(cv2.cvtColor(images, cv2.COLOR_BGR2RGB))
    #plt.title("彩色圖像和深度圖像")
    #plt.axis('off')
    plt.show()

finally:
    pipeline.stop()
