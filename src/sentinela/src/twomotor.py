#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import LVEZ1v2


STEPPER_L_PINS = [6,13,19,26]
#STEPPER_L_PINS = [26,19,13,6]
STEPPER_R_PINS = [12,16,20,21]


STEPPER_SEQ = [[1,0,0,1],[1,0,0,0],
               [1,1,0,0],
               [0,1,0,0],
               [0,1,1,0],
               [0,0,1,0],
               [0,0,1,1],
               [0,0,0,1]]

def SetupMotor(pins):
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

def Setup():
  GPIO.setwarnings(False) 
  GPIO.setmode(GPIO.BCM)
  SetupMotor(STEPPER_R_PINS) 
  SetupMotor(STEPPER_L_PINS) 

def Step(step, pins): 
  for c in range(0, 4):
    GPIO.output(pins[c], STEPPER_SEQ[step][c]) 

Setup() 

while True:
    mm = LVEZ1v2.Measure(18)
    print("distance:",mm)
    for count in range (0, 1000):
      Step(count % 8, STEPPER_R_PINS)
      Step(count % 8, STEPPER_L_PINS)
      time.sleep(0.005)

