#Describe the environment: what objects and locations are available to the robot, where each object is and where the robot is (if it is mobile). The names of the objects and locations should match the API names.
env = """The current environment:
The objects are: []
The locations are: []	

"""

#Describe the robot platform (at the vey beginning of the prompt, add the available skills.
def init_prompt(task, plan, EO):
    prompt = """Context:
Your are now in charge of... You will be given a high-level task that you will need to fulfill using this robot, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step the plan will be updated and you will receive feedback.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:



The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
Here are the expected outcomes of each step in the plan, which you can use as a guide:
""" + str(EO) + """

"""+env+"""

What I need you to do:
Please define a function do(), which will contain mostly action primitives to solve the steps of the plan one by one. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure the locations and objects that you pass as arguments are correct."""
    return(prompt)
    
init_answer = """Here is the code for the first step:
<code>
def do():
	begin()
</code>"""
