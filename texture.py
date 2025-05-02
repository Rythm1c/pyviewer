import OpenGL.GL as gl
from PIL import Image


class Texture:
    def __init__(self, path):
        self.texture_id = gl.glGenTextures(1)
        self.path = path
        self.width = 0
        self.height = 0
        self.load_texture()

    def load_texture(self):
        image = Image.open(self.path)
        self.width, self.height = image.size
        image_data = image.convert("RGBA").tobytes()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            self.width,
            self.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            image_data,
        )
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    def bind(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
