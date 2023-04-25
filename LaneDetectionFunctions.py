import cv2
import numpy as np

# {'h_min': 33, 'h_max': 179, 's_min': 0, 's_max': 255, 'v_min': 210, 'v_max': 255}
# {'h_min': 0, 'h_max': 58, 's_min': 0, 's_max': 255, 'v_min': 133, 'v_max': 255}
# {'h_min': 0, 'h_max': 179, 's_min': 0, 's_max': 255, 'v_min': 29, 'v_max': 255}
# {'h_min': 25, 'h_max': 88, 's_min': 0, 's_max': 255, 'v_min': 201, 'v_max': 255}
# {'h_min': 21, 'h_max': 179, 's_min': 0, 's_max': 255, 'v_min': 219, 'v_max': 255}
def tresholding(img, h_min=27,s_min=0,v_min=246, h_max=179,s_max=255,v_max=255):
    # img -> hsv space

    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([21,0,219])
    upperWhite = np.array([179,255,255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    masked_img = cv2.bitwise_and(img,img,mask=maskWhite)
    mask = cv2.cvtColor(maskWhite, cv2.COLOR_GRAY2BGR)
    return mask, masked_img


def warp_points_trackbar(initialTrackbarVals, wT=240,hT=480):
    cv2.namedWindow('Warp Image Trackbar')
    cv2.resizeWindow('Warp Image Trackbar',360,240)
    cv2.createTrackbar('Width Top', 'Warp Image Trackbar',initialTrackbarVals[0], wT, lambda x: None)
    cv2.createTrackbar('Height Top', 'Warp Image Trackbar',initialTrackbarVals[1], hT, lambda x: None)
    cv2.createTrackbar('Width Bottom', 'Warp Image Trackbar',initialTrackbarVals[2], wT, lambda x: None)
    cv2.createTrackbar('Height Bottom', 'Warp Image Trackbar',initialTrackbarVals[3], hT, lambda x: None)

def valTrackbars(wT=240, hT=480):
    widthTop = cv2.getTrackbarPos('Width Top', 'Warp Image Trackbar')
    heightTop = cv2.getTrackbarPos('Height Top', 'Warp Image Trackbar')
    widthBottom = cv2.getTrackbarPos('Width Bottom', 'Warp Image Trackbar')
    heightBottom = cv2.getTrackbarPos('Height Bottom', 'Warp Image Trackbar')
    # np.float32
    points = np.int32([(widthTop, heightTop), (wT-widthTop, heightTop),
                (widthBottom, heightBottom), (wT-widthBottom, heightBottom)])

    return points


def drawPoints(img,points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]),int(points[x][1])),15,(255,255,255),cv2.FILLED)
    return img

def warpImage(img, points, w, h):
    
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w, 0], [0,h], [w,h]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))

    return imgWarp


### TODO: Create a Region of Interest


def hough(edges):
    # lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=100, )
    # lines = cv2.HoughLinesP(image, rho, angle, min_threshold, np.array([]), minLineLength=20,
    #                                 maxLineGap=4)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=100)
    image = np.zeros_like(edges)
    height, width = edges.shape
    min_y = 234
    max_y = 480
    try:
        x_mean_frame, x_mean_bott, x_mean_top = 0,0,0 # inisialize them

        x_left_line = []
        y_left_line = []
        x_right_line = []
        y_right_line = []
        if lines is not None:
            for line in lines:
            
                x1, y1, x2, y2 = line[0]

                cv2.line(image, (x1, y1), (x2, y2), (255,255,255),5)


                #### calculating the slope:
                slope = (y2-y1) / (x2-x1)
                if abs(slope) < 0.5:
                    continue
                elif slope <=0:
                    x_left_line.extend([x1, x2])
                    y_left_line.extend([y1, y2])
                else:
                    x_right_line.extend([x1, x2])
                    y_right_line.extend([y1, y2])


        ### considering the frame dimensions
            min_y = 234
            max_y = 480
        try:
            left_line_equation = np.poly1d(np.polyfit(x=y_left_line, y=x_left_line, deg=1))
            right_line_equation = np.poly1d(np.polyfit(x=y_right_line, y=x_right_line, deg=1))
            x1_left = int(left_line_equation(max_y))
            x2_left = int(left_line_equation(min_y))
            x1_right = int(right_line_equation(max_y))
            x2_right = int(right_line_equation(min_y))
            right_slope = (max_y - min_y) / (x2_right-x1_right)
            left_slope = (max_y - min_y) / (x2_left-x1_left)

            x_mean_bott = (x1_left + x1_right) // 2
            x_mean_top = (x2_left + x2_right) // 2

            x_mean_frame = edges.shape[1] // 2

            # cv2.putText(edges, f'x_mean_frame - x_mean_top= {x_mean_frame-x_mean_top}',
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,255,255), thickness=3 )
            cv2.circle(edges, center=(x_mean_frame,max_y), radius=10, color=(255,255,255), thickness=5)

            cv2.circle(edges, center=(x_mean_bott,max_y), radius=10, color=(255,255,255), thickness=3)
            cv2.circle(edges, center=(x_mean_top,min_y), radius=10, color=(255,255,255), thickness=5)
            
            # print(f"left_slope: {left_slope}")
            # print(f"right_slope: {right_slope}")
            cv2.line(edges, (x1_left, max_y), (x2_left, min_y), (255,255,255), 5 )
            cv2.line(edges, (x1_right, max_y), (x2_right, min_y), (255,255,255),5)
            cv2.putText(edges, f'x_mean_top - x_mean_bott= {x_mean_top-x_mean_bott}',
                         (2,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
        except:
            # print('what??')
            # raise
            pass
    except:
        # print('error')
        # raise
        pass
    return edges,image,  [x_mean_frame, x_mean_bott, x_mean_top, min_y, max_y]
    

