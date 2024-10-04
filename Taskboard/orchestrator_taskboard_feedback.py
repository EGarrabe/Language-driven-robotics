import numpy as np
import rospy
import ollama
import sys
import time

from std_msgs.msg import String

from init_prompt_taskboard import init_prompt_noeo, init_answer

class Orchestrator():
    def __init__(self):
        self.publisher = rospy.Publisher('llm_code', String, queue_size=10)
        self.task_sub = rospy.Subscriber('task', String, self.task_callback)
        self.plan_sub = rospy.Subscriber('plan', String, self.plan_callback)
        self.feedback_sub = rospy.Subscriber('feedback', String, self.feedback_callback)
        self.messages = []
        
        self.task = None
        self.plan = None
        
    def ask(self, msg):
        #Add to the context and prompt the LLM
        self.messages.append({'role': 'user','content': msg})
        response = ollama.chat(model='llama3.1', stream=False, messages=self.messages, options={'temperature':0})

        #Extract and log LLM output
        assistant_message = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': assistant_message})
        
        #Parse the output to extract the code and then publish it for execution
        code = assistant_message #The parsing happens in the simulation so we can send the assistant message as is.
        output = String()
        output.data = code
        print(msg)
        print(code)
        
        self.publisher.publish(output)
        
    def task_callback(self, msg):
        self.task = msg.data

    def plan_callback(self, msg):
        self.plan = eval(msg.data)
        self.start()
            
    def feedback_callback(self, msg):
        #When feedback is received, go to the next step. The step is successful if the feedback was 'Done'
        feedback = msg.data
        if feedback == 'Task over':
            sys.exit()
        self.step(feedback[:4] == 'Done', feedback)
            
    def start(self):
        #Load the first interaction with the LLM (initial prompt and answer)
        prompt = init_prompt_noeo(self.task, self.plan)
        print(prompt)
        self.messages.append({'role': 'user','content': prompt})
        answer = init_answer
        print(answer)
        self.messages.append({'role': 'assistant', 'content': answer})
        
        self.step(False, '') #Trigger the first step. There is no feedback so far

    def step(self, success, feedback):
        #Update the plan if needed (the previous step was succesful), build the prompt and ask
        if success:
            self.plan = self.plan[1:]
        prompt = self.build_prompt(feedback)
        self.ask(prompt)
        
    def build_prompt(self, feedback):
        return(feedback + ' plan: (' + str(self.plan) + ').')
        
def main(args=None):
    rospy.init_node('orchestrator')

    sub = Orchestrator()

    rospy.spin()


if __name__ == '__main__':
    main()
