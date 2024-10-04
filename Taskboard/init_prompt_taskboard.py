env = """The current environment:
The buttons are: ['Blue', 'Red'] The gripper is empty."""

def init_prompt(task, plan, EO):
    prompt = """Context:
Your are now in charge of a robotic arm on a table, equipped with a parallel gripper. You will be given a high-level task that you will need to fulfill using this arm, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step you will receive feedback and an updated plan.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

press_button(color):
	#In: color (str): color of the button you want to press ('Red' or 'Blue')
	#Press the button with the specified color. The blue button starts the task and the red button ends it.
example: press_button('Blue')

plug_cable():
	#Plug the probe's cable
example: plug_cable()

open_door():
	#Opens the trapdoor
example: open_door()

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
Here are the expected outcomes of each step in the plan, which you can use as a guide:
""" + str(EO) + """

"""+env+"""

What I need you to do:
Each time we interact, please define a function do(), which will contain mostly action primitives to solve the first step of the plan. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure that the code matches the current step of the plan."""
    return(prompt)

def init_prompt_noeo(task, plan):
    prompt = """Context:
Your are now in charge of a robotic arm on a table, equipped with a parallel gripper. You will be given a high-level task that you will need to fulfill using this arm, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step you will receive feedback and an updated plan.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

press_button(color):
	#In: color (str): color of the button you want to press ('Red' or 'Blue')
	#Press the button with the specified color. The blue button starts the task and the red button ends it.
example: press_button('Blue')

plug_cable():
	#Plug the probe's cable
example: plug_cable()

open_door():
	#Opens the trapdoor
example: open_door()

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
"""+env+"""

What I need you to do:
Each time we interact, please define a function do(), which will contain mostly action primitives to solve the first step of the plan. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure that the code matches the current step of the plan."""
    return(prompt)
    
def init_prompt_ol(task, plan, EO):
    prompt = """Context:
Your are now in charge of a robotic arm on a table, equipped with a parallel gripper. You will be given a high-level task that you will need to fulfill using this arm, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step you will receive an updated plan.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

press_button(color):
	#In: color (str): color of the button you want to press ('Red' or 'Blue')
	#Press the button with the specified color. The blue button starts the task and the red button ends it.
example: press_button('Blue')

plug_cable():
	#Plug the probe's cable
example: plug_cable()

open_door():
	#Opens the trapdoor
example: open_door()

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
Here are the expected outcomes of each step in the plan, which you can use as a guide:
""" + str(EO) + """

"""+env+"""

What I need you to do:
Each time we interact, please define a function do(), which will contain mostly action primitives to solve the first step of the plan. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure that the code matches the current step of the plan."""
    return(prompt)
    
init_answer = """Here is the code to begin the task:
<code>
def do():
	begin()
</code>"""
