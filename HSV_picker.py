import cv2
import numpy as np
import json


def hsv_window_trackbar():
    cv2.namedWindow("HSV")
    cv2.resizeWindow('HSV',640,240)
    cv2.createTrackbar("HUE min", "HSV",0, 179, lambda x:None)
    cv2.createTrackbar("HUE max", "HSV", 179, 179, lambda x:None)
    cv2.createTrackbar("SAT min", "HSV", 0, 255, lambda x:None)
    cv2.createTrackbar("SAT max", "HSV",255, 255, lambda x:None)
    cv2.createTrackbar("VALUE min", "HSV",0, 255, lambda x:None)
    cv2.createTrackbar("VALUE max", "HSV",255, 255, lambda x:None)


def hsv(raw_frame):
    img = cv2.resize(raw_frame,(240,480))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE min", "HSV")
    h_max = cv2.getTrackbarPos("HUE max", "HSV")

    s_min = cv2.getTrackbarPos("SAT min", "HSV")
    s_max = cv2.getTrackbarPos("SAT max", "HSV")

    v_min = cv2.getTrackbarPos("VALUE min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE max", "HSV")
    values = {
        'h_min':h_min,
        'h_max':h_max,
        "s_min":s_min,
        "s_max":s_max,
        "v_min":v_min,
        "v_max":v_max
            }
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img,img,mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    h_stack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', h_stack)

    print(values)

