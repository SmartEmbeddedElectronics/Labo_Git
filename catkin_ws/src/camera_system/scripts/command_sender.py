#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker

comm_cam = rospy.Publisher('comm_cam', String, queue_size=10)
comm_v_s = rospy.Publisher('comm_voice_start', String, queue_size=10)

def callback(data):
    print(data.header)
    for m in data.Markers:
        print(m.id)

def aruco_tag_interpret():
    rospy.init_node('command_camera', anonymous=True)
    rospy.Subscriber('/aruco_marker_publisher/markers', MarkerArray, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        aruco_tag_interpret()
    except rospy.ROSInterruptException:
        pass
