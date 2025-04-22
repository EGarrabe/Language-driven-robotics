import numpy as np
import pickle
#import rclpy
import rospy
import sys

from std_msgs.msg import String


from main_file import *

import pickle

#Placeholder for the 'do' function, the LLM will overwrite the definition at each step.
def do():
	return

def log(line):
	#with open('log.txt', 'a') as file:
	#	file.write(line+'\n')
	return

def log_succ():
	with open('success_count.txt', 'a') as file:
		file.write('1 \n')

class robot:
	def __init__(self, name):
		self.held_obj = None #By default no object in gripper
		self.name = name
		self.location = 'Table'
		self.pos = [0,0,0] #Arm position relative to the robot base. Not needed in these experiments
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
	
class task_local():
	def __init__(self, sim):
		print("Local task created")
		self.step = 0
		self.done = False
		self.sim = sim
		self.pub = rospy.Publisher('feedback', String, queue_size=10)
		self.task_sub = rospy.Subscriber('llm_code', String, self.input_cb)
		self.step = 0
	def input_cb(self, msg):
		print("Input callback")
		log(msg.data)
		self.step = self.step + 1
		if msg.data=="Timeout":
			#self.pub.publish('Task over')
			log('Task timeout')
			rospy.signal_shutdown('aa')
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
		print("Checking for success")
		if task.cond_end():
			print("Sim wrapper shutdown")
			self.pub.publish('Task over')
			log('Task ok')
			log_succ()
			rospy.signal_shutdown('aa')
			sys.exit()

success_prob = 0.9
def grasp_object(obj):
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(list(objects.keys())))
	elif robot1.location != objects[obj].location:
		print(objects[obj].location)
		print(robot1.location)
		raise Exception('Robot and objects in different locations')
	elif robot1.held_obj == obj:
		return
	elif robot1.held_obj != None:
		raise Exception('Gripper already full')
	else:
		if np.random.uniform() <= success_prob:
			robot1.held_obj = objects[obj]
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
	else:
		robot1.held_obj = None
		objects[obj].location = target
		grasp_part = None
		
def move_robot_to(target):
	if target not in locations:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
	else:
		robot1.location = target
		
def move_arm_to(pos):
	robot1.move_to(pos[0], pos[1], pos[2])
				
def rotate_end_effector(angle):
	if robot1.held_obj != None and angle >= np.pi/2:
		robot1.held_obj.toggle()
		
def in_gripper(obj):
	if obj in objects:
		return(robot1.held_obj == objects[obj])
	else:
		raise NameError('Invalid object. Valid objects are: '+str(list(objects.keys())))
	
def robot_at(location):
	if location in locations:
		return(robot1.location == location)
	else:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
		
def object_at(obj, location):
	if obj not in objects:
		raise Exception('Invalid object. Valid objects are: '+str(list(objects.keys())))
	elif location not in locations:
		raise Exception('Invalid location. Valid locations are: '+str(locations))
	else:
		return(objects[obj].location == location)
		
def get_position(obj):
	print(obj)
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
	global fridge_open
	global cabinet_open
	global trash_open
	if target in locations:
		if robot1.location != target:
			raise Exception('Robot needs to be next to the object to open it.')
		else:
			if target == 'Fridge':
				fridge_open = True
			elif target == 'TrashCan':
				trash_open = True
			elif target == 'Cabinet':
				cabinet_open = True
	elif target in objects:
		if objects[target].location != robot1.location:
			raise Exception('Robot needs to be next to the object to open it.')
			
def close_obj(target):
	if target in locations:
		if robot1.location != target:
			raise Exception('Robot needs to be next to the object to close it.')
	elif target in objects:
		if objects[target].location != robot1.location:
			raise Exception('Robot needs to be next to the object to close it.')


fridge_open = False
cabinet_open = False
trash_open = False

robot1 = robot('TiaGO')
robots = [robot1]


def main(args=None):
    print("Sim ok")
    i = int(args[0])
    
    with open("task_list.pkl", "rb") as f:
        tasks = pickle.load(f)

    global task
    task = tasks[i]
    
    global objects
    objects = task.objs()
    
    global locations
    locations = task.locs()
    
    sim = simulation(robots)
    sim.objects = objects

    task_loc = task_local(sim)

    rospy.init_node('simulation')
    print("OBJECTS: ",objects)

    rospy.spin()    


if __name__ == '__main__':
    main(sys.argv[1:])


