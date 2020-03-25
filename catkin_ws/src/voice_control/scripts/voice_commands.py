#!/usr/bin/env python

import rospy
import speech_recognition as sr
from std_msgs.msg import String

listen = False

def callback():
    global listen
    listen = True
    print("Aruco tag received\nBegin listening")


def listener():
    global listen
    pub = rospy.Publisher('voice_listener', String, queue_size=10)
    rospy.init_node('voice_controller', anonymous=True)
    rospy.Subscriber("aruco_listener", String, callback)
    rate = rospy.Rate(1) #hz
    available_commands = ("left", "right", "forward", "backwards", "dance", "play music", "music", "play", "shut down", "exit", "test")
    command = ""
    while not rospy.is_shutdown():
        # Obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if listen:
                listen = False
                audio = r.listen(source)
                try:
                    command = r.recognize_google(audio)
                    print(command)
                    if command in available_commands:
                        rospy.loginfo("Command recognized")
                        rospy.loginfo(command)
                        pub.publish(command)
                    else :
                        rospy.loginfo("Command not recognized")

                except sr.UnknownValueError:
                    rospy.loginfo("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                    rospy.loginfo("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                rospy.loginfo("sleeping")
        rate.sleep()

if __name__ == '__main__':
    try:
        print("Module running")
        listener()
    except rospy.ROSInterruptException:
        pass
