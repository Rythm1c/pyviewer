# PYTHON CAPSTONE PROJECT

3D viewer using opengl rendering API

## set up(linux apt store)

- open terminal and run(windows and mac users are on their own):
```
sudo apt install g++ libglfw3-dev libglew-dev libgl-dev 
```

- create a python project and open in vscode(or editor of your choice)
- start a virtual environment
- install neccesary modules(pyglm, OpenGL, numpy, pygltflib, glfw)
- run main.py

## Usage

- W, A, S, D for camera movement 
- M to toggle camera rotation
open a default cube
download a gltf 3D file, uncomment line 67 and and update the models path with the downloaded one
comment out line 66 to stop rendering the cube

might add a ui to make all this user friendly, maybe not :)
