#!/usr/bin/env python

"""
Voice recognition module
Node: voice_controller
Subscribed to: aruco_listener
Publishes  to: voice_listener
"""
import rospy
import speech_recognition as sr
from std_msgs.msg import String

listen = False

def callback(data):
    global listen
    listen = True
    rospy.loginfo("Aruco tag received: " + str(data))

def listener():
    global listen
    pub = rospy.Publisher('voice_listener', String, queue_size=10)
    rospy.init_node('voice_controller', anonymous=True)
    rospy.Subscriber("aruco_listener", String, callback)
    rate = rospy.Rate(2) #hz
    available_commands = ("left", "right", "forward", "backwards", "dance", "music", "play", "exit", "test")
    command = ""
    while not rospy.is_shutdown():
        # Obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if listen:
                rospy.loginfo("Say something!")
                audio = r.listen(source)
                try:
                    command = r.recognize_google(audio)
                    # Split phrase into words
                    command_list = command.split()
                    # Only select first word of phrase (to make recognizer more robust)
                    if command_list[0] in available_commands:
                        rospy.loginfo("Command recognized, publishing: " + command_list[0])
                        pub.publish(command_list[0])
                        listen = False
                        continue

                    else :
                        rospy.loginfo("Command not recognized: " + command)

                except sr.UnknownValueError:
                    rospy.loginfo("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                    rospy.loginfo("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                rospy.loginfo("Waiting on aruco tag")
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.loginfo("Module running")
        listener()
    except rospy.ROSInterruptException:
        pass
