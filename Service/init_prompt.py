env_sort = """The current environment:
The objects are: ['Pliers', 'Bottle', 'Screwdriver', 'SodaCan', 'GreenTray', 'RedTray']
The locations are: ['Table']	
The Pliers, Bottle, Screwdriver, SodaCan, GreenTray and RedTray are on the Table. The robot is at the Table. The gripper is empty."""

env_desk = """The current environment:
The objects are: ['Pliers', 'Bottle', 'Screwdriver']
The locations are: ['Desk', 'Shelf', 'TrashCan']
The Pliers, Bottle and Screwdriver are on the Desk. The robot is at the Desk. The gripper is empty."""

env_bottle = """The current environment:
The objects are: ['Bottle', 'Mug']
The locations are: ['Table']
The Mug and Bottle are on the Table. The robot is at the Table. The gripper is empty."""

env_drink = """The current environment:
The objects are: ['WaterGlass']
The locations are: ['KitchenTable', 'UserDesk']
The WaterGlass is on the KitchenTable. The robot is at the UserDesk. The gripper is empty."""

env_microwave = """The current environment:
The objects are: ['Plate']
The locations are: ['Microwave', 'Counter']
The robot is at the UserDesk. The plate is in the robot's gripper."""

env_pie = """The current environment:
The objects are: ['Pie']
The locations are: ['KitchenTable', 'TrashCan']
The robot is at the UserDesk. The robot's gripper is empty. The pie is on the KitchenTable."""

env_clean = """The current environment:
The objects are: ['Glass1', 'Glass2', 'Glass3', 'Glass4', 'Plate1', 'Plate2', 'Plate3', 'Plate4']
The locations are: ['KitchenTable', 'KitchenCounter', 'Sink']
The robot is at the UserDesk. The robot's gripper is empty."""

env_desk2 = """The current environment:
The objects are: ['Mug', 'Mouse']
The locations are: ['Table', 'Desk', 'KitchenCounter']
The robot is at the Table. The objects are on the Desk. The robot's gripper is empty."""

env_charger = """The current environment:
The objects are: ['PhoneCharger'].
The locations are: ['Desk', 'Outlet']
The robot is at the Desk. The charger is on the Desk. The robot's gripper is empty."""

env_probe = """The current environment:
The objects are: ['VoltageProbe'].
The locations are: ['Table', 'Racl']
The robot is at the Table. The charger is on the Table. The robot's gripper is empty."""

env_pills = """The current environment:
The objects are: ['Soap', 'Pills', 'WaterGlass'].
The locations are: ['BathroomCounter', 'Bathtub', 'Desk']
The robot is at the UserDesk. The items are on the BathroomCounter. The robot's gripper is empty."""

env_plant = """The current environment:
The objects are: ['WaterGlass'].
The locations are: ['KitchenTable', 'CoffeeTable']
The robot is at the CoffeeTable. The WaterGlass is on the KitchenTable. The robot's gripper is empty."""

env_peach = """The current environment:
The objects are: ['Peach'].
The locations are: ['CoffeeTable', 'Desk']
The robot is at the CoffeeTable. The Phone is on the CoffeeTable. The robot's gripper is empty."""

env_winedinner = """The current environment:
The objects are: ['Plate', 'WineGlass'].
The locations are: ['Table', 'KitchenCounter']
The robot is at the Table. The objets are on the Table. The robot's gripper is empty."""

env = """The current environment:
The objects are: ['Sponge', 'Soap'].
The locations are: ['Table', 'KitchenCounter']
The robot is at the Table. The objets are on the KitchenCounter. The robot's gripper is empty."""

env_cabinet = """The current environment:
The objects are: ['Pills'].
The locations are: ['Cabinet', 'BathroomCounter']
The robot is at the Table. The Pills are on the BathroomCounter. The robot's gripper is empty."""

def init_prompt(task, plan, EO):
    prompt = """Context:
Your are now in charge of a mobile robot equipped with one arm with a parallel gripper. You will be given a high-level task that you will need to fulfill using this robot, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step the plan will be updated and you will receive feedback.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

get_position(object):
	#In: object (str): name of the object
	#Out: (pos) (3,1 array): position of the object
	#Get 3 degree-of-freedom position of the object
example: (x_drill, y_drill, z_drill) = get_position('drill')

move_arm_to(pos):
	#In: pos (3,1 array): Target position for the end effector
	#Moves the robot's end effector to a given position
example: move_arm_to((x_mug, y_mug, z_mug))

move_robot_to(target):
	#In: target (string): location to where the robot should move
	#Move robot body to target location
example: move_robot_to('Desk')
	
get_end_effector_position():
	#Out: (pos, orn) (6,1 array): position and orientation of the end effector
	#Get 6 degree-of-freedom position and orientation of the end effector
example: eff_pos_orn = get_end_effector_position(); eff_pos = eff_pos_orn[:3]

grasp_object(obj, part=None):
	#In: obj (string): object the robot should grasp
	#In: part (string, optionnal): part of the object that should be grasped. If unspecified, the robot chooses the most secure grasp possible.
	#Gripper goes to object 'obj' and grasps it
example: grasp_oject('Bottle')
example: grasp_object('Mug', 'Handle')

put_down(obj, target):
	#Put down object 'obj' at location 'target'
example: put_down('Mug', 'Table')

rotate_end_effector(angle):
	#In: angle (float): Angle of the end effector's rotation, clockwise
	#Rotates the end effetor by angle radians.
example: rotate_end_effector(3.14)

in_gripper(object):
	#In: object (string): Object that should be in the gripper or 'None' if the gripper should be empty
	#Out: (bool): True if the object is in the gripper, false otherwise
example: in_gripper('Pliers'), in_gripper('None')

open_obj(obj):
	#Opens the object. Requires the robot to be next to the object.
example: open_obj('Microwave')

close_obj(obj):
	#Closes the object. Requires the robot to be next to the object.
example: close_obj('Fridge')

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
Here are the expected outcomes of each step in the plan, which you can use as a guide:
""" + str(EO) + """

"""+env+"""

What I need you to do:
Please define a function do(), which will contain mostly action primitives to solve the steps of the plan one by one. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure the locations and objects that you pass as arguments are correct."""
    return(prompt)
  
  
def init_prompt_openloop(task, plan, EO):
#    prompt = """Context:
#You are now in charge of a mobile robot with one arm, equipped with a parallel gripper. You will be given a high-level task that you will need to fulfill using this arm, and the corresponding plan, 
    prompt = """Context:
Your are now in charge of a mobile robot equipped with two arms with parallel grippers. You will be given a high-level task that you will need to fulfill using this robot, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step the plan will be updated.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

get_position(object):
	#In: object (str): name of the object
	#Out: (pos) (3,1 array): position of the object
	#Get 3 degree-of-freedom position of the object
example: (x_drill, y_drill, z_drill) = get_position('drill')

move_arm_to(pos):
	#In: pos (3,1 array): Target position for the end effector
	#Moves the robot's end effector to a given position
example: move_arm_to((x_mug, y_mug, z_mug))

move_robot_to(target):
	#In: target (string): location to where the robot should move
	#Move robot body to target location
example: move_robot_to('Desk')
	
get_end_effector_position():
	#Out: (pos, orn) (6,1 array): position and orientation of the end effector
	#Get 6 degree-of-freedom position and orientation of the end effector
example: eff_pos_orn = get_end_effector_position(); eff_pos = eff_pos_orn[:3]

grasp_object(obj):
	#In: obj (string): object the robot should grasp
	#Gripper goes to object 'obj' and grasps it
example: grasp_oject('Bottle')

put_down(obj, target):
	#Put down object 'obj' at location 'target'
example: put_down('Mug', 'Table')

rotate_end_effector(angle):
	#In: angle (float): Angle of the end effector's rotation, clockwise
	#Rotates the end effetor by angle radians.
example: rotate_end_effector(3.14)

in_gripper(object):
	#In: object (string): Object that should be in the gripper or 'None' if the gripper should be empty
	#Out: (bool): True if the object is in the gripper, false otherwise
example: in_gripper('Pliers'), in_gripper('None')

open_obj(obj):
	#Opens the object. Requires the robot to be next to the object.
example: open_obj('Microwave')

close_obj(obj):
	#Closes the object. Requires the robot to be next to the object.
example: close_obj('Fridge')

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """
Here are the expected outcomes of each step in the plan, which you can use as a guide:
""" + str(EO) + """

"""+env+"""

What I need you to do:
Please define a function do(), which will contain mostly action primitives to solve the steps of the plan one by one. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure the locations and objects that you pass as arguments are correct."""
    return(prompt)
    
def init_prompt_noeo(task, plan):
    prompt = """Context:
Your are now in charge of a mobile robot equipped with an arm with a parallel gripper. You will be given a high-level task that you will need to fulfill using this robot, and the corresponding plan, which is a series of simpler steps. You will need to carry out the task step by step by interacting with the system using some code primitives. At each step the plan will be updated and you will receive feedback.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

get_position(object):
	#In: object (str): name of the object
	#Out: (pos) (3,1 array): position of the object
	#Get 3 degree-of-freedom position of the object
example: (x_drill, y_drill, z_drill) = get_position('drill')

move_robot_to(target):
	#In: target (string): location to where the robot should move
	#Move robot body to target location
example: move_robot_to('Desk')

move_arm_to(pos):
	#In: pos (3,1 array): Target position for the end effector
	#Moves the robot's end effector to a given position
example: move_arm_to((x_mug, y_mug, z_mug))
	
get_end_effector_position():
	#Out: (pos, orn) (6,1 array): position and orientation of the end effector
	#Get 6 degree-of-freedom position and orientation of the end effector
example: eff_pos_orn = get_end_effector_position(); eff_pos = eff_pos_orn[:3]

grasp_object(obj):
	#In: obj (string): object the robot should grasp
	#Gripper goes to object 'obj' and grasps it
example: grasp_oject('Mug')

put_down(obj, target):
	#Put down object 'obj' at location 'target'
example: put_down('Mug', 'Table')

rotate_end_effector(angle):
	#In: angle (float): Angle of the end effector's rotation, clockwise
	#Rotates the end effetor by angle radians.
example: rotate_end_effector(3.14)

in_gripper(object):
	#In: object (string): Object that should be in the gripper or 'None' if the gripper should be empty
	#Out: (bool): True if the object is in the gripper, false otherwise
example: in_gripper('Pliers'), in_gripper('None')

open_obj(obj):
	#Opens the object. Requires the robot to be next to the object.
example: open_obj('Microwave')

close_obj(obj):
	#Closes the object. Requires the robot to be next to the object.
example: close_obj('Fridge')

The task and the plan:
You are in charge of executing the following task: """ + str(task) + """. The plan is: """ + str(plan) + """

"""+env+"""

What I need you to do:
Please define a function do(), which will contain mostly action primitives to solve the steps of the plan one by one. Everytime we interact, this code should execute the first step of the current plan. You will then receive feedback. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure the locations and objects that you pass as arguments are correct."""
    return(prompt)
    
def init_prompt_os(task):
    prompt = """Context:
You are now in charge of a mobile robot with one arm, equipped with a parallel gripper. You will be given a high-level task that you will need to fulfill using this arm. You will need to carry out the task using some code primitives.
The skills are python functions, which allow you to perceive and act on your environment.

Skills:
Here are the functions and skills, with examples of the syntax:

get_position(object):
	#In: object (str): name of the object
	#Out: (pos) (3,1 array): position of the object
	#Get 3 degree-of-freedom position of the object
example: (x_drill, y_drill, z_drill) = get_position('drill')

move_arm_to(pos):
	#In: pos (3,1 array): Target position for the end effector
	#Moves the robot's end effector to a given position
example: move_arm_to((x_mug, y_mug, z_mug))

move_robot_to(target):
	#In: target (string): location to where the robot should move
	#Move robot body to target location
example: move_robot_to('Desk')
	
get_end_effector_position():
	#Out: (pos, orn) (6,1 array): position and orientation of the end effector
	#Get 6 degree-of-freedom position and orientation of the end effector
example: eff_pos_orn = get_end_effector_position(); eff_pos = eff_pos_orn[:3]

grasp_object(obj, part=None):
	#In: obj (string): object the robot should grasp
	#In: part (string, optionnal): part of the object that should be grasped. If unspecified, the robot chooses the most secure grasp possible.
	#Gripper goes to object 'obj' and grasps it
example: grasp_oject('Bottle')
example: grasp_object('Mug', 'Handle')

put_down(obj, target):
	#Put down object 'obj' at location 'target'
example: put_down('Mug', 'Table')

rotate_end_effector(angle):
	#In: angle (float): Angle of the end effector's rotation, clockwise
	#Rotates the end effetor by angle radians.
example: rotate_end_effector(3.14)

in_gripper(object):
	#In: object (string): Object that should be in the gripper or 'None' if the gripper should be empty
	#Out: (bool): True if the object is in the gripper, false otherwise
example: in_gripper('Pliers'), in_gripper('None')

open_obj(obj):
	#Opens the object. Requires the robot to be next to the object.
example: open_obj('Microwave')

close_obj(obj):
	#Closes the object. Requires the robot to be next to the object.
example: close_obj('Fridge')

The task:
You are in charge of executing the following task: """ + str(task) + """.

"""+env+"""

What I need you to do:
Please define a function do(), which will contain mostly action primitives to solve the task. Please output python code, enclosed between the tags <code> and </code>. Please only use the functions I defined above and ensure the locations and objects that you pass as arguments are correct."""
    return(prompt)
    
init_answer = """Here is the code for the first step:
<code>
def do():
	begin()
</code>"""
