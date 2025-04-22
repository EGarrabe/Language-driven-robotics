import numpy as np
import rospy
import ollama
import sys
import time

from std_msgs.msg import String

from init_prompt_taskboard import init_prompt, init_answer

class Orchestrator():
    def __init__(self):
        self.publisher = rospy.Publisher('llm_code', String, queue_size=10) #Pour publish le code que le LLM écrit
        self.task_sub = rospy.Subscriber('task', String, self.task_callback) #Pour recevoir la tâche
        self.plan_sub = rospy.Subscriber('plan', String, self.plan_callback) #Pour recevoir le plan
        self.EO_sub = rospy.Subscriber('EO', String, self.EO_callback) #Pour recevoir les expected outcomes
        self.feedback_sub = rospy.Subscriber('feedback', String, self.feedback_callback) #Pour recevoir le feedback du digital twin
        self.messages = []
        
        self.task = None
        self.plan = None
        self.EO = None
        self.timestep = 0
        self.plan_N = 0
        
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
        
        self.publisher.publish(output)
        
    def task_callback(self, msg):
        self.task = msg.data

    def plan_callback(self, msg):
        self.plan = eval(msg.data)
        self.plan_N = len(self.plan)

    def EO_callback(self, msg):
        self.EO = list(eval(msg.data).values()) #The expected outcomes are formatted as a dict for clarity, so here we extract the values to keep in a list
        time.sleep(1)
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
        prompt = init_prompt(self.task, self.plan, self.EO)
        print('\n')
        print('Feedback:')
        print(prompt)
        self.messages.append({'role': 'user','content': prompt})
        answer = init_answer
        print(answer)
        self.messages.append({'role': 'assistant', 'content': answer})
        
        self.step(False, '') #Trigger the first step. There is no feedback so far

    def step(self, success, feedback):
        #Update the plan if needed (the previous step was succesful), build the prompt and ask
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
            if self.EO == []:
                self.EO = ["0"]
        prompt = self.build_prompt(feedback)
        self.ask(prompt)
        
    def build_prompt(self, feedback):
        #The context is updated with the past step's feedback and the current plan.
        return(feedback + ' plan: (' + str(self.plan) + '). Details of current step: '+self.EO[0])
        
def main(args=None):
    print("orchestrator ok")
    rospy.init_node('orchestrator')

    sub = Orchestrator()

    rospy.spin()


if __name__ == '__main__':
    main()
