from OpenGL import GL as gl
import ctypes
import numpy as np

class Mesh:
    def __init__(self, vertices, indices):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

    def create(self):
        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            gl.GL_STATIC_DRAW,
        )

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            gl.GL_STATIC_DRAW,
        )
        gl.glVertexAttribPointer(
            0,  # attribute 0.
            3,  # components per vertex attribute
            gl.GL_FLOAT,  # type
            False,  # to be normalized?
            4 * 3 * 2,  # stride
            ctypes.c_void_p(0),  # array buffer offset
        )
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(
            1,  # attribute 1.
            3,  # components per vertex attribute
            gl.GL_FLOAT,  # type
            False,  # to be normalized?
            4 * 3 * 2,  # stride
            ctypes.c_void_p(4 * 3 * 1),  # array buffer offset
        )
        gl.glEnableVertexAttribArray(1)

    def bind(self):
        gl.glBindVertexArray(self.vao)

    def unbind(self):
        gl.glBindVertexArray(0)

    def draw(self):
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.indices),
            gl.GL_UNSIGNED_INT,
            None,
        )
        gl.glBindVertexArray(0)

    def destroy(self):
        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.vbo])
        gl.glDeleteBuffers(1, [self.ebo])


def get_cube_mesh():
    vertices = [
           # Positions        Normals  
        # Front face
        -0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    
         0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    
         0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    
        -0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    
        # Back face (z = -0.5)
        -0.5, -0.5, -0.5,    0.0,  0.0, -1.0,   
         0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    
         0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    
        -0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    
        # Left face (x = -0.5)
        -0.5, -0.5, -0.5,   -1.0,  0.0,  0.0,    
        -0.5, -0.5,  0.5,   -1.0,  0.0,  0.0,    
        -0.5,  0.5,  0.5,   -1.0,  0.0,  0.0,    
        -0.5,  0.5, -0.5,   -1.0,  0.0,  0.0,    
        # Right face (x = +0.5)
         0.5, -0.5, -0.5,    1.0,  0.0,  0.0,    
         0.5, -0.5,  0.5,    1.0,  0.0,  0.0,    
         0.5,  0.5,  0.5,    1.0,  0.0,  0.0,    
         0.5,  0.5, -0.5,    1.0,  0.0,  0.0,   
        # Top face (y = +0.5)
        -0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    
         0.5,  0.5,  0.5,    0.0,  1.0,  0.0,   
         0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    
        -0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    
        # Bottom face (y = -0.5)
        -0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    
         0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    
         0.5, -0.5, -0.5,    0.0, -1.0,  0.0,   
        -0.5, -0.5, -0.5,    0.0, -1.0,  0.0,   
    ]

    indices = [
        0, 1, 2, 2, 3, 0,       # Front
        4, 5, 6, 6, 7, 4,       # Back
        8, 9,10,10,11, 8,       # Left
       12,13,14,14,15,12,       # Right
       16,17,18,18,19,16,       # Top
       20,21,22,22,23,20        # Bottom
    ]

    mesh = Mesh(vertices=vertices, indices=indices)
    mesh.create()
    return mesh
