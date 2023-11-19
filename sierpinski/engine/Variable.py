from OpenGL.GL import *
import numpy as np

class Variable:
    def __init__(self, program_id, data_type, data, variable_name):
        self.program_id = program_id
        self.data_type = data_type
        self.data = np.array(data, np.float32)
        self.variable_name = variable_name
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.ravel(), GL_STATIC_DRAW)

    def load(self):
        variable_id = glGetAttribLocation(self.program_id, self.variable_name)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        if self.data_type == 'vec3':
            glVertexAttribPointer(variable_id, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(variable_id)

