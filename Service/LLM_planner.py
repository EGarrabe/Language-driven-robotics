import numpy as np
import rospy
import ollama
from std_msgs.msg import String
import time

def plan_prompt(task):
    prompt = """You are in charge of a mobile robot with an arm ending in a gripper. Your task is the following: '"""+task+"""'
Please output an plan, composed of simple actions, to carry out this task. Remember that the robot should always move to a location before interacting with objects in this location, unless it is already there. However, you can assume that simple actions (such as grasping or putting down objects) automatically move the arm to the correct position.

Please only output the plan as a tuple of strings, where each step is a string, without any other text."""
    return(prompt)

def EO_prompt(task, plan):
    D = {}
    for i in range(len(eval(plan))): #Eval the plan to get the length of the tuple
        D['step'+str(i+1)] = ''
    prompt = """You are in charge of executing the following task: '"""+task+"""'. The plan consists of the following steps: """+plan+""" Each of the steps of the plan will be executed with a mobile robot equipped with an arm ending in a gripper. For each step of the plan, I need you to give a more precise description of the actions involved in the step, in physical and visual terms.
This should consist of one or two short, simple sentences that are a more complete and detailed description of what the step should do. The sentences should describe what the robot should do, for example if it should move to a location, grasp an object (and what part of the object, if relevant for the task), or where an object should be put down. You can add some information if the plan is too concise. Here are some examples, with the plan step first and the requirements after:
- Put bottle on shelf: The robot should put the bottle down on the shelf.
- Grasp the mug: The robot should move to the table (where the mug is) and grasp the mug.
- Grasp the knife: The robot should grasp the knife by the blade.
For each step of the plan, please briefly describe the expected outcome as shown above. Please try to be concise and focus on the most relevant information. Please fill out the following python dictionnary with the detailed plan steps: """ +str(D)+""". Only output the dictionnary and no other text."""
    return(prompt)


class planner():
    def __init__(self):
        self.plan_publisher_ = rospy.Publisher('plan', String, queue_size=10)
        self.EO_publisher_ = rospy.Publisher('EO', String, queue_size=10)
        self.subscription = rospy.Subscriber('task', String, self.listener_callback)
    def ask(self, msg):
        messages = []
        messages.append({'role': 'user','content': msg})
        response = ollama.chat(model='llama3.1', stream=False, messages=messages, options={'temperature':0})

        #Get and return the response
        assistant_message = response['message']['content']
        return(response['message']['content'])

    def listener_callback(self, msg):
        print('Entering callback')
        task = msg.data
        
        plan_p = plan_prompt(task)
        self.plan = self.ask(plan_p)
        print(self.plan)
        
        EO_p = EO_prompt(task, self.plan)
        EO = self.ask(EO_p)
        print(EO)
        
        #Publish plan and EOs
        plan_out = String()
        plan_out.data = self.plan
        EO_out = String()
        EO_out.data = EO
        self.plan_publisher_.publish(plan_out)
        self.EO_publisher_.publish(EO_out)

def main(args=None):
    rospy.init_node('planner')

    pl = planner()

    rospy.spin()


if __name__ == '__main__':
    main()
