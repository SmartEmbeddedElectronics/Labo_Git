#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker

comm_cam = rospy.Publisher('comm_cam', String, queue_size=10)
comm_v_s = rospy.Publisher('comm_voice_start', String, queue_size=10)

def callback(data):
    for m in data.markers:
	if m.id == 1:
		comm_cam.publish("dance")
	elif m.id == 2:
		comm_cam.publish("home")
	elif m.id == 3:
		comm_cam.publish("play")
	elif m.id == 4:
		comm_v_s.publish("start")
	elif m.id > 100 and m.id < 200:
		distance = m.id - 100
		comm_cam.publish("move+" + str(distance))
	else:
		comm_cam.publish("error")
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
