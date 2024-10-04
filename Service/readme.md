### Dependancies and installation
This code needs the VirtualHome simulator and ollama (with llama3.1) to be used. Our module files can be anywhere, while the sim-wrapper middleware needs to be in the virtualHome directory that is the parent of the directory where virtualHome's executable is located.

### How to run this code
Before starting the experiment, select the task statement (in the _pub\_task.py_ file), the available objects and locations (in _init\_prompt.py_) and the matching object and location lists (in _sim\_wrapper.py_).\\
Then, in a terminal, run roscore, the planner and one of the orchestrator files (we provide four versions, corresponding to the modalities of our ablation study). Then, start the simulation wrapper and the virtualHome executable. When the executable is started (after a few seconds), the task_poblisher can be used, starting the experiment.
