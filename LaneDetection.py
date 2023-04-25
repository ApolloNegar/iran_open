import cv2
import numpy as np
import time
import LaneDetectionFunctions
from HSV_picker import hsv, hsv_window_trackbar
from steering import calculate_steer
# from motorControl import send_serial
#### debug mode: HSV color picker 
debug_mode_HSV = False 
### debug mode: Region of Interest 
debug_mode_roi = True

def roi(image, points):
    # (height, width) = image.shape
    mask = np.zeros_like(image)

    polygon = np.array([[(0,480), (80,234), (240-80, 234), (240, 480)]], np.int32)
    # print(polygon.shape)

    cv2.fillPoly(mask, pts=[polygon], color=(255,255,255))
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def getLaneCurve(frame):
    # TODO: use canny edge detector

    ### HSV color space

    points = LaneDetectionFunctions.valTrackbars()
    # print(type(points))
    masked_img = roi(frame, points)
    mask, m = LaneDetectionFunctions.tresholding(frame) # returns tresholded mask
    # cv2.imshow('mask', mask)
    edges = cv2.Canny(mask, 75, 150)
    h,w = edges.shape
    roi_image = roi(edges, points)
    # cv2.imshow('masked_image', roi_image) ### our goal image
    imgWarp = LaneDetectionFunctions.warpImage(edges, points, w, h)
    imgWarpPoints = LaneDetectionFunctions.drawPoints(edges, points)

    if debug_mode_HSV:
        hsv(frame)

    lined_img,image, params = LaneDetectionFunctions.hough(roi_image)
    direction, angle = calculate_steer(*params)
    print(direction, angle)
    # send_serial(angle=angle+80)
    cv2.imshow('image', image)
    # cv2.imshow('image warp points', imgWarpPoints)
    

    # h_stack = np.hstack([frame, mask,lined_img])
    # shapes = {
    #     'frame': frame.shape,
    #     'edges':edges.shape,
    #     'mask':mask.shape,
    #     'lined_image': lined_img.shape
    # }
    # cv2.imshow('frame, mask, lines on image', h_stack)
    cv2.imshow('edges', edges)
    cv2.imshow('final image', lined_img)

if __name__ == "__main__":
    # cap = cv2.VideoCapture(r'clips\race.mkv') # test video

    if debug_mode_roi:
        # create warp points trackbar
        LaneDetectionFunctions.warp_points_trackbar([0,0,0,480])
        pass

    if debug_mode_HSV:
        # create hsv_window_trackbar
        hsv_window_trackbar() 
        
    frameCounter = 0
    img = cv2.imread(r"clips\1.jpg" )

    # repeating the video
    while True:
        # frameCounter += 1
        # if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #     frameCounter = 0

        # success, img = cap.read()

        img = cv2.imread(r"clips\1.jpg" )
        
        img = cv2.resize(img, (240,480))


        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        getLaneCurve(img)

    cv2.waitKey(1)

    cv2.destroyAllWindows()
