### Dependancies and installation
This code depends on Ollama (with llama3.1 or Deepseek r1-7b). An adapted version of the _sim\_wrapper_ was used for rendering, based on the VirtualHome simulator. 

### How to run this code
The main file is used to generate tasks. Alternate task instructions, generated with GPT, are provided in the same file.\\
As the communication system is based on ROS1, running Roscore in a terminal window is also needed. We provide different versions of the orchestrator, matching the ablated variants of our pipeline.
