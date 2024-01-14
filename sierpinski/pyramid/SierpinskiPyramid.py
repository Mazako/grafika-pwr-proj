from OpenGL.GL import *

from sierpinski.engine.Texture import Texture
from sierpinski.engine.Uniform import Uniform
from sierpinski.engine.Variable import Variable
from sierpinski.utils.Translations import *


class SierpinskiPyramid:
    def __init__(self, program_id, draw_type, vertices, colors, normals,
                 uvs, texture_id,
                 translation=(0, 0, 0),
                 rotation=Rotation(1, pygame.Vector3(0, 1, 0))):
        self.draw_type = draw_type
        self.program_id = program_id
        self.vertices = vertices
        self.colors = colors
        self.normals = normals
        self.uvs = uvs
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        Variable(program_id, 'vec3', self.vertices, 'pos').load()
        Variable(program_id, 'vec3', self.colors, 'inColor').load()
        Variable(program_id, 'vec3', self.normals, 'inNormal').load()
        Variable(program_id, 'vec2', self.uvs, 'inUv').load()

        self.rotation = rotation
        self.translation = translation

        self.transformation_matrix = identity_matrix()
        self.transformation_matrix = translate(self.transformation_matrix, translation[0], translation[1], translation[2])
        self.transformation = Uniform(program_id, 'mat4', self.transformation_matrix, 'model_matrix')
        self.texture = Uniform(self.program_id, 'sampler2D', [texture_id, 1], 'tex')

    def draw(self):
        self.texture.load()
        self.transformation_matrix = rotate(self.transformation_matrix, self.rotation.angle, self.rotation.axis)
        self.transformation = Uniform(self.program_id, 'mat4', self.transformation_matrix, 'model_matrix').load()
        glBindVertexArray(self.vao)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
