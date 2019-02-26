import RPi.GPIO as GPIO
from multiprocessing import Queue, Process, Lock
import time
import SimpleMFRC522
import userlist

def run(lock):
    GPIO.setmode(GPIO.BCM)
    #TRIG=14
    UX=21
    #GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(UX,GPIO.OUT)
    reader = SimpleMFRC522.SimpleMFRC522() # unMFRC library for override operations

    try:
            id, text = reader.read() # reads the RFID and any stored data on the key fob
            text = text.rstrip()
            
            print(id)
            print(text)
    except:
            print('nokeyerror')
    if userlist.returnuser(id,text): #Checks the list of Keyfobs to see if the scanned one is valid
        GPIO.output(UX, True) #open lock
        time.sleep(5)#wait 5 seconds Blocking but in a seperate process from the controller
        print('door opened')
        #GPIO.output(TRIG, False)
        GPIO.output(UX, False)#close door
        
        GPIO.cleanup()
        lock.release()
        exit(0)
    else:
        GPIO.cleanup()
        lock.release()
        exit(0)
        
def train(lock):
    reader = SimpleMFRC522.SimpleMFRC522()

    try:
        id, text = reader.read()
        print(id)
        print(text)
        text = text.rstrip() 
        userlist.adduser(id,text)#add scanned fob to user file
    finally:
        GPIO.cleanup()
        lock.release()
        exit(0)