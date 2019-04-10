import RPi.GPIO as GPIO
import time

echoPin = 18
trigerPin = 16
MAX_DIST = 500 # cm
TIME_OUT_PEEK= MAX_DIST * 60 # 220 * 60 = 13200 microseconds


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

def getSonar():
#    print("Probing")
    distances =[]
    for i in range(0,100):
        GPIO.output(trigerPin, GPIO.HIGH)
        time.sleep(.00001) # 10 microsec
        GPIO.output(trigerPin, GPIO.LOW)
        pingTime = pulseIn(echoPin, GPIO.HIGH, TIME_OUT_PEEK)
        d1 = pingTime * 340.0/2.0/10000.0 # sound speed 340 m/s
        distances.append(d1)
        time.sleep(0.001)
#        print("current Iteration %d"%(i))
            
    distance = sum(distances)/len(distances)   

    return distance
            
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigerPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    
    
def loop():
#    GPIO.setup(11,GPIO.IN)
    while True:
        distances =[]
        for j in range(0,100):
            d1 = getSonar()
            distances.append(d1)
#            print("current Iteration %d"%(j))
            time.sleep(0.001)
        distance = sum(distances)/len(distances)   
#        cummulative = sum(distances)
#        
#        distance = cummulative/len(distances)
        
        print("Distance is %.2f cm"%(distance))
        time.sleep(1)

def destroy():
    GPIO.cleanup()
#    GPIO.output(trigerPin, GPIO.LOW)
    print("In destroy() cleaning up")
    

#    if __name__ =="__main__":
#        setup()
#        try:
#            loop()
#        except KeyboardInterrupt:
#            destroy()
#        
