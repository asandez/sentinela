#!/usr/bin/env python
# Rangefinder ultrasonic distance sensor
# 13 min  62 max
#  Ros Node publish Topic "range"  std_msgs/Strings messages
#  rosrun sentina rangefinder.py
#




import LVEZ1v2
import rospy
from std_msgs.msg import String
distance =0

def filter(newdist):
    global distance
    if newdist > distance*1.2 or newdist < (distance-distance*.2):  
        tempdist = distance
        distance = newdist
        return tempdist
    
    return newdist

def range():
    GPIO = 18
  
    print "Iniciado rangefinder"
    pub = rospy.Publisher('range', String, queue_size=10)
    rospy.init_node('range', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        mm = LVEZ1v2.Measure(GPIO)
        sensor_str = "Distance: %s filtered: %s" % (mm, filter(mm))
        rospy.loginfo(sensor_str)
        #pub.publish(str(mm))
        rate.sleep()

if __name__ == '__main__':
    try:
        range()
    except rospy.ROSInterruptException:
        pass
