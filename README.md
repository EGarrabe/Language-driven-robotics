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
