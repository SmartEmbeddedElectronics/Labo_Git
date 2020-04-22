#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker
from time import time
import sys

comm_pos = rospy.Publisher('comm_pos', String, queue_size=10)

def callback(data):
    for m in data.markers:
	if m.id == 5:
	    print "\rTracking",
            print m.pose.pose.position.x,
            print m.pose.pose.position.y,
            print m.pose.pose.position.z,
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
