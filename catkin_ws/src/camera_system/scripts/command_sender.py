#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray, Marker
from time import time

comm_cam = rospy.Publisher('comm_cam', String, queue_size=10)
comm_v_s = rospy.Publisher('comm_voice_start', String, queue_size=10)

prev_time = time()
prev_id = 0

def callback(data):
    global prev_id, prev_time
    now = time()
    for m in data.markers:
	if m.id == prev_id and now - prev_time < 10:
	    print("Too early")
	else:
	    prev_time = now
	    prev_id = m.id
            if m.id == 1:
	        comm_cam.publish("dance")
            elif m.id == 2:
                comm_cam.publish("home")
            elif m.id == 3:
	        comm_cam.publish("play")
            elif m.id == 4:
	        comm_v_s.publish("start")
            elif m.id == 5:
                comm_cam.publish("follow")
	    elif m.id > 100 and m.id < 200:
	        distance = m.id - 100
	        comm_cam.publish("move+" + str(distance))
	    else:
	        comm_cam.publish("error")
        print(now, m.id)

def aruco_tag_interpret():
    print "\033[2JDetect a tag and send its action"
    rospy.init_node('command_camera', anonymous=True)
    rospy.Subscriber('/aruco_marker_publisher/markers', MarkerArray, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        aruco_tag_interpret()
    except rospy.ROSInterruptException:
        pass
