#!/usr/bin/env python
import smbus
#import math
import rospy
import time
from std_msgs.msg import String

# Register

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1


# MAG3110 address, 0x0E(14)
# Read data back from 0x01(1), 6 bytes
# X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
data = bus.read_i2c_block_data(0x0E, 0x01, 6)
 
def get_gyro():
    # MAG3110 address, 0x0E(14)
    # Read data back from 0x01(1), 6 bytes
    # X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)

    # Convert the data
    xMag = data[0] * 256 + data[1]
    if xMag > 32767 :
            xMag -= 65536

    yMag = data[2] * 256 + data[3]
    if yMag > 32767 :
            yMag -= 65536

    zMag = data[4] * 256 + data[5]
    if zMag > 32767 :
            zMag -= 65536

    # Output data to screen
    print "Magnetic field in X-Axis : %d" %xMag
    print "Magnetic field in Y-Axis : %d" %yMag
    print "Magnetic field in Z-Axis : %d" %zMag
         
    return yMag 
   
def talker():
    # MAG3110 address, 0x0E(14)
    # Select Control register, 0x10(16)
    #		0x01(01)	Normal mode operation, Active mode

    bus.write_byte_data(0x0E, 0x10, 0x01)

    time.sleep(0.5)
   
    print "Iniciado Gyroscope"
    pub = rospy.Publisher('gyrox', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        mm = get_gyro()
        sensor_str = "X rotation: %s time: %s" % (mm,rospy.get_time())
        #print "xxxxx"
        rospy.loginfo(sensor_str)
        pub.publish(str(mm))
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
