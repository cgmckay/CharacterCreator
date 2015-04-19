from OpenGL.GL import *
import ctypes


class Shader():
    def __init__(self, filepaths):
        self.filepaths = filepaths
        self.shaderIDs = {}
        for shader_type in filepaths.keys():
            shader_id = glCreateShader(shader_type)
            self.shaderIDs[shader_type] = shader_id
            path = filepaths[shader_type]
            with open(path, 'r') as file:
                source = file.read()
                glShaderSource(GLhandle(shader_id), [source])

            glCompileShader(shader_id)
            status = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
            if status != GL_TRUE:
                shader_log = glGetShaderInfoLog(shader_id)
                raise Exception("Shader did not compile: " + str(shader_log))
