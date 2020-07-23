import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.IN)
a=13

#UltraSonic

GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 15
GPIO_ECHO = 16
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

#STEPPER

P_A1 = 29  # adapt to your wiring
P_A2 = 31 # ditto
P_B1 = 33 # ditto
P_B2 = 35 # ditto
delay = 0.005 # time to settle

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_A1, GPIO.OUT)
    GPIO.setup(P_A2, GPIO.OUT)
    GPIO.setup(P_B1, GPIO.OUT)
    GPIO.setup(P_B2, GPIO.OUT)

def forwardStep():
    setStepper(1, 0, 0, 0)
    setStepper(0, 1, 0, 0)
    setStepper(0, 0, 1, 0)
    setStepper(0, 0, 0, 1)

def backwardStep():
    setStepper(1, 0, 0, 0)
    setStepper(0 ,0, 0, 1)
    setStepper(0, 0, 1, 0)
    setStepper(0, 1, 0, 0)
    
def Stop():
    setStepper(1, 1, 1, 1)
    setStepper(1 ,1, 1, 1)
    setStepper(1, 1, 1, 1)
    setStepper(1, 1, 1, 1)
  
def setStepper(in1, in2, in3, in4):
    GPIO.output(P_A1, in1)
    GPIO.output(P_A2, in2)
    GPIO.output(P_B1, in3)
    GPIO.output(P_B2, in4)
    time.sleep(delay)
#print("Mr India")
    
setup()
if __name__ == '__main__':
    
    try:
        
        while True:
            
            while GPIO.input(a)==0:
                dist = distance()
                print (dist)
                while dist < 5.000 and GPIO.input(a)==0:
                    dist = distance()
                    client = mqtt.Client()
                    client.connect("localhost",1883,60)
                    client.publish("topic/test", "full")
                    for i in range(128):
                        Stop()
#                        dist = distance()
                        print(dist)
                        GPIO.output(11,GPIO.HIGH)
#                    if GPIO.input(a)==0:
#                        if dist > 5.000:
#                            GPIO.output(11,GPIO.LOW)
#                            break
#                else:
                    GPIO.output(11,GPIO.LOW)
                while dist > 5.000 and GPIO.input(a)==0:
                    
                    client = mqtt.Client()
                    client.connect("localhost",1883,60)
                    client.publish("topic/test", "nfull")                    
                    print ("Found")
                    print ("forward")
                    for i in range(128):
                        forwardStep()
                    time.sleep(1)
          
                    print ("backward")
                    for i in range(128):
                        backwardStep()
                    GPIO.output(11,GPIO.LOW) #buzzer
                    
    except:
        GPIO.cleanup()


