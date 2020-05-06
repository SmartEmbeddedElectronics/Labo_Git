#!/usr/bin/env python
import rospy
import sys
import threading
import time
import speech_recognition as sr
from std_msgs.msg import Float64

period = None
start = None
i = 0
def flash():
    global period, i
    end = time.time()
    if (end - start) > 27:
        return
    if i%2 == 0:
        sys.stdout.write("\r***LED flash***")
    else:
        sys.stdout.write("\r               ")
    sys.stdout.flush()
    i += 1
    threading.Timer(period, flash).start()

def callback(data):
    global freq, period, start
    rospy.loginfo("bpm data received: " + str(data))
    bpm = data.data
    freq = bpm*2/60
    period = 1.0 / freq
    start = time.time()
    flash()

def listener():
    global freq
    rospy.init_node('Led_controller', anonymous=True)
    rospy.Subscriber("comm_bpm", Float64, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.logdebug("Module running")
        listener()
    except rospy.ROSInterruptException:
        pass