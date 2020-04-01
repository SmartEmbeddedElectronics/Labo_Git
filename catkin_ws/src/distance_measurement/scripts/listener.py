#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    distance = data.data
    rospy.loginfo(rospy.get_caller_id() + ' I heard %s', distance)
    if distance<5: #distance in cm
        rospy.loginfo(rospy.get_caller_id() + 'STOP signal has been sent')
        pub.publish('STOP')
        

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/sonar_dist', String, callback)
    pub = rospy.Publisher('/comm_distance', String, queue_size=10)
    
    
    rospy.spin()
    

if __name__ == '__main__':
    listener()
