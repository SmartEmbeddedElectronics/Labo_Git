#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker
from time import time
import sys
import numpy as np

comm_pos = rospy.Publisher('comm_pos', String, queue_size=10)

def callback(data):
    for m in data.markers:
	if m.id == 5:
            posx = m.pose.pose.position.x
            posz = m.pose.pose.position.z

	    print "\rTracking",
            print posx,
            print m.pose.pose.position.y,
            print posz,
            deg  = (np.arctan2(posz, posx) * 180) / np.pi
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
