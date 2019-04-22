import cv2 
import time

try:
    while True:
        cap1 = cv2.VideoCapture(0)
        if not (cap1.isOpened()):
            print("not accessible")
            exit(-1)
                
        # cap2 = cv2.VideoCapture(1)
        ret, framel = cap1.read()
        # _, framer = cap2.read()

        cv2.imshow("Left", framel )
        # cv2.imshow("Right", framer)
        time.sleep(1)
except KeyboardInterrupt:
    cap1.release()
    # cap2.release()
    cv2.destroyAllWindows()