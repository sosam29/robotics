import cv2
import numpy as np 

cap = cv2.VideoCapture(0)
_ , frame = cap.read()
# Convert BGR to HSV
if _ is True:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
else:
    # continue
    hsv = cv2.imread('/home/pi/examples/python/robotics/robotics/images/opencv_frame_2.png')
if hsv is None:
    print("No imaga found!! Check path")
    exit(-1)
cv2.imshow("Image", hsv)
cv2.waitKey(0)
hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

edges = cv2.Canny(hsv, 100, 200,  apertureSize=3)
if edges is None:
    print("No edges detected")
    exit(-1)
lines = cv2.HoughLines(edges, 1, np.pi/360, 100)
if lines is None:
    print("No lines detected")
    exit(-1)

for r, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = r * a
    y0 = r * b
    x1 = int(x0 + 1000*(-b)) 
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b)) 
    y2 = int(y0 - 1000*(a))

    cv2.line(hsv, (x1,y1), (x2, y2), (255, 0,0), 2)

cv2.imshow("Lined image", hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
