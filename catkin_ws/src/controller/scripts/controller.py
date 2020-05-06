#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String

move_pub = rospy.Publisher('movement', String, queue_size=10)
sound_pub = rospy.Publisher('sound', String, queue_size=10)

var_move = 0 #Debug var

#List to remember the movenments of the bot, so it can return home
movement_list = list()

def dance():
    print "Dance" #Debug print
    sound_pub.publish("Play+DanceMusic")
    move_pub.publish("start")
    move_pub.publish("d+1")
    move_pub.publish("r+90")
    move_pub.publish("d+1")
    move_pub.publish("r+540")
    move_pub.publish("d+2")
    move_pub.publish("r+180")
    move_pub.publish("d+1")
    move_pub.publish("r+90")
    move_pub.publish("d+1")
    move_pub.publish("r+180")
    


def return_home(data):
    print "Return home" #Debug print
    move_pub.publish("start")
    move_pub.publish("r+360")
    

def foute_data(errorms):
    print "Fault "+errorms

    
def movement(verplaatsing):
    print verplaatsing #Debug print
    move_pub.publish("start")
    move_pub.publish(verplaatsing)

#Handels the strings that come from toppic comm_cam
def aruco(data):
    print data.data #Debug print
    #Determine command
    if (data.data=="dance"):
        sound_pub.publish("Play+ArucoTag")
        dance()
    elif (data.data=="home"):
        sound_pub.publish("Play+ArucoTag")
        return_home()
    elif (data.data=="go"):
        sound_pub.publish("Play+ArucoTag")
        movement("d+1")
    else:
        sound_pub.publish("Play+ArucoNotRec")
        foute_data("Aruco")

def follow(data):
    print "follow or home"
    print data.data
    if (data.data=="tag+r"):
        movement("r+360") #max turning
    elif (data.data=="tag+d"):
        movement("d+100") #overkill distance
    else:
        foute_data("follow")

#Handels the strings that come from toppic comm_voice
def voice(data):
    print data.data #Debug print
    if (data.data=="dance"):
        sound_pub.publish("Play+VoiceOff")
        dance()
    elif (data.data=="home"):
        sound_pub.publish("Play+VoiceOff")
        return_home()
    elif (data.data=="go"):
        sound_pub.publish("Play+VoiceOff")
        movement("d+1")
    else:
        sound_pub.publish("Play+VoiceNotRec")
        foute_data("voice")

def voice_start(data):
    print data.data #Debug print
    if (data.data=="start"):
        sound_pub.publish("Play+VoiceOn")
    elif (data.data=="aruco"):
        sound_pub.publish("Play+VoiceOn")
    else:
        sound_pub.publish("Play+ArucoNotRec")


def central_switcher():
    #Init of node
    rospy.init_node('central_switcher', anonymous=True)
    #Subscribe on the aruco, distance and voice toppic
    rospy.Subscriber('comm_cam', String, aruco)
    rospy.Subscriber('comm_voice', String, voice)
    rospy.Subscriber('comm_voice_start', String, voice_start)
    rospy.Subscriber('comm_pos', String, follow)
    #Keep hanging until one of the three gives a responce
    rospy.spin()


if __name__ == '__main__':
    try:
        central_switcher()
    except rospy.ROSInterruptException:
        print "Error in main"
        pass