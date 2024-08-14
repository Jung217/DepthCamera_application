import cv2
import numpy as np
import pyrealsense2 as rs

def mask_depth(image, th, threshold=1000):
    th[image > threshold] = 0

def find_obstacle(depth, thresh=20, max_thresh=255, area=500):
    dep = depth.copy()
    mask_depth(depth, dep, 1000)
    dep = (dep / 16).astype(np.uint8)
    
    # Depth image with color map
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(dep, alpha=0.03), cv2.COLORMAP_JET)
    
    # Morphology to reduce noise
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    out = cv2.morphologyEx(dep, cv2.MORPH_OPEN, element)
    
    # Thresholding
    threshold_output = cv2.threshold(dep, thresh, max_thresh, cv2.THRESH_BINARY)[1]
    
    contours, _ = cv2.findContours(threshold_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = [cv2.convexHull(contour, False) for contour in contours]
    result = [h for h in hull if cv2.contourArea(h) >= area]
    
    drawing = np.zeros((threshold_output.shape[0], threshold_output.shape[1], 3), dtype=np.uint8)
    rng = np.random.default_rng(12345)
    
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) < area:
            continue
        color = tuple(rng.integers(0, 255, size=3).tolist())
        cv2.drawContours(drawing, contours, i, color, 1, 8)
        cv2.drawContours(drawing, hull, i, color, 1, 8)
    
    # Convert binary images to 3 channels (RGB)
    contours_image = cv2.cvtColor(drawing, cv2.COLOR_BGR2RGB)
    morphology_image = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)
    
    return depth, contours_image, morphology_image

def main():
    idxImageRes = 640
    idxFrameRate = 30
    
    pipeline = rs.pipeline()
    config = rs.config()
    
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            depth_image = np.asanyarray(depth_frame.get_data())
            raw_depth_image, contours_image, morphology_image = find_obstacle(depth_image, 20, 255, 500)
            
            # Convert raw depth image to 8-bit grayscale image
            raw_depth_image_8bit = cv2.convertScaleAbs(raw_depth_image, alpha=0.03)
            raw_depth_image_colored = cv2.cvtColor(raw_depth_image_8bit, cv2.COLOR_GRAY2BGR)
            
            # Stack images horizontally
            combined_image = np.hstack((raw_depth_image_colored, contours_image, morphology_image))
            
            cv2.imshow("Combined View", combined_image)
            
            if cv2.waitKey(1) == 27:
                break
    finally:
        pipeline.stop()

if __name__ == "__main__":
    main()