import RPi.GPIO as GPIO
import time
import datetime
from dateutil import relativedelta
from ultra_sonic import setup as ultrasetup
from ultra_sonic import destroy as ultradestroy
from ultra_sonic import getSonar
from ultra_sonic import pulseIn

motorLFPin = 35 #----(ML)---- left fwd motor
motorRFPin = 37 #----(MR)---- right fwd motor
motorLRPin = 38 #----(ML)---- left rev motor
motorRRPin = 40 #----(MR)---- right rev motor

PCT_DUTY_CYCLE = 0.5
FWD = 1  # move fwd
REV = 2  # move rev
LEFT = 3  # left
RIGHT = 4  # right
D_MIN = 15 # this is min distance in cms bot should  check
TURN_ANGLE = 30 # DEGREES  how to convert radians to linear?? pi * D 
TIME_OUT = 2  # in minutes

def setup():
    # global distance, p_fwd, p_rev
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorLFPin, GPIO.OUT) # left motor fwd
    GPIO.setup(motorRFPin, GPIO.OUT) # Right motor fwd
    GPIO.setup(motorLRPin, GPIO.OUT) # left motor rev
    GPIO.setup(motorRRPin, GPIO.OUT) # right motor rev
    ultrasetup()


def loop():
#    d = measureIt()
    
    distance = getSonar()
    while True:
        #senseIt()  # can we split this into two sections 1) sensor 2) measurement?
          # need check for back side as well to avoid failure
#        distance = next(d)
        print("Distance from object is %d" %(distance))
        if (distance > D_MIN):
            distance = getSonar()
            print("Distance from object is %d" %(distance))
            time.sleep(1)
        elif (distance<= D_MIN):
            stop()
            cum_min = 0
            while True:
                time1 = datetime.datetime.now()
#                print("Started clock %.3f" %(time1))
                safeR = checkDirection(RIGHT, TURN_ANGLE)
                
                safeL = safeR or checkDirection(LEFT, TURN_ANGLE)
                print("LEFT : %s RIGHT: %s"%(safeR, safeL))
                time2 = time1 = datetime.datetime.now()
                diff = relativedelta.relativedelta(time2, time1)
                cum_min += diff.minutes
#                print("Time in Minutes : %.3f" %(timeinmin))
                if (TIME_OUT>=cum_min):
                    print("We are stalled")
                    destroy()
                    ultradestroy()
                    exit(1)
                if safeR or safeL:
                    print("Breaking Direction Check and resuming the travel")
                    break

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
    d = getSonar()
    print("Direction : %s Turning : %d Degrees" %(dirextion, degrees))
    if ( d > D_MIN):
        return True
    else:
        return False

def moveit(direction, degrees):
    print("motor should turn to direction %s by %d degrees"%(direction, degrees))
    if (direction== RIGHT):
#        pring("motor should turn right")
        GPIO.output(motorRFPin, GPIO.LOW)
        GPIO.output(motorRRPin, GPIO.HIGH)
        GPIO.output(motorLFPin, GPIO.HIGH)
        GPIO.output(motorLRPin, GPIO.LOW)        
        time.sleep(1)
    elif (direction== LEFT):
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
#     distance = getSonar()
     
def destroy():
    # pulling all outputs to low and cleaning it up
    GPIO.output(motorLFPin, GPIO.LOW) # left motor fwd
    GPIO.output(motorRFPin, GPIO.LOW) # Right motor fwd
    GPIO.output(motorLRPin, GPIO.LOW) # left motor rev
    GPIO.output(motorRRPin, GPIO.LOW) # right motor rev    

    ultradestroy()
    GPIO.cleanup()


if __name__=='__main__':
    setup()
    ultrasetup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

    
    