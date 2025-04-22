import rospy
from std_msgs.msg import String
import sys
import time

d0 = "Solve the taskoard: press the blue button, then plug the probe cable in its socket, then open the trapdoor and press the red button."

d1 = 'Can you please prepare the taskboard in the following way: Start by pressing the blue button in order to power the circuit. Then, plug the probe in the red socket and power the socket by pressing the red button. Finally open the gray hatch.'

d2 = 'Perform the following steps. First, press the blue button located on the right. Second, insert the cable in the red socket in the centre. Third, press the red button on the right. Finally, open the grey door on the left using the handle.'

d3 = "Press the blue button, plug the probe cable in the red socket, press the red button and then open the hatch."

#Fail after three steps because my boy forgot about the red button
d_olivier = """Follow these instruction in order: 
First press the blue button,
then plug the probe cable in the red socket, 
finally keep the grey door open."""

d4 = "Hi robot assistant, could you please help me probe the voltage on the machine. Here are the following instructions you need to follow to achieve this: first press the blue button then plug the cable into the red socket and press the red button and finally open the grey door on the left. Thanks!" 

d5 = "Dear Robot Assistant. You need to help me prepare a task so I want you to do the following steps sequentially. I want you to first press the blue button, then please plug the probe cable into the red socket and afterwards activate it by pressing the red button. Finally, open the grey door by pulling on the knob."

#Fail due to checks, just ends up printing
d6 = """Apply a vertical pressure on the blue button at the upper right of the box; Grasp the cable
Plug the la cable into the red socket, 
Check that the cable is well plugged,
Apply a vertical pressure on the red button at the upper right of the box; 
Open the door by gasping the door’s handle and then rotate the door around its axis using the handle;
Check that the door is opened."""

d7 = "I need your help for probing the voltage of one of the taskboard's ports placed under the grey door. You will need to perform several sequential tasks in that regards. Make sure you've completed each task before doing the next. First, you need to press the blue button so as to power the port. In a second time, you need to plug the probe cable into the red socket. Once that is done you need to power the socket by pressing the red button. Lastly, you need to open the port's door."

d8 = """first, power the circuitry by pressing the blue button
next, connect the probe cable to the red socket
after that, power the socket by pressing the red button
ensure the door is open"""

d9 = "Press the blue button. Take the cable next to the red socket out of the dark socket and put it in the red socket. Press the red button. Open the grey door."

ed = 'Prepare the taskboard for me. The probe charger is currently unplugged, the current is switched off (there is a blue button to switch it on) and the port I want to probe is behind a closed trapdoor.'

dlist = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9]

def talker(args=None):
    time.sleep(1)
    global n_task
    n_task = int(args[0])
    d = dlist[n_task]
    pub = rospy.Publisher('task', String, queue_size=10)
    pub2 = rospy.Publisher('plan', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    task_str = d
    rospy.loginfo(task_str)
    pub.publish(task_str)
        
    rospy.signal_shutdown('aa')
    sys.exit()

if __name__ == '__main__':
    try:
        talker(sys.argv[1:])
    except rospy.ROSInterruptException:
        pass
