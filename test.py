import numpy as np
import cv2
p = np.poly1d([1,2,3])
x = np.polyfit(x=[1,2,3], y=[1,2,3], deg=1)
p1 = np.poly1d(x)


image = cv2.imread(filename=r'clips\road.jpg')
print(image)
print(f'image shape: {image.shape}')
cv2.imshow('main image', image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

image = cv2.Canny(image, 2,200)

# edges = cv2.Canny(mask, 75, 150)


def detect_lines(image):
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 10, np.array([]), minLineLength=20, maxLineGap=100)
    return lines


def best_line(frame, lines):
    image = np.zeros_like(frame)

    try:
        x_left_line = []
        y_left_line = []
        x_right_line = []
        y_right_line = []

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
        min_y = int(image.shape[0]*(3/5))
        max_y = int(image.shape[0])

        left_line_equation = np.poly1d(np.polyfit(x=y_left_line, y=x_left_line, deg=1))
        right_line_equation = np.poly1d(np.polyfit(x=y_right_line, y=x_right_line, deg=1))

        x1_left = int(left_line_equation(max_y))
        x2_left = int(left_line_equation(min_y))
        x1_right = int(right_line_equation(max_y))
        x2_right = int(right_line_equation(min_y))
        right_slope = (max_y - min_y) / (x2_right-x1_right)
        left_slope = (max_y - min_y) / (x2_left-x1_left)
        
        print(f"left_slope: {left_slope}")
        print(f"right_slope: {right_slope}")
        cv2.line(frame, (x1_left, max_y), (x2_left, min_y), (255,0,0), 5 )
        cv2.line(frame, (x1_right, max_y), (x2_right, min_y), (255,0,0),5)
    except:
        print('error')
        raise
    return image

lines = detect_lines(image)
i = best_line(image, lines)

cv2.imshow('i', i)
cv2.imshow('iii', image)
cv2.circle(image, center=(5,100),radius=3,color=(255,0,0), thickness=4 )
cv2.imshow('i', image)



cv2.waitKey(0)


