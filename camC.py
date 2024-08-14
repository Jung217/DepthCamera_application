import pyrealsense2 as rs

# 檢查是否有任何設備連接
ctx = rs.context()
devices = ctx.query_devices()
if len(devices) == 0:
    print("No device connected")
else:
    print("Connected devices:")
    for dev in devices:
        print(dev.get_info(rs.camera_info.name))
