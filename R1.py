import RPi.GPIO as GPIO
import time
from Sonic import UltraSonic

motorLFPin = 35 #----(ML)---- left fwd motor
motorRFPin = 37 #----(MR)---- right fwd motor
motorLRPin = 38 #----(ML)---- left rev motor
motorRRPin = 40 #----(MR)---- right rev motor
#ledPin = 11   #-----|LED>------
#sensorTrgPin = 18 # this is outpin _|-|_
#sensorEchoPin = 16  # this is input____|-----|____
PCT_DUTY_CYCLE = 0.5
FWD = 1  # move fwd
REV = 2  # move rev
LEFT = 3  # left
RIGHT = 4  # right
D_MIN = 15 # this is min distance in cms bot should  check
TURN_ANGLE = 10 # DEGREES  how to convert radians to linear?? pi * D 
TIME_OUT = 10

def setup():
    global distance, p_fwd, p_rev
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorLFPin, GPIO.OUT) # left motor fwd
    GPIO.setup(motorRFPin, GPIO.OUT) # Right motor fwd
    GPIO.setup(motorLRPin, GPIO.OUT) # left motor rev
    GPIO.setup(motorRRPin, GPIO.OUT) # right motor rev
    UltraSonic.setup()


def loop():
#    d = measureIt()
    
    distance = UltraSonic.getSonar()
    while True:
        #senseIt()  # can we split this into two sections 1) sensor 2) measurement?
          # need check for back side as well to avoid failure
#        distance = next(d)
        print("Distance from object is %d" %(distance))
        if (distance > D_MIN):
            distance = moveFwd(distance, 1)
            print("Distance from object is %d" %(distance))
            time.sleep(1)
        elif (distance<= D_MIN):
            stop()
            while True:
                time1 = time.time()
                print("Started clock %.3f" %(time1))
                safeR = checkDirection(RIGHT, TURN_ANGLE)
                safeL = safeR or checkDirection(LEFT, TURN_ANGLE)
                time2 = time1 + time,time()
                print("Cummulative Time : %.3f" %(time2))
                if (TIME_OUT>=time2):
                    print("We are stalled")
                    exit(1)
                if safeR or safeL:
                    break
                
        #takeCall()
            
        
#def measureIt():
#    # this will measure distance of an object and should return the distance d
#    for i in list(range(10, -1, -1)):
#        moveit(FWD, 1)
#        yield int(i)
    
def moveFwd(distance, steps):
    #if (distance -D_MIN <=0):
    #   return
    retval = distance - steps
    return retval
 
def stop():
    #destroy() # should stop the motors
    GPIO.output(motorLFPin, GPIO.LOW) # left motor fwd
    GPIO.output(motorRFPin, GPIO.LOW) # Right motor fwd
    GPIO.output(motorLRPin, GPIO.LOW) # left motor rev
    GPIO.output(motorRRPin, GPIO.LOW) # right motor rev
    #GPIO.output(ledPin, GPIO.LOW)
    
def checkDirection(dirextion, degrees):
    # make motor move right/left
#    safe = False
    ## measure distance between object and machine
    # turn motor 1 to right and motor 2 left by few degree??
    moveit(dirextion, degrees)
    d = UltraSonic.getSonar()
    if ( d > D_MIN):
        return True
    else:
        return False

def moveit(direction, degrees):
    if (direction== RIGHT):
        # motor should turn right
        GPIO.output(motorRFPin, GPIO.LOW)
        GPIO.output(motorRRPin, GPIO.HIGH)
        GPIO.output(motorLFPin, GPIO.HIGH)
        GPIO.output(motorLRPin, GPIO.LOW)
        time.sleep(1)
    elif (direction== LEFT):
        # motor should turn LEFT
        GPIO.output(motorRFPin, GPIO.HIGH)
        GPIO.output(motorRRPin, GPIO.LOW)
        GPIO.output(motorLFPin, GPIO.LOW)
        GPIO.output(motorLRPin, GPIO.HIGH)
        time.sleep(1)
    elif(direction== FWD):   # FWD    
        GPIO.output(motorRFPin, GPIO.HIGH)
        GPIO.output(motorRRPin, GPIO.LOW)
        GPIO.output(motorLFPin, GPIO.HIGH)
        GPIO.output(motorLRPin, GPIO.LOW)
        time.sleep(1)
    elif(direction== REV):   # REV    
        GPIO.output(motorRFPin, GPIO.LOW)
        GPIO.output(motorRRPin, GPIO.HIGH)
        GPIO.output(motorLFPin, GPIO.LOW)
        GPIO.output(motorLRPin, GPIO.HIGH)
        time.sleep(1)
 
def destroy():
    # pulling all outputs to low and cleaning it up
    GPIO.output(motorLFPin, GPIO.LOW) # left motor fwd
    GPIO.output(motorRFPin, GPIO.LOW) # Right motor fwd
    GPIO.output(motorLRPin, GPIO.LOW) # left motor rev
    GPIO.output(motorRRPin, GPIO.LOW) # right motor rev    

    UltraSonic.destroy()
    GPIO.cleanup()


if __name__=='__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

    
    