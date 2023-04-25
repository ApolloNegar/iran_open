import cv2
import numpy as np

# cap = cv2.VideoCapture('vid1.mp4') # test video

def hough(frame):

    img = cv2.resize(frame,(480,240))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print(img.shape)

    edges = cv2.Canny(gray, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,50, maxLineGap=500)
    print(lines)

    # print these lines
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0),3)
    cv2.imshow('ed',edges)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
    
