#!/usr/bin/env python

import rospy
from std_msgs.msg import String
pub = rospy.Publisher('stop', String, queue_size=10)

def callback(data):
    distance = data.data
    rospy.loginfo(rospy.get_caller_id() + ' I heard %s', distance)
    if int(distance)<5: #distance in cm
        rospy.loginfo(rospy.get_caller_id() + ' stop signal has been sent')
        pub.publish('stop')
        

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/sonar_dist', String, callback)

    
    
    rospy.spin()
    

if __name__ == '__main__':
    listener()
