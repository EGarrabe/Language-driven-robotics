import numpy as np
import rospy
import ollama
import sys

from std_msgs.msg import String

from init_prompt import init_prompt_openloop, init_answer

class Orchestrator():

    def __init__(self):
        self.task_sub = rospy.Subscriber('task', String, self.task_callback)
        self.plan_sub = rospy.Subscriber('plan', String, self.plan_callback)
        self.EO_sub = rospy.Subscriber('EO', String, self.EO_callback)
        self.messages = []
        self.task = None
        self.plan = None
        self.EO = None
        
    def ask(self, msg):
        #Add to the context and prompt the LLM
        self.messages.append({'role': 'user','content': msg})
        response = ollama.chat(model='llama3.1', stream=False, messages=self.messages, options={'temperature':0})

        #Extract and log LLM output
        assistant_message = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': assistant_message})
        
        #Publish the output for execution
        code = assistant_message
        output = String()
        output.data = code
        print(msg)
        print(code)
        
        self.step(True, 'Done.')
        
    def task_callback(self, msg):
        self.task = msg.data

    def plan_callback(self, msg):
        self.plan = eval(msg.data)
            
    def EO_callback(self, msg):
        self.EO = list(eval(msg.data).values()) #The expected outcomes are formatted as a dict for clarity, so here we extract the values to keep in a list
        self.start()
            
    def start(self):
        #Load the first interaction with the LLM (initial prompt and answer)
        prompt = init_prompt_openloop(self.task, self.plan, self.EO)
        print(prompt)
        self.messages.append({'role': 'user','content': prompt})
        
        answer = init_answer
        print(answer)
        self.messages.append({'role': 'assistant', 'content': answer})
        
        self.step(False, '') #Trigger the first step. There is no feedback so far

    def step(self, success, feedback):
        #Update the plan, build the prompt and ask
        if len(self.plan) == 0:
        	sys.exit()
        if success:
            self.plan = self.plan[1:]
            self.EO = self.EO[1:]
        prompt = self.build_prompt(feedback)
        self.ask(prompt)
        
    def build_prompt(self, feedback):
        #The context is updated with the past step's feedback and the current plan.
        return(feedback + '. plan: (' + str(self.plan) + '). Details of current step: '+self.EO[0])
        
def main(args=None):
    rospy.init_node('orchestrator')

    sub = Orchestrator()

    rospy.spin()


if __name__ == '__main__':
    main()
    
#ros2 topic pub /tasks std_msgs/String 'data: Hello World' -1
