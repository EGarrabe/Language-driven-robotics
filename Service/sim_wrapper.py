import numpy as np
import pickle
#import rclpy
import rospy
import sys

from std_msgs.msg import String

from simulation.unity_simulator import comm_unity

#Expected outcomes could be better


def do():
	return
	
def check():
	return

def log(line):
	with open('log.txt', 'a') as file:
		file.write(line+'\n')

class robot:
	def __init__(self, name):
		self.held_obj = None #By default no object in gripper
		self.name = name
		self.location = 'Table'
		self.pos = [0,0,0]
	def grasp(self, obj):
		if self.location != obj.location:
			raise Exception('Robot and objects in different locations')
		elif self.held_obj != None:
			raise Exception('Gripper already full')
		else:
			self.held_obj = obj
			log('Grasp success')
			return(True)
		log('Grasp failure')
		return(False)
	def move_to(self,x,y,z):
		self.pos = [x,y,z]
		if self.held_obj != None:
			self.held_obj.pos = [x,y,z]

class sobject:
	def __init__(self, name, location='Table', pos = [0,0,0]):
		self.name = name
		self.toggled = False
		self.location = location
		self.pos = pos
	def get_position(self):
		return(self.pos)
	def toggle(self):
		self.toggled = True

class simulation:
	def __init__(self, robots):
		self.objects = []
		self.robots = robots
	def add_obj(self, obj):
		self.objects.append(obj)
	def save(self):
		#Save simulation state in case of outcome problems
		f = open('sim_state.pckl','wb')
		pickle.dump([self.objects, self.robots],f)
		f.close()
	def load(self):
		#Load simulation state after failure
		f = open('sim_state.pckl','rb')
		l = pickle.load(f)
		self.objects = l[0]
		self.robots = l[1]
		f.close()
	def check_collisions(self):
		return
	
class task():
	def __init__(self, sim):
		self.step = 0
		self.done = False
		self.sim = sim
		self.pub = rospy.Publisher('feedback', String, queue_size=10)
		self.task_sub = rospy.Subscriber('llm_code', String, self.input_cb)
		self.step = 0
	def task_ok(self):
		for piece in [glass1,glass2,glass3,glass4]:
			if piece.location != 'KitchenCounter':
				return False
		for piece in [plate1,plate2,plate3,plate4]:
			if piece.location != 'Sink':
				return False
		return True
	def input_cb(self, msg):
		#print('Entering callback')
		log(msg.data)
		self.step = self.step + 1
		if self.step >= 41:
			self.pub.publish('Task over')
			log('Task timeout')
			sys.exit()
		print(self.step)
		try:
			instr = msg.data.split('<code>')[1]
			instr = instr.split('</code>')[0]
		except:
			self.pub.publish('Please enclose the code between tags <code> and </code>')
			log('Invalid tags')
			return
		try:
			#exec(msg.data, globals())
			exec(instr, globals())
			log('Def ok')
		except Exception as e:
			self.pub.publish('Error in defining do(): '+str(e))
			log('Error in defining do(): '+ str(e))
			return
		try:
			do()
			self.pub.publish('Done. Object in robot gripper: ' +obj_in_gripper()+', robot location: '+str(robot_loc())+'. ')
			log('Done')
		except Exception as e1:
			self.pub.publish('Error in executing do(): '+str(e1)+'. Object in robot gripper: ' +obj_in_gripper()+', robot location: '+str(robot_loc())+'. ')
			log('Error in executing do(): '+str(e1))
			return
		if self.task_ok():
			self.pub.publish('Task over')
			log('Task ok')
			sys.exit()

grasp_part = None
success_prob = 1 #0.9
failed = False
def grasp_object(obj, part=None):
	global failed
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(list(objects.keys())))
	elif robot1.location != objects[obj].location:
		raise Exception('Robot and objects in different locations')
	elif robot1.held_obj == obj:
		return
	elif robot1.held_obj != None:
		raise Exception('Gripper already full')
	else:
		if failed: #np.random.uniform() <= success_prob:
			robot1.held_obj = objects[obj]
			instr = '<char0> [grab] ' + obj_ids[obj]
			comm.render_script([instr], recording=True, frame_rate=10)
			grasp_part = part
		else:
			failed = True
			raise Exception('Object fell from gripper, try again. Object in robot gripper: ' +obj_in_gripper()+', robot location: '+str(robot_loc())+'. ')
			log('Grasp failure')
		

def put_down(obj, target):
	global fridge_open
	global cabinet_open
	global trash_open
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(list(objects.keys())))
	elif robot1.held_obj == None:
		raise Exception('No object in gripper')
	elif objects[obj] != robot1.held_obj:
		raise Exception('Robot is holding a different object')
	elif target not in locations and target not in objects:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
	elif target not in objects and robot1.location != target:
		raise Exception('Robot is not at the target location')
	elif target == 'Fridge' and not fridge_open:
		raise Exception('Target must be open before objects are put inside')
	elif target == 'Cabinet' and not cabinet_open:
		raise Exception('Target must be open before objects are put inside')
	#elif target == 'TrashCan' and not trash_open:
	#	raise Exception('Target must be open before objects are put inside')
	else:
		robot1.held_obj = None
		objects[obj].location = target
		if target in ['Fridge', 'Microwave']:
			instr = '<char0> [putin] ' + obj_ids[obj] + ' ' + loc_ids[target]
		else:
			instr = '<char0> [putback] ' + obj_ids[obj] + ' ' + loc_ids[target]
		comm.render_script([instr], recording=True, frame_rate=10)
		grasp_part = None
		
def move_robot_to(target):
	if target not in locations:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
	else:
		robot1.location = target
		instr = '<char0> [walk] ' + loc_ids[target]
		comm.render_script([instr], recording=True, frame_rate=10)
		
def move_arm_to(pos):
	#TODO implement type check on pos
	#for o in objects:
	#	if objects[o].pos == [pos[0], pos[1], pos[2]]:
	#		raise Exception("Collision between arm and object during move. Avoid moving to an object's position")
	robot1.move_to(pos[0], pos[1], pos[2])
				
def rotate_end_effector(angle):
	if robot1.held_obj != None and angle >= np.pi/2:
		robot1.held_obj.toggle()
		
def in_gripper(obj):
	if obj in objects:
		return(robot1.held_obj == objects[obj])
	else:
		raise NameError('Invalid object. Valid objects are: '+str(objects.keys()))
	
def robot_at(location):
	if location in locations:
		return(robot1.location == location)
	else:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
		
def object_at(obj, location):
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(objects.keys()))
	elif location not in locations:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
	else:
		return(objects[obj].location == location)
		
def get_position(obj):
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(list(objects.keys())))
	else:
		return(objects[obj].pos)
		
def get_end_effector_position():
	return(robot1.pos+[0,0,0])
		
def obj_in_gripper():
	if robot1.held_obj == None:
		return('None')
	else:
		return(robot1.held_obj.name)
		
def robot_loc():
	return(robot1.location)

def open_obj(target):
	#if robot1.held_obj != None:
	#	raise Exception('Gripper needs to be empty for this action.')
	global fridge_open
	global cabinet_open
	global trash_open
	if target in locations:
		if robot1.location != target:
			raise Exception('Robot needs to be next to the object to open it.')
		else:
			instr = '<char0> [open] ' + loc_ids[target]
			comm.render_script([instr], recording=True, frame_rate=10)
			if target == 'Fridge':
				fridge_open = True
			elif target == 'TrashCan':
				trash_open = True
			elif target == 'Cabinet':
				cabinet_open = True
	elif target in objects:
		if objects[target].location != robot1.location:
			raise Exception('Robot needs to be next to the object to open it.')
		else:
			instr = '<char0> [open] ' + obj_ids[target]
			comm.render_script([instr], recording=True, frame_rate=10)
			
def close_obj(target):
	if target in locations:
		if robot1.location != target:
			raise Exception('Robot needs to be next to the object to close it.')
		else:
			instr = '<char0> [close] ' + loc_ids[target]
			comm.render_script([instr], recording=True, frame_rate=10)
	elif target in objects:
		if objects[target].location != robot1.location:
			raise Exception('Robot needs to be next to the object to close it.')
		else:
			instr = '<char0> [close] ' + obj_ids[target]
			comm.render_script([instr], recording=True, frame_rate=10)

YOUR_FILE_NAME = "./simulation/linux_exec.v2.2.4.x86_64" # Your path to the simulator
port= "8080" # or your preferred port

comm = comm_unity.UnityCommunication(file_name=YOUR_FILE_NAME, port=port)
print('Unity comm ok')
	
env_id = 0
comm.reset(env_id)

# Get graph
s, graph = comm.environment_graph()

# Get the fridge node
fridge_node = [node for node in graph['nodes'] if node['class_name'] == 'kitchencounter'][0]

# Open it
#fridge_node['states'] = ['OPEN']

# create a new node
new_node = {
    'id': 1001,
    'class_name': 'washingsponge',
    'states': []
}
# Add an edge
new_edge = {'from_id': 1001, 'to_id': fridge_node['id'], 'relation_type': 'ON'}
graph['nodes'].append(new_node)
graph['edges'].append(new_edge)

# update the environment
comm.expand_scene(graph)

print('Sponge added')
	
comm.add_character('Chars/Female1')

fridge_open = False
cabinet_open = False
trash_open = False

glass = sobject('WaterGlass', location='KitchenTable')
salmon = sobject('Salmon', location='Microwave')
plate = sobject('Plate')
microwave = sobject('Microwave', pos = [2,0,0])
fork = sobject('Fork', location='Cupboard')
knife = sobject('Knife', location='Cupboard')
trashcan = sobject('TrashCan', location='Kitchen')
sink = sobject('Sink', location='Kitchen')
pie = sobject('Pie', location='KitchenTable')

mug = sobject('Mug', location = 'Desk')
cupcake = sobject('Cupcake', location = 'Desk')
mouse = sobject('Mouse', location = 'Desk')
keyboard = sobject('Keyboard', location = 'Desk')

pliers = sobject('Pliers', location='Desk')
screwdriver = sobject('Screwdriver', location='Desk')

bottle = sobject('Bottle', pos = [1,0,0], location='Desk')
#mug = sobject('Mug', pos = [0,1,0])

glass1 = sobject('WaterGlass', location='KitchenTable')
glass2 = sobject('WaterGlass', location='KitchenTable')
glass3 = sobject('WaterGlass', location='KitchenTable')
glass4 = sobject('WaterGlass', location='KitchenTable')
plate1 = sobject('Plate', location='KitchenTable')
plate2 = sobject('Plate', location='KitchenTable')
plate3 = sobject('Plate', location='KitchenTable')
plate4 = sobject('Plate', location='KitchenTable')

glass11 = sobject('WaterGlass', location='BathroomCounter')
pills = sobject('Pills', location='BathroomCounter')
soap1 = sobject('Soap', location='BathroomCounter')

peach = sobject('Peach', location='CoffeeTable')


wineglass = sobject('WineGlass', location='Table')
plate31 = sobject('Plate', location='Table')

soap = sobject('Soap', location='KitchenCounter')
sponge = sobject('Sponge', location='KitchenCounter')

robot1 = robot('TiaGO')

#locations = ['Door', 'UserDesk', 'TrashCan', 'Fridge', 'Microwave', 'Counter']
#locations = ['KitchenTable', 'TrashCan']

#locations = ['Desk', 'TrashCan', 'Shelf']
#loc_ids = {'KitchenTable': '<kitchentable> (231)', 'UserDesk': '<coffeetable> (372)', 'TrashCan': '<garbagecan> (105)', 'Fridge': '<fridge> (306)', 'Microwave': '<microwave> (314)', 'Counter': '<kitchentable> (231)', 'Sink': '<sink> (247)', 'KitchenCounter': '<kitchencounter> (238)', 'Desk': '<kitchentable> (231)', 'Shelf': '<kitchencounter> (238)'}
#locations = ['BathroomCounter', 'Desk', 'Bathtub']

locations = ['KitchenCounter', 'Table']
#locations = ['BathroomCounter', 'Cabinet']
#locations = ['KitchenCounter', 'Desk', 'Table']
#locations = ['KitchenTable', 'CoffeeTable']
#locations = ['KitchenTable', 'UserDesk']
#locations = ['Desk', 'CoffeeTable']
loc_ids = {'Desk2': '<desk>: (110)', 'Table': '<coffeetable> (372)', 'KitchenCounter': '<kitchencounter> (238)', 'BathroomCounter': '<bathroomcounter> (50)', 'Bathroom': '<bathroom> (11)', 'Bathtub': '<bathtub> (39)', 'KitchenTable': '<kitchentable> (231)', 'CoffeeTable':'<coffeetable> (112)', 'Table1':'<coffeetable> (112)', 'TrashCan': '<garbagecan> (105)', 'Cabinet': '<bathroomcabinet> (49)', 'UserDesk': '<coffeetable> (372)', 'Shelf': '<kitchencounter> (238)', 'Desk': '<kitchentable> (231)'} #For plant exp coffeetable 113, for peach 372

#objects = {'Pliers': pliers, 'Bottle': bottle, 'Screwdriver': screwdriver}
#objects = {'Mouse': mouse, 'Keyboard': keyboard, 'Mug': mug, 'Cupcake':cupcake}
#objects = {'Glass1': glass1, 'Glass2': glass2, 'Glass3': glass3, 'Glass4': glass4, 'Plate1': plate1, 'Plate2': plate2, 'Plate3': plate3, 'Plate4': plate4}
#objects = {'Pliers': pliers, 'Bottle': bottle, 'Screwdriver': screwdriver}
#objects = {'WaterGlass': glass11, 'Pills': pills, 'Soap': soap}
#objects = {'Plate': plate31, 'WineGlass':wineglass}
objects = {'Soap': soap, 'Sponge': sponge}
#objects = {'Pills': pills}
#objects = {'WaterGlass': glass}
#objects = {'Pills': pills, 'WaterGlass': glass11}
#objects = {'Pie': pie}
#objects = {'Peach': peach}
#objects = {'Pills': pills}


obj_ids = {'WaterGlass1': '<waterglass> (271)', 'Salmon': '<salmon> (328)', 'Plate1': '<salmon> (328)', 'Pie':'<pie> (320)', 'Glass1': '<waterglass> (271)', 'Glass2': '<waterglass> (275)', 'Glass3': '<waterglass> (282)', 'Glass4': '<waterglass> (283)', 'Plate1': '<plate> (274)', 'Plate2': '<plate> (278)', 'Plate3': '<plate> (279)', 'Plate4': '<plate> (286)', 'Bottle': '<waterglass> (271)', 'Bottle': '<waterglass> (283)', 'Screwdriver': '<plate> (274)', 'Pliers': '<plate> (278)', 'Mouse': '<mouse> (172)', 'Keyboard': '<keyboard> (174)', 'Mug': '<mug> (196)', 'Cupcake': '<cupcake> (197)', 'WaterGlass': '<waterglass> (65)', 'Pills': '<painkillers> (64)', 'Soap1': '<barsoap> (67)', 'Peach': '<peach> (443)', 'Plate':'<plate> (201)', 'WineGlass':'<wineglass> (200)', 'Soap':'<dishwashingliquid> (268)', 'Sponge':'<washingsponge> (267)'}

robots = [robot1]
#robot1.held_obj = plate
instr = '<char0> [grab] <salmon> (328)'
#comm.render_script([instr], recording=True, frame_rate=10)


sim = simulation(robots)
sim.objects = objects

task = task(sim)

rospy.init_node('simulation')


rospy.spin()


# TODO put down needs the object or only location?
