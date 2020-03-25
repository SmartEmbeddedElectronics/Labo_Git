#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String

Command_camera = rospy.Publisher('Command_camera', String, queue_size=10)
Move_controller = rospy.Publisher('Move_controller', String, queue_size=10)


def dance():
    print "Dance"

def return_home():
    print "Return home"


def foute_data(data):
    print "Foute data"
    print data

    
def movement(data):
    print data.data
    Move_controller.publish("Recht vooruit")


def aruco(data):
    print data.data
    #Determine command
    if (data.data=="dance"):
        dance()
    elif (data.data=="home"):
        return_home()
    else:
        foute_data("Aruco")



def voice(data):
    print data.data


def distance(data):
    print data.data

def central_switcher():
    #Init of all nodes (publisher and subscriber)
    rospy.init_node('comm_cam_node', anonymous=True)
    rospy.init_node('movement_node', anonymous=True)
    rospy.init_node('comm_voice_node', anonymous=True)
    rospy.init_node('comm_distance_node', anonymous=True)
    rospy.init_node('sound_node', anonymous=True)
    #Subscribe on the aruco, distance and voice toppic
    rospy.Subscriber('comm_cam', String, aruco)
    rospy.Subscriber('comm_voice', String, voice)
    rospy.Subscriber('comm_distance', String, distance)
    #Keep hanging until one of the three gives a responce
    rospy.spin()


if __name__ == '__main__':
    try:
        central_switcher()
    except rospy.ROSInterruptException:
        print "Error in main"
        pass