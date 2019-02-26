import search
import time
import override
import enroll
from multiprocessing import Queue, Process, Lock
import SimpleMFRC522
import fileinput
import RPi.GPIO as GPIO
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import SimpleMFRC522



GPIO.setmode(GPIO.BCM)

#TRIG=14
UL = 26 #unlock pin
OV = 19 #override button pin
TR = 13#training button pin
#GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(UL,GPIO.IN)
GPIO.setup(OV,GPIO.IN)
GPIO.setup(TR,GPIO.IN)
#define and set up GPIO button input pins
lock=Lock()#create semaphore
mode = ''
while True:
    if lock.acquire(True, None): # blocking acquire lock 
        if GPIO.input(UL) == 1 and GPIO.input(OV) == 0 and GPIO.input(TR) == 0:
            time.sleep(0.1)
            if GPIO.input(UL) ==1 and GPIO.input(OV) == 0 and GPIO.input(TR) == 0:
                mode = 'unlock'#old text based mode definition from before button implementation
        elif GPIO.input(UL) == 0 and GPIO.input(OV) == 1 and GPIO.input(TR) == 0:
            time.sleep(0.1)
            if GPIO.input(UL) ==0 and GPIO.input(OV) == 1 and GPIO.input(TR) == 0:
                mode = 'override'
        elif GPIO.input(UL) == 0 and GPIO.input(OV) == 0 and GPIO.input(TR) == 1:
            time.sleep(0.1)
            if GPIO.input(UL) ==0 and GPIO.input(OV) == 0 and GPIO.input(TR) == 1:
                mode = 'train' 
        #mode = raw_input("Choose Mode(Unlock/Train/Override): ")
        #mode = mode.strip()
        #mode = mode.lower()
        lock.release() #releases lock to allow the start of the unlock/override/train processes
    if mode == 'unlock' and lock.acquire(False,None):#non-blocking lock acquires will no acquire the lock unless mode is matching
        Process(target=search.run, args=(lock,)).start()
        mode = ''
    if mode == 'override' and lock.acquire(False,None):#non-blocking
        Process(target=override.run, args=(lock,)).start()
        mode = ''
    if mode == 'train' and lock.acquire(False,None):
        Process(target=enroll.run, args=(lock,)).start()
        mode = ''
    
    


