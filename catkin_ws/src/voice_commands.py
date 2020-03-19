#!/usr/bin/env python

# NOTE: this module requires PyAudio because it uses the Microphone class

import rospy
import speech_recognition as sr

commands = ("left", "right", "forward", "backwards", "dance", "play music", "music", "play", "shut down", "exit", "test")

# Obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    available_commands = []
    while True:
        print("Say something!")
        audio = r.listen(source)
        try:
            """
            Recognize speech using Google Speech Recognition
            For testing purposes, we're just using the default API key
            To use another API key, use r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY") instead of r.recognize_google(audio)
            """
            command = r.recognize_google(audio)
            print(command)
            if command in commands:
                print("Command recognized")
                pass

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
