#!/usr/bin/env python

import rospy
import speech_recognition as sr
from std_msgs.msg import String

def voice_commands():
    pub = rospy.Publisher('voice listener', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) #10hz
    available_commands = ("left", "right", "forward", "backwards", "dance", "play music", "music", "play", "shut down", "exit", "test")
    command = ""
    listen = False
    while not rospy.is_shutdown():
        # Obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if listen:
                print("Say something!")
                audio = r.listen(source)
                try:
                    command = r.recognize_google(audio)
                    print(command)
                    if command in available_commands:
                        print("Command recognized")
                        #TODO: Confirm command with correct sound feedback
                    else :
                        print("Command not recognized")
                        #TODO: Confirm command with faulty sound feedback

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        rospy.loginfo(command)
        pub.publish(command)
        rate.sleep()
