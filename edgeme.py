import cv2
import numpy as np 

img = cv2.imread('/home/pi/examples/python/robotics/robotics/2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 100, 200,  apertureSize=3)
if edges is None:
    print("No edges detected")
    exit(-1)
lines = cv2.HoughLines(edges, 1, np.pi/360, 200)
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

    cv2.line(img, (x1,y1), (x2, y2), (255, 0,0), 2)

cv2.imshow("Lined image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
