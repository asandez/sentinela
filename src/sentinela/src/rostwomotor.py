#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

#STEPPER_L_PINS = [26,19,13,6]
STEPPER_L_PINS = [26,13,19,6]
#STEPPER_R_PINS = [12,16,20,21]
STEPPER_R_PINS = [21,16,20,12]



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

# dire 1 forward, -1 reverse
def Step(step, pins, dire):
  
  if dire == 1:
    print "forw"
    for c in range(0, 4):
      GPIO.output(pins[c], STEPPER_SEQ[step][c])
  else:
    print "rev"
    for c in range(0, 4):
      GPIO.output(pins[3-c], STEPPER_SEQ[step][c])

def rostwomotor():

  Setup()
  # In ROS, nodes are uniquely named. If two nodes with the same
  # name are launched, the previous one is kicked off. The
  # anonymous=True flag means that rospy will choose a unique
  # name for our 'listener' node so that multiple listeners can
  # run simultaneously.
  rospy.init_node('rostwomotor', anonymous=True)

  rospy.Subscriber('navegacion', String, callback)
  print "entro en rostwomotor"
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()


def callback (data):

  for count in range (0, 500):
    Step(count % 8, STEPPER_R_PINS,1)
    Step(count % 8, STEPPER_L_PINS,-1)
    time.sleep(0.0009)

if __name__ == '__main__':
    rostwomotor()


