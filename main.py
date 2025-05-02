import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import time
from pyglm import glm


from model import *
from mesh import *
from camera import *


def readGlslFile(filename):
    with open(filename, "r") as file:
        return file.read()


vertex_src = readGlslFile("shaders/shader.vert")
fragment_src = readGlslFile("shaders/shader.frag")

last_frame = 0.0


WIDTH = 800
HEIGHT = 600

lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
mouse_active = False


def handle_resize(window, w, h):
    global WIDTH, HEIGHT
    WIDTH = w
    HEIGHT = h
    # Set the viewport to the new window size
    glViewport(0, 0, w, h)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)
# set the callback function for window resize
glfw.set_window_size_callback(window, handle_resize)
# make the context current
glfw.make_context_current(window)

model = Model(
    pos=[0, -3, -5],
    rot=[0, glm.radians(90.0), 0],
    scale=[0.1, 0.1, 0.1],
    color=[0.0, 0.0, 1.0],
)

#model.add_mesh(get_cube_mesh())
model.load_gltf("models/astronaut/scene.gltf")

shader = compileProgram(
    compileShader(vertex_src, GL_VERTEX_SHADER),
    compileShader(fragment_src, GL_FRAGMENT_SHADER),
)

# set camera
camera = Camera(
    position=[0, 0, 3],
    yaw=-90.0,
    pitch=0.0,
    speed=4.5,
    sensitivity=0.1,
)


def mouse_callback(window, xpos, ypos):
    # Get the current mouse position
    global lastX, lastY

    if mouse_active:
        if first_mouse:
            lastX = xpos
            lastY = ypos

        xoffset = xpos - lastX
        yoffset = lastY - ypos

        lastX = xpos
        lastY = ypos
        # Process mouse movement
        camera.process_mouse_movement(xoffset=xoffset, yoffset=yoffset)


def mouse_enter_clb(window, entered):
    global first_mouse

    if entered:
        first_mouse = False
    else:
        first_mouse = True


def toggle_mouse():
    global mouse_active
    if mouse_active:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        mouse_active = False
    else:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        mouse_active = True


def keyboard_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_M and action == glfw.PRESS:
        toggle_mouse()


# Set the mouse callback function
glfw.set_cursor_enter_callback(window, mouse_enter_clb)
glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_key_callback(window, keyboard_callback)


def delta_time():
    global last_frame
    current_frame = time.time()
    delta_time = current_frame - last_frame
    last_frame = current_frame
    return delta_time


def update():
    # camera.update_view_matrix()
    projection = glm.perspective(
        glm.radians(45),
        WIDTH / HEIGHT,
        0.1,
        100,
    )
    glUniformMatrix4fv(
        glGetUniformLocation(shader, "u_projection"),
        1,
        GL_FALSE,
        glm.value_ptr(projection),
    )

    # view = glm.lookAt(glm.vec3(camera.position), glm.vec3(0, 0, 1), glm.vec3(0, 1, 0))
    view = camera.get_view_matrix()
    glUniformMatrix4fv(
        glGetUniformLocation(shader, "u_view"),
        1,
        GL_FALSE,
        glm.value_ptr(view),
    )
    glUniform3f(
        glGetUniformLocation(shader, "view_position"),
        camera.position[0],
        camera.position[1],
        camera.position[2],
    )
    glUniform3f(glGetUniformLocation(shader, "light_position"), 0.0, 10.0, 3.0)
    glUniform3f(glGetUniformLocation(shader, "light_color"), 1.0, 1.0, 1.0)


glEnable(GL_DEPTH_TEST)
glUseProgram(shader)
glClearColor(0.0, 1.1, 0.1, 1)

# the main application loop
while not glfw.window_should_close(window):
    delta = delta_time()
    glfw.poll_events()

    # process mouse movement
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard("FORWARD", delta)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard("BACKWARD", delta)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard("LEFT", delta)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard("RIGHT", delta)

    update()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw the cube
    model.draw(shader)

    glfw.swap_buffers(window)

# delete the shader program
glDeleteProgram(shader)
# delete the mesh
model.destroy()
# delete the window
glfw.destroy_window(window)
# terminate glfw, free up allocated resources
glfw.terminate()
