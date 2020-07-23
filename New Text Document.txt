import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from subprocess import call
import time
import os
import glob
import smtplib
import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
import subprocess
import sys

#MAIL
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, False)
gmail_user = "knightfoxlucifer@yahoo.com"
gmail_pwd = "1234567890@test"
FROM = 'knightfoxlucifer@yahoo.com'
TO = ['bhamrehrushikesh78@gmail.com'] #must be a list

time.sleep(1)
msg = MIMEMultipart()
time.sleep(1)
msg['Subject'] ="BIN Status :"
body = ": AYE GAADI WALA AYYA GHAR SE KAACHRA NIKAL "
msg.attach(MIMEText(body,'plain'))

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

def mail():
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587) #or port 465 doesn't seem to work!
    print "smtp.gmail"
    server.ehlo()
    print "ehlo"
    server.starttls()
    print "starttls"
    server.login(gmail_user, gmail_pwd)
    print "reading mail & password"
    server.sendmail(FROM, TO, msg.as_string())
    print "from"
    server.close()
    print 'successfully sent the mail'
    GPIO.output(22, True)
    time.sleep(2)
    GPIO.output(22, False)
    
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
                    mail()
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
                    time.sleep(3)
          
                    print ("backward")
                    for i in range(128):
                        backwardStep()
                    GPIO.output(11,GPIO.LOW) #buzzer
                    
    except:
        print "failed to send mail"
        GPIO.output(25, False)
        GPIO.cleanup()



