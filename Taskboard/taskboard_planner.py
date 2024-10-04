import numpy as np
import rospy
import ollama
from std_msgs.msg import String
import time

def plan_prompt(task):
    prompt = """You are in charge of a robotic arm. Your task is the following: '"""+str(task)+"""'
Please output an plan, composed of simple actions, to carry out this task. Assume that the robot arm doesn't need to be moved to an object before interacting with it.

Please only output the plan as a tuple of strings, without any other text."""
    return(prompt)

def EO_prompt(task, plan):
    D = {}
    for i in range(len(eval(plan))):
        D['step'+str(i+1)] = ''
    prompt = """You are in charge of executing the following task: '"""+str(task)+"""'. The plan consists of the following steps: """+plan+""" Each of the steps of the plan will be carried out with a robotic arm ending with a gripper. For each step of the plan, I need you to give a more precise description of the actions involved in the step, in physical and visual terms.
This should consist of one or two short, simple sentences that are a more complete and detailed description of what the step should do. The sentences should describe what the robot should do, for example if it should move to a location, grasp an object (and what part of the object, if relevant for the task), or where an object should be put down. You can add some information if the plan is too concise. Here are some examples, with the plan step first and the requirements after:
-Press button: The robot should press the (color) button.
-Grasp object: The robot should grasp the (object) by the (object part).
For each step of the plan, please briefly describe the expected outcome as shown above. Please try to be concise and focus on the most relevant information. Please fill out the following python dictionnary with the expected outcomes: """ +str(D)+""". Only output the dictionnary and no other text."""# Please only output the expected outcomes as a tuple of strings, and no other text."""
    return(prompt)


class planner():
    def __init__(self):
        #self.listener_callback("Solve the taskoard: press the blue button, then plug in the probe cable, then open the trapdoor and press the red button.")
        self.plan_publisher_ = rospy.Publisher('plan', String, queue_size=10)
        self.EO_publisher_ = rospy.Publisher('EO', String, queue_size=10)
        self.subscription = rospy.Subscriber('task', String, self.listener_callback)
        self.subscription = rospy.Subscriber('plan', String, self.plan_callback)
    def ask(self, msg):
        messages = []
        messages.append({'role': 'user','content': msg})
        response = ollama.chat(model='llama3.1', stream=False, messages=messages, options={'temperature':0})

        # Preparing the assistant message by concatenating all received chunks from the API
        assistant_message = response['message']['content']
        return(response['message']['content'])
        
    def plan_callback(self, msg):
        self.plan = msg.data

    def listener_callback(self, msg):
        print('Entering callback')
        task = msg
        plan_p = plan_prompt(task)
        
        self.plan = self.ask(plan_p)
        print(self.plan)
        
        print(self.plan)
        EO_p = EO_prompt(task, self.plan)
        print('EO prompt ok')
        EO = self.ask(EO_p)
        print(EO)
        plan_out = String()
        plan_out.data = self.plan
        EO_out = String()
        EO_out.data = EO
        self.plan_publisher_.publish(plan_out)
        self.EO_publisher_.publish(EO_out)

def main(args=None):
    rospy.init_node('planner')
    #print('node ok')

    pl = planner()

    rospy.spin()


if __name__ == '__main__':
    main()
