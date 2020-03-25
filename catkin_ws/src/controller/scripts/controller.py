#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String

move_pub = rospy.Publisher('movement', String, queue_size=10)
sound_pub = rospy.Publisher('sound', String, queue_size=10)


def dance():
    print "Dance"

def return_home():
    print "Return home"


def foute_data(data):
    print "Foute data"
    print data

    
def movement(data):
    print data.data
    move_pub.publish("Recht vooruit")


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
    #Init of node
    rospy.init_node('central_switcher', anonymous=True)
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