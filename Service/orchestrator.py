import numpy as np
import rospy
import ollama
import sys

from std_msgs.msg import String

from init_prompt import init_prompt, init_answer

from main_file import *

import pickle

import time

def log(line):
    with open(f'./logs/log{n_task}.txt', 'a') as file:
        file.write(line+'\n')
def logTime(line):
    with open('times.txt', 'a') as file:
        file.write(str(line)+'\n')

class Orchestrator():

    def __init__(self):
        self.publisher = rospy.Publisher('llm_code', String, queue_size=10)
        self.task_sub = rospy.Subscriber('task', String, self.task_callback)
        self.plan_sub = rospy.Subscriber('plan', String, self.plan_callback)
        self.plan_N = 0
        self.EO_sub = rospy.Subscriber('EO', String, self.EO_callback)
        self.feedback_sub = rospy.Subscriber('feedback', String, self.feedback_callback)
        self.messages = []
        self.task = None
        self.plan = None
        self.EO = None
        self.env = None
        self.timestep = 0
        
    def ask(self, msg):
        log(msg)
        #Add to the context and prompt the LLM
        self.messages.append({'role': 'user','content': msg})
        t1 = time.time()
        response = ollama.chat(model='llama3.1', stream=False, messages=self.messages, options={'temperature':0})
        t2 = time.time()
        logTime(t2-t1)

        #Extract and log LLM output
        assistant_message = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': assistant_message})
        
        #Publish the output for execution
        code = assistant_message
        output = String()
        output.data = code
        print(msg)
        print(code)
        log(code)
        print("Code ready")
        self.publisher.publish(output)
        print("Code published")
        
    def task_callback(self, msg):
        self.task = msg.data

    def plan_callback(self, msg):
        print("Plan received")
        self.plan = eval(msg.data)
        self.plan_N = len(self.plan)
            
    def EO_callback(self, msg):
        self.EO = list(eval(msg.data).values()) #The expected outcomes are formatted as a dict for clarity, so here we extract the values to keep in a list
        self.start()
            
    def feedback_callback(self, msg):
        #When feedback is received, go to the next step. The step is successful if the feedback was 'Done'
        feedback = msg.data
        
        if feedback == 'Task over':
            print("Orchestrator shutdown on task success")
            rospy.signal_shutdown('aa')
            sys.exit()
        self.step(feedback[:4] == 'Done', feedback)
            
    def start(self):
        #Load the first interaction with the LLM (initial prompt and answer)
        prompt = init_prompt(self.task, self.plan, self.EO, self.env)
        print(prompt)
        self.messages.append({'role': 'user','content': prompt})
        
        answer = init_answer
        print(answer)
        self.messages.append({'role': 'assistant', 'content': answer})
        
        self.step(False, '') #Trigger the first step. There is no feedback so far

    def step(self, success, feedback):
        #Update the plan if needed (the previous step was succesfull), build the prompt and ask
        self.timestep = self.timestep + 1
        if self.timestep > self.plan_N*2:
            print(f"Orchestrator shutdown on task failure (step {self.timestep})")
            output = String()
            output.data = "Timeout"
            log("Timeout")
            self.publisher.publish(output)
            rospy.signal_shutdown('aa')
            sys.exit()
        if success:
            self.plan = self.plan[1:]
            self.EO = self.EO[1:]
        prompt = self.build_prompt(feedback)
        self.ask(prompt)
        
    def build_prompt(self, feedback):
        #The context is updated with the past step's feedback and the current plan.
        return(feedback + 'Plan: (' + str(self.plan) + '). Expected outcome of current step: '+self.EO[0])
        
def main(args=None):
    print("Orches ok")
    global n_task
    n_task = int(args[0])
    
    with open("task_list.pkl", "rb") as f:
        tasks = pickle.load(f)
    
    task = tasks[n_task]
    print(task.env())
    rospy.init_node('orchestrator')

    sub = Orchestrator()
    sub.env = task.env()

    rospy.spin()


if __name__ == '__main__':
    main(sys.argv[1:])
#ros2 topic pub /tasks std_msgs/String 'data: Hello World' -1
