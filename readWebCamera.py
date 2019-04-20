import cv2 as cv
import numpy as np 
import RPi.GPIO as GPIO
import time

echoPin = 18
triggerPin = 16
MAX_DIST = 500 # cm
TIME_OUT_PEEK= MAX_DIST * 60 # 220 * 60 = 13200 microseconds

GPIO.setmode(GPIO.BOARD)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)


def pulseIn(pin, level, TO):
    t0 = time.time()
    while (GPIO.input(pin) != level):
        if((time.time() - t0) > TO *0.000001):
            return 0

    t0=time.time()
    
    while (GPIO.input(pin)==level):
        if((time.time()- t0) > TO * 0.000001):
            return 0
    pulsetime = (time.time()- t0) * 1000000
    return pulsetime

def getDistance():
#    print("Probing")
    distances =[]
    for _ in range(0,50):
        GPIO.output(triggerPin, GPIO.HIGH)
        time.sleep(.00001) # 10 microsec
        GPIO.output(triggerPin, GPIO.LOW)
        pingTime = pulseIn(echoPin, GPIO.HIGH, TIME_OUT_PEEK)
        d1 = pingTime * 340.0/2.0/10000.0 # sound speed 340 m/s
        distances.append(d1)
        time.sleep(0.001)
#        print("current Iteration %d"%(i))
            
    distance = sum(distances)/len(distances)   

    return distance


def destroy():
    print("cleaning things up")
    GPIO.cleanup()

capture = cv.VideoCapture(0)
capture2 = cv.VideoCapture(1)
while True:
    d = getDistance()
    print("Distance is %.2f cm"%(d))
    ret, frame = capture.read()
    ret1, frame1 = capture2.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("grayed" , gray)
    cv.imshow("color",frame1)
    c = cv.waitKey(0)
    if 'q'==chr (c & 255):
        destroy()
        break

capture.release()
cv.destroyAllWindows()