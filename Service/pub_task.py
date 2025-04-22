import rospy
from std_msgs.msg import String
import sys
from main_file import *
import pickle
import time

def log(line):
    with open(f'./logs/log{n_task}.txt', 'a') as file:
        file.write(line+'\n')

def talker(args=None):
    print("Publisher ok")
    global n_task
    n_task = int(args[0])
    
    with open("task_list.pkl", "rb") as f:
        tasks = pickle.load(f)
    
    task = tasks[n_task]
    d = task.prompt
    
    print(d)
    
    pub = rospy.Publisher('task', String, queue_size=10)
    pub2 = rospy.Publisher('plan', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.0001)
    while not rospy.is_shutdown():
        hello_str = d
        log(d)
        time.sleep(1)
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        print("Publisher shutdown")
        sys.exit()

if __name__ == '__main__':
    try:
        talker(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
