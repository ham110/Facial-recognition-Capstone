#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
#Modified by Christopher Booth
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO
from multiprocessing import Queue, Process, Lock
import time



## Tries to search the finger and calculate hash
def run(lock):##pass in the USER id fom the camera in later development 
    GPIO.setmode(GPIO.BCM)

    #TRIG=14
    UX=21
    #GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(UX,GPIO.OUT)


## Search for a finger
##

## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000) # initialize sensor attached to USB

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            GPIO.cleanup()
            lock.release()
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            #GPIO.output(TRIG, True)
            GPIO.output(UX, True)#open door
            time.sleep(5)#wait 5 sec
            #GPIO.output(TRIG, False)
            GPIO.output(UX, False)#close door
            GPIO.cleanup()
            lock.release()
            exit(0)
    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
        ##f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
        ##characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
        ##print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        lock.release()
        exit(1)
