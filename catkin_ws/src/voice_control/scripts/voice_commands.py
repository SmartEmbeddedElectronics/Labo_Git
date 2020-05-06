#!/usr/bin/env python

"""
Voice recognition module:
    ----------------------------------------
    |   Node: Voice_controller             |
    |   Subscribed to: comm_voice_start    |
    |   Publishes  to: comm_voice          |
    ----------------------------------------
"""

import rospy
import time
import speech_recognition as sr
from std_msgs.msg import String


listen = False

def levenshteinDistance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings.

    Arguments:
        s1 {String} -- first string to match
        s2 {String} -- second string to match

    Returns:
        int -- the Levenshtein distance.
    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def callback(data):
    """
    Callback function for the comm_voice_start topic.
    Sets the global listen flag on True, to start listening for a voice.

    Arguments:
        data {String} -- Data from topic comm_voice_starts
    """
    global listen
    rospy.loginfo("Aruco tag received: " + str(data))
    time.sleep(1) # elay so that audible feedback gets heard first
    listen = True


def listener(available_commands = None, threshold = 3, frequency = 2):
    """
    Listens to speech and uses the Google TTS API for transforming this speech to text.
    Then this text gets interpreted (and/or corrected) to a valid command.
    This valid command then gets outputted on the comm_voice topic.

    Keyword Arguments:
        available_commands {Tuple[Strings]} -- Tuple of all available commands that can be used  (default: {None})
        threshold {int} -- Threshold for the maximum allowed Levenshtein distance  (default: {3})
        frequency {int} -- Frequency of while function (in Hertz)  (default: {2})
    """
    global listen
    pub = rospy.Publisher('comm_voice', String, queue_size=10)
    rospy.init_node('Voice_controller', anonymous=True)
    rospy.Subscriber("comm_voice_start", String, callback)
    rate = rospy.Rate(frequency) #hz
    if available_commands == None:
        available_commands = ("left", "right", "forward", "backwards", "dance", "music", "exit", "home", "go", "stop")
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
                        rospy.loginfo("Trying to find similar commands...")
                        distance = None
                        correct_command = ""
                        # Find strings with most similarities using Levenshteins distance
                        for available_command in available_commands:
                            if distance > levenshteinDistance(command_list[0], available_command) or distance == None:
                                distance = levenshteinDistance(command_list[0], available_command)
                                correct_command = available_command

                        if distance <= threshold:
                            rospy.loginfo("Command corrected to: " + correct_command + ", publishing.")
                            pub.publish(correct_command)
                            listen = False
                            continue

                except sr.UnknownValueError:
                    rospy.logwarn("Google Speech Recognition could not understand audio. Try again.")

                except sr.RequestError as e:
                    rospy.logerr("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                rospy.loginfo("Waiting on aruco tag")
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.logdebug("Module running")
        listener()
    except rospy.ROSInterruptException:
        pass
