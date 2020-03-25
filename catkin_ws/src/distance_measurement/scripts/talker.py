import rospy
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('chatter', String, queue_size=10)
	pub2 = rospy.Publisher('movement', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1) # 10hz
	while not rospy.is_shutdown():
		#hello_str = "hello world %s" % rospy.get_time()
		txt = raw_input("Enter your value: ") 
		print(txt) 
		rospy.loginfo(txt)
		pub2.publish(txt)
	rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass