from OpenGL.GL import *

class Uniform:
    def __init__(self, program_id, data_type, data, variable_name):
        self.program_id = program_id
        self.data_type = data_type
        self.data = data
        self.uniform_id = glGetUniformLocation(program_id, variable_name)

    def load(self):
        if self.data_type == 'vec3':
            glUniform3f(self.uniform_id, self.data[0], self.data[1], self.data[2])
        elif self.data_type == 'mat4':
            glUniformMatrix4fv(self.uniform_id, 1, GL_TRUE, self.data)
        elif self.data_type == 'sampler2D':
            obj, unit = self.data
            glActiveTexture(GL_TEXTURE0 + unit)
            glBindTexture(GL_TEXTURE_2D, obj)
            glUniform1i(self.uniform_id, unit)
        elif self.data_type == 'bool':
            glUniform1i(self.uniform_id, self.data)
