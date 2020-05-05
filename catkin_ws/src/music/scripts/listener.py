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

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
import os
import pygame
from bpm_detection import get_file_bpm
from std_msgs.msg import String, Float64

pub = rospy.Publisher('comm_bpm', Float64, queue_size=10)
pygame.init()
current_path = os.path.dirname(__file__)

def callback(data):
    global pub
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    vorigedata=data.data
    if (data.data=="Play+DanceMusic"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.music.load(os.path.join(current_path, 'startdancing.mp3'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            rospy.loginfo("hier")
        #    if (vorigedata==data.data):
 		#        continue
        #    else:
        #        break
            continue

        pygame.mixer.music.load(os.path.join(current_path, 'music.mp3'))
        bpm = get_file_bpm(os.path.join(current_path, 'music.mp3'))
        pub.publish(bpm)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            rospy.loginfo("hier")
        #    if (vorigedata==data.data):
 		#        continue
        #    else:
        #        break
            continue
    if (data.data=="Play+ArucoTag"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, 'foundtag.mp3'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
        #    if (vorigedata==data.data):
 		#        continue
    #        else:
    #            break
            continue
    if (data.data=="Play+ArucoNotRec"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, "tagnotrecogn.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    if (data.data=="Play+VoiceOn"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, "tellme.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
    #        if (vorigedata==data.data):
 	#	        continue
    #        else:
    #            break
            continue
    if (data.data=="Play+VoiceOff"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, "thanks.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
    #        if (vorigedata==data.data):
 	#	        continue
    #        else:
    #            break
            continue
    if (data.data=="Play+VoiceNotRec"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, "voicenotrecogn.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
        #    if (vorigedata==data.data):
 		 #       continue
        #    else:
        #        break
            continue
    if (data.data=="Play+Ultrasonic"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(current_path, "socialdistance.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
        #    if (vorigedata==data.data):
 		 #       continue
        #    else:
        #        break
            continue
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Sound_controller', anonymous=True)
    rospy.Subscriber('sound', String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
