import RPi.GPIO as GPIO 
import time

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT) # motor front 1 fwd (H/L in tandem with  pin38)
    GPIO.setup(38, GPIO.OUT) # motor front 1 fwd
    GPIO.setup(36, GPIO.OUT)  # motor front 2 fwd (H/L in tandem with  pin32)
    GPIO.setup(32, GPIO.OUT) # motor front 2 fwd
    
    GPIO.setup(37, GPIO.OUT) # motor rear 1 fwd (H/L in tandem with  pin38)
    GPIO.setup(35, GPIO.OUT) # motor rear 1 fwd
    GPIO.setup(33, GPIO.OUT)  # motor rear 2 fwd (H/L in tandem with  pin32)
    GPIO.setup(31, GPIO.OUT) # motor rear  2 fwd

def loop():
    print("Intitial command fwd motor 1 & motor 2 ")
    while True:
# front set of motors        
        print("start  motors  in Fwd direction ..>>>")
        GPIO.output(40, GPIO.HIGH) # motor 2
        GPIO.output(38, GPIO.LOW)
        GPIO.output(36, GPIO.HIGH) # motor 2
        GPIO.output(32, GPIO.LOW)
# rear set of motors
        GPIO.output(37, GPIO.HIGH) # motor 2
        GPIO.output(35, GPIO.LOW)
        GPIO.output(33, GPIO.HIGH) # motor 2
        GPIO.output(31, GPIO.LOW)

        time.sleep(2)
        print("Stopping motors... ")
        pullDownAllMotors()
        time.sleep(.1)

def destroy():
    GPIO.cleanup()


def pullDownAllMotors():
    GPIO.output(40, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(32, GPIO.LOW)

    # rear set of motor set
    GPIO.output(37, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopping ....")
        pullDownAllMotors()
    finally:
        destroy()

    