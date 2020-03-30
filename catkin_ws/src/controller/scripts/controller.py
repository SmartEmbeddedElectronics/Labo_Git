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
    move_pub.publish("Command 1")
    move_pub.publish("Command 2")
    move_pub.publish("Command 3")
    sound_pub.publish("Start dance song")


def return_home(data):
    global movement_list
    print "Return home" #Debug print
    for st in reversed(movement_list):
        #Reminder: reverse speed
        move_pub.publish(st)
    del movement_list[:]
    

def foute_data(data):
    print "Foute data" #Debug print
    print data.data


def stop():
    print "Bot stop"
    move_pub.publish("Snelheid = 0")
    
def movement(data):
    print data.data #Debug print
    global var_move
    var_move+=1
    movement_list.append("Straigt "+str(var_move))
    
    move_pub.publish("Go straight")
    print movement_list

#Handels the strings that come from toppic comm_cam
def aruco(data):
    print data.data #Debug print
    #Determine command
    if (data.data=="dance"):
        dance()
    elif (data.data=="home"):
        return_home(data)
    elif (data.data=="go"):
        movement(data)
    else:
        foute_data("Aruco")



#Handels the strings that come from toppic comm_voice
def voice(data):
    print data.data #Debug print
    if (data.data=="dance"):
        dance()
    elif (data.data=="home"):
        return_home(data)
    elif (data.data=="go"):
        movement(data)
    else:
        foute_data("Aruco")

#Handels the strings that come from toppic comm_distance
def distance(data):
    print data.data #Debug print
    if (data.data=="stop"):
        stop()
    else:
        foute_data("Aruco")

def central_switcher():
    #Init of node
    rospy.init_node('central_switcher', anonymous=True)
    #Subscribe on the aruco, distance and voice toppic
    rospy.Subscriber('comm_cam', String, aruco)
    rospy.Subscriber('comm_voice', String, voice)
    rospy.Subscriber('comm_distance', String, distance)
    #Keep hanging until one of the three gives a responce
    rospy.spin()


if __name__ == '__main__':
    try:
        central_switcher()
    except rospy.ROSInterruptException:
        print "Error in main"
        pass