#!/usr/bin/env python
import rospy
import sys
import speech_recognition as sr
from std_msgs.msg import Float64

freq = 0.01
def callback(data):
    global freq
    rospy.loginfo("bpm data received: " + str(data))
    bpm = data.data
    freq = bpm*2/60

def listener():
    global freq
    rospy.init_node('Led_controller', anonymous=True)
    rospy.Subscriber("comm_bpm", Float64, callback)
    """ Code for flashing leds on correct frequency goes here """
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.logdebug("Module running")
        listener()
    except rospy.ROSInterruptException:
        pass