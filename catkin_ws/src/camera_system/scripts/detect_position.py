#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker
from time import time
import sys
import numpy as np

comm_pos = rospy.Publisher('comm_pos', String, queue_size=10)

turning = False
driving = False

timeout = None

def timeout_callback(event):
    timeout = None
    print "tag+stop"

def callback(data):
    for m in data.markers:
	if m.id == 5:
            if timeout != None:                                                                                               │-rw-rw-r--  1 laurens laurens   1494 Apr 25 10:18 output4
                timeout.shutdown()                                                                                            │drwxrwxr-x  2 laurens laurens  12288 Apr 25 10:17 OutputData
            timeout = rospy.Timer(rospy.Duration(0.1), timeout_callback, oneshot=True)

            posx = m.pose.pose.position.x
            posz = m.pose.pose.position.z
            deg  = (np.arctan2(posx, posz) * 180) / np.pi

            if not turning and (deg > 10 or deg < -10):
                turning = True
                print "tag+r"
            elif turning and (deg < 10 and  deg > -10):
                turning = False
                print "tag+stop"
            elif not driving and posz > 0.5:
                driving = True
                print "tag+d"
            elif driving and posz < 0.5:
                driving = False
                print "tag+stop"

	    print "\rTracking",
            print posx,
            print m.pose.pose.position.y,
            print posz,
            print deg,
            sys.stdout.flush()

def aruco_tag_tracking():
    rospy.init_node('detect_position', anonymous=True)
    rospy.Subscriber('/aruco_marker_publisher/markers', MarkerArray, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        aruco_tag_tracking()
    except rospy.ROSInterruptException:
        pass
