#!/usr/bin/env python
# A music module by Stijn De Bels

import rospy
import os
import pygame, mutagen.mp3
from bpm_detection import get_file_bpm
from std_msgs.msg import String, Float64

pub = rospy.Publisher('comm_bpm', Float64, queue_size=10)
#pygame.init()
current_path = os.path.dirname(__file__)
def speel(f):
    try: #to make the music immediately play when another cmnd is sent
        pygame.mixer.quit()
    except Exception as e:
        pass
    file=os.path.join(current_path, f)
    #mp3=mutagen.mp3.MP3(file)
    #we need to do this to find the sample Rate, otherwise
    #it won't play in the right key and tempo
    pygame.mixer.init()#frequency=mp3.info.sample_rate)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    try:
        while pygame.mixer.music.get_busy() == True:
            continue
    except Exception as e:
            return;
    pygame.mixer.quit()

def callback(data):
    global pub
    vorigedata=data.data
    if (data.data=="Play+DanceMusic"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('startdancing.mp3')
        bpm = get_file_bpm(os.path.join(current_path, 'music-short.mp3'))
        pub.publish(bpm) #send the beats per minute so we can flash leds
        speel('music-short.mp3')

    if (data.data=="Play+ArucoTag"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('foundtag.mp3')

    if (data.data=="Play+ArucoNotRec"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('tagnotrecogn.mp3')

    if (data.data=="Play+VoiceOn"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('tellme.mp3')

    if (data.data=="Play+VoiceOff"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('thanks.mp3')

    if (data.data=="Play+VoiceNotRec"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('voicenotrecogn.mp3')

    if (data.data=="Play+Ultrasonic"):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        speel('socialdistance.mp3')

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
