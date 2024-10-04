import rospy
from std_msgs.msg import String

d_expert = "Solve the taskoard: press the blue button, then plug the probe cable in its socket, then open the trapdoor and press the red button."

def talker():
    pub = rospy.Publisher('task', String, queue_size=10)
    pub2 = rospy.Publisher('plan', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.0001)
    while not rospy.is_shutdown():
        task_str = d
        rospy.loginfo(task_str)
        pub.publish(task_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
