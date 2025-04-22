import numpy as np
import pickle
#import rclpy
import rospy
import sys
import random
import subprocess

from std_msgs.msg import String

import time

import pickle

import copy

Ntasks = 50

class sobject:
	def __init__(self, name, location='Table', pos = [0,0,0]):
		self.name = name
		self.toggled = False
		self.pos = pos
	def get_position(self):
		return(self.pos)
	def toggle(self):
		self.toggled = True

class task_simple:
    def __init__(self, obj, start, end):
        self.obj = obj
        self.obj.location = start
        self.start = start
        self.end = end
        self.prompt = self.statement()
    def statement(self):
        i = np.random.choice([1,2,3])
        if i == 1:
            return(f"Put the {self.obj.name} on the {locations_dict[self.end]}. The {self.obj.name} is on the {locations_dict[self.start]}")
        elif i == 2:
            return(f"Take the {self.obj.name} and put it on the {locations_dict[self.end]}. The {self.obj.name} is on the {locations_dict[self.start]}")
        elif i == 3:
            return(f"Bring the {self.obj.name} to the {locations_dict[self.end]}. The {self.obj.name} is on the {locations_dict[self.start]}")
    def cond_end(self):
        return(self.obj.location == self.end)
    def env(self):
        return(f"""The current environment:
The objects are: ['{self.obj.name}']
The locations are: ['{self.start}','{self.end}']
The {self.obj.name} is on the {self.start}. The robot is at the {self.end}. The gripper is empty.""")
    def objs(self):
        return({self.obj.name:self.obj})
    def locs(self):
        return([self.start, self.end])
        
glass = sobject('WaterGlass', location='KitchenTable')
plate = sobject('Plate')
fork = sobject('Fork', location='Cupboard')
knife = sobject('Knife', location='Cupboard')
pie = sobject('Pie', location='KitchenTable')
mug = sobject('Mug', location = 'Desk')
cupcake = sobject('Cupcake', location = 'Desk')
mouse = sobject('Mouse', location = 'Desk')
keyboard = sobject('Keyboard', location = 'Desk')
pliers = sobject('Pliers', location='Desk')
screwdriver = sobject('Screwdriver', location='Desk')
bottle = sobject('Bottle', location='Desk')
pills = sobject('Pills', location='BathroomCounter')
peach = sobject('Peach', location='CoffeeTable')
wineglass = sobject('WineGlass', location='Table')
soap = sobject('Soap', location='KitchenCounter')
sponge = sobject('Sponge', location='KitchenCounter')
objects = [glass,plate,fork,knife,pie,mug,cupcake,mouse,keyboard,pliers,screwdriver,bottle,pills,peach,wineglass,soap,sponge]
locations_main = ['Table', 'Desk', 'KitchenCounter', 'BathroomCounter', 'CoffeeTable', 'KitchenTable']
locations_full = ['Table', 'Desk', 'Kitchen counter', 'Bathroom counter', 'Coffee table', 'Kitchen table']

locations_dict = {'Table': 'Table', 'Desk': 'Desk', 'KitchenCounter': 'Kitchen counter', 'BathroomCounter': 'Bathroom counter', 'CoffeeTable': 'Coffee table', 'KitchenTable': 'Kitchen table'}



if __name__ == '__main__':
    for i in range(9,10): #TODO adapt sim wrapper and publisher to match orchestrator
        print(f'python3 taskboard_planner.py & python3 orchestrator_taskboard.py & python3 taskboard_sim.py & python3 pub_task_taskboard.py {i} & wait')
        subprocess.run(f'python3 taskboard_planner.py & python3 orchestrator_taskboard_feedback.py & python3 taskboard_sim.py & python3 pub_task_taskboard.py {i} & wait', shell = True, executable="/bin/bash")
        #subprocess.run(f'python3 orchestrator.py {i} & wait', shell = True, executable="/bin/bash")
