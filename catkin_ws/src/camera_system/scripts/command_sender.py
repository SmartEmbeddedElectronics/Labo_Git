#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

comm1 = rospy.Publisher('comm1', String, queue_size=10)
comm2 = rospy.Publisher('comm2', String, queue_size=10)

def callback(data):
    if data.data == "C1":
        comm1.publish("C1 Received")
    elif data.data == "C2":
        comm2.publish("C2 Received")

def command_sender():
    rospy.init_node('command_sender', anonymous=True)
    rospy.Subscriber('commands', String, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        command_sender()
    except rospy.ROSInterruptException:
        pass
