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
    global timeout, turning, driving
    if turning or driving:
        turning = False
        driving = False
        comm_pos.publish("tag+stop")
    timeout = None

def callback(data):
    global timeout, turning, driving
    for m in data.markers:
	if m.id == 5:
            if timeout is not None:
                timeout.shutdown()
            timeout = rospy.Timer(rospy.Duration(1), timeout_callback, oneshot=True)

            posx = m.pose.pose.position.x
            posz = m.pose.pose.position.z
            deg  = (np.arctan2(posx, posz) * 180) / np.pi

            if not turning and (deg > 10 or deg < -10):
                turning = True
                comm_pos.publish("tag+r")
            elif turning and (deg < 10 and  deg > -10):
                turning = False
                comm_pos.publish("tag+stop")
            elif not driving and posz > 0.5:
                driving = True
                comm_pos.publish("tag+d")
            elif driving and posz < 0.5:
                driving = False
                comm_pos.publish("tag+stop")

	    print "\rTracking",
            print "%.2f" % posx,
            print "%.2f" % m.pose.pose.position.y,
            print "%.2f" % posz,
            print "%.2f" % deg,
            sys.stdout.flush()

def aruco_tag_tracking():
    print "\033[2JDetect Position of tag"
    rospy.init_node('detect_position', anonymous=True)
    rospy.Subscriber('/aruco_marker_publisher/markers', MarkerArray, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        aruco_tag_tracking()
    except rospy.ROSInterruptException:
        pass
