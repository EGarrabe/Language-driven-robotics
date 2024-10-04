import rospy
from std_msgs.msg import String

d_desk = "Put the pliers and screwdriver on the shelf and the bottle in the trash. The objects are currently on the desk."

d_pie = 'Put the pie in the trash can.'

d_drink = 'Bring me a drink. There is a water glass on the kitchen table. The robot is at the user desk and the gripper is empty.'

d_desk2 = 'Bring the mouse to the table and put the mug on the kitchen counter. The mouse and the mug are on on the desk.'

d_pills = 'Bring pills and a water glass to my desk. The items are on the bathroom counter. The robot is in the bathroom.'

d_plant = 'Bring me something to water my plant with. There is a water glass on the kitchen table and I am at the coffee table.'

d_peach = "I'm hungry. There is a peach on the coffee table and I am at my desk."

d_winedinner = 'I am done eating. Please clear the table. There are a wine glass and a plate on the table.'

d_stain = 'Bring me something to clean this stain on the table. There are soap and a sponge on the kitchen counter.'

d_cabinet = 'Put away the pills in the bathroom cabinet. The pills are on the bathroom counter.'

d = d_pills

def talker():
    pub = rospy.Publisher('task', String, queue_size=10)
    pub2 = rospy.Publisher('plan', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.0001)
    while not rospy.is_shutdown():
        hello_str = d
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
