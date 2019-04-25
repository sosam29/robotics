import cv2
import time

capture = cv2.VideoCapture(1)
for i in range(0,3):
    ret, frame = capture.read()
    print("Take picture")
    # cv2.waitKey(0)
    cv2.imshow("Img"+str(i), frame)
    cv2.imwrite(str(i)+".jpg", frame)
    print("Change position..")  
    time.sleep(5)

print("Exiting!!!")
cv2.waitKey(0)
capture.release()
cv2.destroyAllWindows()