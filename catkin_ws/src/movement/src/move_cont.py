#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time

PI = 3.1415926535897
right = 90*2*PI/360
left = -90*2*PI/360
a_speed = 0.2

pub = rospy.Publisher('movement', String, queue_size=10)
velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)


def move_control():
	rospy.init_node('move_control', anonymous=True)
	rospy.Subscriber('mov_cont', String, callback)
    	# spin() simply keeps python from exiting until this node is stopped
    	rospy.spin()

def callback(data):
	# Starts a new node
	print("callback")
	txt = data.data
	rospy.loginfo(txt)
	#pub.publish(txt)
	if(txt == 'start'):
		pub.publish("start")
	else:
		x = txt.split("+")
		if(x[0] == "r"): #rotate
			print("rotate")
			angle = int(x[1])
			angle_rad = angle*2*PI/360
			if(angle > 0):
				msg = "r+0.7"
				pub.publish(msg)
			else:
				msg = "r+-0.7"
				pub.publish(msg)
			current_angle = 0
			t0 = rospy.get_time()
			while(current_angle <= abs(angle_rad)):
				t1 = rospy.Time.now().to_sec()
				current_angle = 0.7*(t1-t0)
			pub.publish("stop")
			time.sleep(2)
			
		elif(x[0] == "d"): #drive
			print("drive")
			dist = int(x[1])
			if(dist > 0):
				msg = "d+0.1"
				pub.publish(msg)
			else:
				msg = "d+-0.1"
				pub.publish(msg)
			current_dist = 0
			t0 = rospy.get_time()
			while(current_dist <= abs(dist)):
				t1 = rospy.Time.now().to_sec()
				current_dist = 0.1*(t1-t0)
			pub.publish("stop")
			time.sleep(2)
	
				
	

if __name__ == '__main__':
    try:
        move_control()
    except rospy.ROSInterruptException:
        pass
