# Language-driven-robotics
This repo contains the code required to replicate the experiments from the paper _Enhancing Robustness in Language-Driven Robotics: A Modular Approach to Failure Reduction_ by Émiland Garrabé, Pierre Teixeira, Mahdi Khoramshahi, Stéphane Doncieux.

## Architecture components
The main components of our architecture are implemented as follows:

#### Planning and Expected outcomes module
The planning module receives the task statement by listening to the topic 'Task'. When this happens, the LLM is prompted to output a plan as a tuple of Python strings. When the plan is ready, the LLM is re-prompted (resetting the context), and outputs the expected outcomes of each step. Both the plan and expected outcomes are then published on separate topics.

#### Execution module
The execution module subscribes to the 'Task', 'Plan' and 'EO' (expected outcomes) topics. When all three have been published, the execution module starts interacting with the LLM by adding the first prompt and reply to the context. The first prompt contains the setting of the experiment, guidelines for code formatting, primitive headers and use examples, information about the environment and the task, plan and expected outcomes. The first reply uses a dud function (_begin()_) to provide an example of properly-formatted code to the LLM.\\
At each step, the context is completed with a short input containing the feedback from the previous step, the current plan and a reminder of the robot's position and of the object in its gripper. The LLM then outputs code for the step.

## Experiment implementation
### Requirements
VirtualHome (for the service setting) and ollama (with llama3.1) are required to replicate this work.

### Service setting
The service robot experiments are done in the [VirtualHome](virtual-home.org/) simulator. In VirtualHome, the robot is represented by a humanoid agent and evolves inside an appartment. 

#### Digital twin
In the digital twin, we provide lists of the known locations and objects for each task. Automatically exploring and memorizing the environment is the topic of future work. The motion primitives are coded as VirtualHome actions, see the [Documentation](http://virtual-home.org/documentation/master/get_started/get_started.html#key-concepts) for more details.

### Industrial setting
We inspire our industrial setting on the euROBIN Robothon taskboard., which is a manipulation benchmark inspired by eletronic recycling tasks. For these experiments, we use as skills a set of motion primitives developed prior to this work. For the moment, the code is provided for the reader's information, due to the hardware requirements for running the experiments.

#### Digital twin
Given the limited combinatorics of the task, and the difficulty of accurately simulating the taskboard, we design a simple digital twin that verifies wether a skill has been run before or not when appropriate. The motion primitives are ROS services that are called from the digital twin.
