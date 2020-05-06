#!/usr/bin/env python

#this listener listens to the sensor that is pointed to the ground (not directly but with an angle, so the robot can stop in time).

import rospy
from std_msgs.msg import String
pub = rospy.Publisher('stop', String, queue_size=10)

def callback(data):
    distance = data.data
    rospy.loginfo(rospy.get_caller_id() + ' Listener2 heard %s', distance)
    if int(distance)>5: #distance in cm
        rospy.loginfo(rospy.get_caller_id() + ' stop signal has been sent')
        pub.publish('stop')
        

def listener():
    rospy.init_node('listener2', anonymous=True)
    rospy.Subscriber('/sonar_dist2', String, callback)

    
    
    rospy.spin()
    

if __name__ == '__main__':
    listener()
