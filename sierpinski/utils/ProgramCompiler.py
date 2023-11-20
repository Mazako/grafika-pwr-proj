from OpenGL.GL import *


def compile_shader(type, source):
    shader_id = glCreateShader(type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not success:
        glDeleteShader(shader_id)
        raise Exception('\n' + glGetShaderInfoLog(shader_id).decode('utf-8'))
    return shader_id


def create_program(vertex_shader_path, fragment_shader_path):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, open(vertex_shader_path).read())
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, open(fragment_shader_path).read())

    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)

    success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not success:
        raise RuntimeError(glGetProgramInfoLog(program_id))
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id
