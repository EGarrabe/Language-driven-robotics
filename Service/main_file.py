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

tasks_reformulated_1 = [
    "Move the WaterGlass to the Kitchen table. It is currently on the Table.",
    "Pick up the Cupcake from the Bathroom counter and place it on the Table.",
    "Transfer the Pliers to the Coffee table. They are on the Table.",
    "Set the Mouse down on the Table. It is on the Desk.",
    "Relocate the Cupcake to the Desk. It is now on the Table.",
    "Move the Pie onto the Table. It is currently on the Bathroom counter.",
    "Take the Sponge and place it on the Kitchen table. It is now on the Coffee table.",
    "Pick up the Knife from the Table and put it on the Kitchen counter.",
    "Carry the Knife to the Coffee table. It is on the Kitchen counter.",
    "Retrieve the Knife from the Desk and place it on the Kitchen table.",
    "Pick up the Screwdriver from the Table and place it on the Kitchen table.",
    "Move the Mug onto the Kitchen counter. It is on the Table.",
    "Carry the Screwdriver to the Coffee table. It is on the Bathroom counter.",
    "Relocate the WaterGlass to the Bathroom counter. It is now on the Kitchen counter.",
    "Put the Knife onto the Coffee table. It is currently on the Desk.",
    "Place the Fork on the Kitchen table. It is now on the Coffee table.",
    "Move the Fork to the Desk. It is on the Kitchen table.",
    "Transfer the Plate to the Kitchen counter. It is on the Table.",
    "Pick up the Mug from the Bathroom counter and place it on the Coffee table.",
    "Set the Keyboard on the Bathroom counter. It is currently on the Table.",
    "Take the Bottle from the Table and place it on the Kitchen counter.",
    "Pick up the Screwdriver from the Desk and put it on the Coffee table.",
    "Place the Pliers on the Desk. They are currently on the Kitchen counter.",
    "Move the Fork onto the Table. It is on the Desk.",
    "Pick up the WineGlass and put it on the Kitchen table. It is on the Desk.",
    "Carry the Peach to the Bathroom counter. It is currently on the Table.",
    "Set the WaterGlass on the Kitchen table. It is currently on the Table.",
    "Move the Pie to the Bathroom counter. It is on the Table.",
    "Transfer the Knife to the Desk. It is on the Coffee table.",
    "Place the Mug on the Desk. It is on the Coffee table.",
    "Pick up the Cupcake and put it on the Bathroom counter. It is on the Table.",
    "Move the Fork to the Kitchen counter. It is currently on the Bathroom counter.",
    "Take the Pie from the Kitchen counter and place it on the Bathroom counter.",
    "Pick up the Pills and set them on the Kitchen counter. They are on the Desk.",
    "Move the Pie to the Coffee table. It is currently on the Bathroom counter.",
    "Transfer the Pliers to the Kitchen counter. They are on the Table.",
    "Pick up the Keyboard from the Bathroom counter and place it on the Coffee table.",
    "Retrieve the Knife from the Coffee table and place it on the Desk.",
    "Place the Pie on the Kitchen table. It is now on the Bathroom counter.",
    "Bring the Soap to the Coffee table. It is currently on the Kitchen table.",
    "Move the WineGlass to the Kitchen table. It is on the Desk.",
    "Pick up the Keyboard from the Bathroom counter and put it on the Kitchen counter.",
    "Take the Cupcake from the Bathroom counter and bring it to the Table.",
    "Pick up the Pie and place it on the Desk. It is on the Coffee table.",
    "Carry the Plate to the Kitchen counter. It is currently on the Coffee table.",
    "Move the Bottle to the Coffee table. It is on the Table.",
    "Pick up the Fork from the Coffee table and bring it to the Desk.",
    "Transport the Soap to the Table. It is now on the Bathroom counter.",
    "Put the Soap onto the Kitchen table. It is currently on the Coffee table.",
    "Move the Plate to the Coffee table. It is now on the Desk."
]

tasks_reformulated_2 = [
    "Take the WaterGlass from the Table and move it to the Kitchen table.",
    "Fetch the Cupcake from the Bathroom counter and set it on the Table.",
    "Place the Pliers on the Coffee table. They are currently on the Table.",
    "Move the Mouse to the Table. It is on the Desk.",
    "Set the Cupcake down on the Desk. It is now on the Table.",
    "Relocate the Pie onto the Table. It is on the Bathroom counter.",
    "Transport the Sponge to the Kitchen table. It is now on the Coffee table.",
    "Grab the Knife from the Table and place it on the Kitchen counter.",
    "Move the Knife to the Coffee table. It is currently on the Kitchen counter.",
    "Transfer the Knife from the Desk to the Kitchen table.",
    "Move the Screwdriver from the Table to the Kitchen table.",
    "Set the Mug down on the Kitchen counter. It is on the Table.",
    "Bring the Screwdriver to the Coffee table. It is now on the Bathroom counter.",
    "Take the WaterGlass from the Kitchen counter and put it on the Bathroom counter.",
    "Place the Knife onto the Coffee table. It is now on the Desk.",
    "Move the Fork to the Kitchen table. It is on the Coffee table.",
    "Transport the Fork to the Desk. It is now on the Kitchen table.",
    "Relocate the Plate onto the Kitchen counter. It is currently on the Table.",
    "Pick up the Mug from the Bathroom counter and put it on the Coffee table.",
    "Place the Keyboard on the Bathroom counter. It is on the Table.",
    "Move the Bottle from the Table to the Kitchen counter.",
    "Set the Screwdriver down on the Coffee table. It is now on the Desk.",
    "Move the Pliers to the Desk. They are currently on the Kitchen counter.",
    "Put the Fork onto the Table. It is now on the Desk.",
    "Take the WineGlass and set it on the Kitchen table. It is on the Desk.",
    "Move the Peach from the Table to the Bathroom counter.",
    "Transfer the WaterGlass onto the Kitchen table. It is on the Table.",
    "Place the Pie on the Bathroom counter. It is currently on the Table.",
    "Move the Knife from the Coffee table to the Desk.",
    "Relocate the Mug to the Desk. It is on the Coffee table.",
    "Set the Cupcake onto the Bathroom counter. It is on the Table.",
    "Place the Fork on the Kitchen counter. It is on the Bathroom counter.",
    "Transfer the Pie from the Kitchen counter to the Bathroom counter.",
    "Move the Pills from the Desk to the Kitchen counter.",
    "Pick up the Pie and bring it to the Coffee table. It is on the Bathroom counter.",
    "Take the Pliers from the Table and set them on the Kitchen counter.",
    "Transport the Keyboard to the Coffee table. It is now on the Bathroom counter.",
    "Place the Knife onto the Desk. It is currently on the Coffee table.",
    "Move the Pie to the Kitchen table. It is on the Bathroom counter.",
    "Relocate the Soap to the Coffee table. It is currently on the Kitchen table.",
    "Transport the WineGlass to the Kitchen table. It is on the Desk.",
    "Move the Keyboard from the Bathroom counter to the Kitchen counter.",
    "Carry the Cupcake to the Table. It is on the Bathroom counter.",
    "Move the Pie to the Desk. It is on the Coffee table.",
    "Place the Plate onto the Kitchen counter. It is on the Coffee table.",
    "Set the Bottle down on the Coffee table. It is on the Table.",
    "Pick up the Fork from the Coffee table and move it to the Desk.",
    "Bring the Soap to the Table. It is now on the Bathroom counter.",
    "Relocate the Soap to the Kitchen table. It is currently on the Coffee table.",
    "Move the Plate from the Desk to the Coffee table."
]


if __name__ == '__main__':
    #with open("task_list.pkl", "rb") as f:
    #    tasks = pickle.load(f)
    #for i in range(50):
    #    tasks[i].prompt = tasks_reformulated_2[i]
    #with open("task_list.pkl", "wb") as f:
    #    pickle.dump(tasks, f)
    for i in range(3): #TODO adapt sim wrapper and publisher to match orchestrator
        print(f'python3 LLM_planner.py {i} & python3 orchestrator.py {i} & python3 sim_wrapper.py {i} & python3 pub_task.py {i} & wait')
        subprocess.run(f'python3 LLM_planner.py {i} & python3 orchestrator.py {i} & python3 sim_wrapper.py {i} & python3 pub_task.py {i} & wait', shell = True, executable="/bin/bash")
        #subprocess.run(f'python3 orchestrator.py {i} & wait', shell = True, executable="/bin/bash")
