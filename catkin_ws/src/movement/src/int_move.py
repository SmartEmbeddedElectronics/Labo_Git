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
velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
vel_msg = Twist()

PI = 3.1415926535897
right = -10*2*PI/360
left = 10*2*PI/360
stop_cont = 0 #0 = stop/1 = start
msg = ""
def stop_callback(data):
	global stop_cont
	rospy.loginfo(rospy.get_caller_id() + ' stop callback %s', data.data)
	if(data.data == 'stop'):
		print('STOPPERDEPOP')
		stop_cont = 0
		vel_msg.angular.z = 0
		vel_msg.linear.x = 0
		velocity_publisher.publish(vel_msg)
	else:
		print('not stop')
def callback(data):
	global msg
	global stop_cont
	rospy.loginfo(rospy.get_caller_id() + 'callback %s', data.data)
	if(data.data == 'start'):
		print('start')
		stop_cont = 1
	else:
		print('not start')
		msg = data.data
		move()
	




	
def move():
	global msg
	if(stop_cont == 1):#start
		print("move")
		print(msg)
		if(msg == "stop"):
			print("stop")
			vel_msg.angular.z = 0
			vel_msg.linear.x = 0
			velocity_publisher.publish(vel_msg)
		else:
			x = msg.split("+")
			print('test')
			print(x[0])
			if(x[0] == "r"): #rotate
				print("rotate")
				vel_msg.angular.z = float(x[1])
				vel_msg.linear.x = 0
				velocity_publisher.publish(vel_msg)
			elif(x[0] == "d"):#drive	
				print("drive")
				print(float(x[1]))
				vel_msg.linear.x = float(x[1])
				vel_msg.angular.z = 0
				velocity_publisher.publish(vel_msg)
			else:
				print("fout comando")
	else:
		print("cont stop")
			
	

def test_module():
	# Starts a new node
	rospy.init_node('receiver', anonymous=True)
	rospy.Subscriber('movement', String, callback)
	rospy.Subscriber('stop', String, stop_callback)
	velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	rate = rospy.Rate(1) # 10hz
	vel_msg = Twist()
    	# spin() simply keeps python from exiting until this node is stopped
   	rospy.spin()

if __name__ == '__main__':
    try:
        test_module()
    except rospy.ROSInterruptException:
        pass
