from OpenGL import GL as gl
from pyglm import glm
import numpy as np
from mesh import Mesh
from pygltflib import GLTF2
import os, base64


class Model:
    def __init__(self, pos, rot, scale, color=(1.0, 1.0, 1.0)):
        self.meshes = []
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.color = color
        self.model_matrix = glm.mat4()
        self.update_model_matrix()

    def add_mesh(self, mesh):
        self.meshes.append(mesh)

    def update_model_matrix(self):
        self.model_matrix = glm.translate(glm.mat4(), self.pos)
        self.model_matrix = glm.rotate(
            self.model_matrix, self.rot[0], glm.vec3(1, 0, 0)
        )
        self.model_matrix = glm.rotate(
            self.model_matrix, self.rot[1], glm.vec3(0, 1, 0)
        )
        self.model_matrix = glm.rotate(
            self.model_matrix, self.rot[2], glm.vec3(0, 0, 1)
        )
        self.model_matrix = glm.scale(self.model_matrix, self.scale)

    def draw(self, shader):
        for mesh in self.meshes:
            gl.glUniformMatrix4fv(
                gl.glGetUniformLocation(shader, "u_model"),
                1,
                gl.GL_FALSE,
                glm.value_ptr(self.model_matrix),
            )
            gl.glUniform3f(
                gl.glGetUniformLocation(shader, "input_color"),
                self.color[0],
                self.color[1],
                self.color[2],
            )
            mesh.draw()
            mesh.unbind()

    def set_position(self, pos):
        self.pos = pos
        self.update_model_matrix()

    def set_rotation(self, rot):
        self.rot = rot
        self.update_model_matrix()

    def set_scale(self, scale):
        self.scale = scale
        self.update_model_matrix()

    def destroy(self):
        for mesh in self.meshes:
            mesh.destroy()
        self.meshes = []

    def load_gltf(self, filepath):
        gltf = GLTF2().load(filepath)

        # Figure out base directory for external files
        base_dir = os.path.dirname(filepath)

        # Load binary buffer
        buffer = gltf.buffers[0]
        if buffer.uri.startswith("data:"):
            # Embedded base64 buffer
            encoded = buffer.uri.split(",")[1]
            buffer_data = base64.b64decode(encoded)
        else:
            # External .bin file
            bin_path = os.path.join(base_dir, buffer.uri)
            with open(bin_path, "rb") as f:
                buffer_data = f.read()

        # Get first mesh

        def get_textures(gltf):
            textures = []
            for image in gltf.images:
                if image.uri.startswith("data:"):
                    # Embedded base64 image
                    encoded = image.uri.split(",")[1]
                    image_data = base64.b64decode(encoded)
                else:
                    # External image file
                    img_path = os.path.join(base_dir, image.uri)
                    with open(img_path, "rb") as f:
                        image_data = f.read()
                textures.append(image_data)
            return textures

        texures = get_textures(gltf)

        for mesh in gltf.meshes:
            """primitive = gltf.meshes[0].primitives[0]"""

            for primitive in mesh.primitives:

                def read_accessor(accessor_idx):
                    accessor = gltf.accessors[accessor_idx]
                    bufferView = gltf.bufferViews[accessor.bufferView]
                    byteOffset = (bufferView.byteOffset or 0) + (
                        accessor.byteOffset or 0
                    )
                    count = accessor.count

                    componentType = accessor.componentType
                    if componentType == 5123:
                        dtype = np.uint16
                        component_size = 2
                    elif componentType == 5125:
                        dtype = np.uint32
                        component_size = 4
                    elif componentType == 5126:
                        dtype = np.float32
                        component_size = 4
                    else:
                        raise Exception(f"Unsupported componentType {componentType}")

                    typeName = accessor.type
                    num_components = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[
                        typeName
                    ]

                    if bufferView.byteStride:  # data is interleaved
                        stride = bufferView.byteStride
                        array = []
                        for i in range(count):
                            offset = byteOffset + i * stride
                            element = np.frombuffer(
                                buffer_data,
                                dtype=dtype,
                                count=num_components,
                                offset=offset,
                            )
                            array.append(element)
                        return np.array(array)
                    else:  # tightly packed
                        total_count = count * num_components
                        array = np.frombuffer(
                            buffer_data,
                            dtype=dtype,
                            count=total_count,
                            offset=byteOffset,
                        )
                        array = array.reshape((count, num_components))
                        return array

                positions = read_accessor(primitive.attributes.POSITION)
                normals = read_accessor(primitive.attributes.NORMAL)
                indices = read_accessor(primitive.indices)

                vertex_data = (
                    np.hstack((positions, normals)).astype(np.float32).flatten()
                )

                mesh = Mesh(vertex_data, indices)
                mesh.create()
                self.add_mesh(mesh)
