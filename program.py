from abc import ABCMeta, abstractmethod
import logging

import glfw
import numpy
import vispy.util.transforms as transform
from OpenGL.GL import *

import shader as shader_class
from configuration import shaders
import openglUtils

logging.basicConfig()


class Program(metaclass=ABCMeta):
    """
     A program is a process run with some other programs sequentially.
     This is referred to as the program pipeline.  The end result of
     a program pipeline is typically rendering to a window, but
     program is fairly generic, so that is not always the case.

     Programs pass information to each other with a dict
     called program_data.  program_data is initialized at the start
     of the pipeline, and is provided to each program in the run method.
     Programs add or update entries to send information to programs later in the pipeline.
     Programs read entries to receive information from earlier in the pipeline.
    """
    def __init__(self):
        self.name = "Default"
        self.required_data = []

    def validate(self, program_data):
        for data in self.required_data:
            if data not in program_data:
                raise Exception("Required data "+data+"was not included in program data of "+self.name)

    @abstractmethod
    def run(self, program_data):
        pass


class OpenGLProgram(Program, metaclass=ABCMeta):
    """
    A program type used to run an opengl program
    """
    def __init__(self, window, shader, uniforms, positions):
        super().__init__()
        self.shader = shader
        self.window = window
        self.uniforms = uniforms
        self.positions = positions
        program_id = glCreateProgram()
        self.program_id = program_id
        self.link_with_shaders()
        glUseProgram(program_id)
        self.vertex_array_id = openglUtils.create_vertex_array()
        self.vertex_buffer_id = glGenBuffers(1)
        self.start_program()
        self.init_buffer()
        self.init_attributes()
        self.init_uniforms()
        self.stop_program()

    def init_buffer(self):
        glBufferData(GL_ARRAY_BUFFER, self.positions, GL_DYNAMIC_DRAW)

    # def setup_buffer(self):
    #    glBufferData(GL_ARRAY_BUFFER, self.positions, GL_DYNAMIC_DRAW)

    def link_with_shaders(self):
        program_id = self.program_id
        shader_ids = self.shader.shaderIDs.values()
        for shader_id in shader_ids:
            glAttachShader(program_id, shader_id)

        glLinkProgram(program_id)

        for shader_id in shader_ids:
            glDetachShader(program_id, shader_id)

        for shader_id in shader_ids:
            glDeleteShader(shader_id)

        status = glGetProgramiv(program_id, GL_LINK_STATUS)
        if status == GL_FALSE:
            log = glGetProgramInfoLog(program_id)
            raise Exception("Could not link shaders to program" + log)
        openglUtils.check_for_errors()

    def init_uniforms(self):
        for uniform_name in self.uniforms.keys():
            self.uniforms[uniform_name] = glGetUniformLocation(self.program_id, uniform_name)

    @staticmethod
    def stop_program():
        glUseProgram(0)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def start_program(self):
        glUseProgram(self.program_id)
        glBindVertexArray(self.vertex_array_id)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)

    @abstractmethod
    def init_attributes(self):
        pass

    @abstractmethod
    def run(self, program_data):
        pass

    @abstractmethod
    def setup_uniforms(self, program_data):
        pass


class SimpleMatricesSetupProgram(Program):
    """
    Program type used to set up the matrices used in SimpleRenderingProgram
    """
    def __init__(self, window):
        super().__init__()
        self.position = [0, 0, -5]
        self.positional_velocity = [.05, .05, .05]
        self.rotation = [0, 0, 0]
        self.rotational_velocity = [.9, .9, .9]
        self.name = "SimpleMatricesSetup"
        self.window = window

    def run(self, program_data):
        input = program_data["input"]
        # program_data["projectionMatrix"] = transform.ortho(-10, 10, -10, 10, .01, 50)
        program_data["projectionMatrix"] = transform.perspective(45.0, self.window.width/self.window.height, 0.1, 70.0)
        if input.keyCounter[glfw.KEY_ESCAPE] != 0:
            glfw.set_window_should_close(self, True)

        modelview_matrix = numpy.eye(4, dtype=numpy.float32)
        self.rotation[0] += self.rotational_velocity[0] * (input.keyDown[glfw.KEY_J] - input.keyDown[glfw.KEY_L])
        self.rotation[1] += self.rotational_velocity[1] * (input.keyDown[glfw.KEY_I] - input.keyDown[glfw.KEY_K])
        self.rotation[2] += self.rotational_velocity[2] * (input.keyDown[glfw.KEY_O] - input.keyDown[glfw.KEY_U])
        transform.rotate(modelview_matrix, self.rotation[0], 1, 0, 0)
        transform.rotate(modelview_matrix, self.rotation[1], 0, 1, 0)
        transform.rotate(modelview_matrix, self.rotation[2], 0, 0, 1)
        self.position[0] += self.positional_velocity[0] * (input.keyDown[glfw.KEY_D] - input.keyDown[glfw.KEY_A])
        self.position[1] += self.positional_velocity[1] * (input.keyDown[glfw.KEY_W] - input.keyDown[glfw.KEY_S])
        self.position[2] += self.positional_velocity[2] * (input.keyDown[glfw.KEY_E] - input.keyDown[glfw.KEY_Q])
        transform.translate(modelview_matrix, self.position[0], self.position[1], self.position[2])

        program_data["modelviewMatrix"] = modelview_matrix


class SimpleRenderingProgram(OpenGLProgram):
    """
    Simple opengl program to draw a square
    """
    def init_attributes(self):
        openglUtils.enable_vertex_attributes(1)

        offset = ctypes.c_void_p(0)
        stride = self.positions.strides[0]
        glVertexAttribPointer(0, 3, GL_FLOAT, False, stride, offset)

    def __init__(self, window):
        shader = shader_class.Shader(shaders.simpleShader)
        uniforms = {'mvpMatrix': -1}
        positions = numpy.array([
            # a square
            (1,  1, 0),
            (1, -1, 0),
            (-1,  1, 0),
            (-1, -1, 0)
        ], numpy.float32)
        super().__init__(window, shader, uniforms, positions)
        self.required_data = ['modelviewMatrix', 'projectionMatrix']
        self.name = "SimpleRendering"

    def setup_uniforms(self, program_data):
        mvp_matrix = program_data['modelviewMatrix'].dot(program_data['projectionMatrix'])
        glUniformMatrix4fv(self.uniforms['mvpMatrix'], 1, False, mvp_matrix)

    def run(self, program_data):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(.1, .36, .36, 1)
        self.start_program()
        self.setup_uniforms(program_data)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        openglUtils.check_for_errors()
        self.stop_program()


class VectorCylinderProgram(OpenGLProgram):
    def __init__(self, window):
        shader = shader_class.Shader(shaders.cylinderShader)
        uniforms = {'mvpMatrix': -1}
        positions = numpy.array([
            # a line
            (1,  0, 0),
            (-1, 0, 0),
        ], numpy.float32)
        super().__init__(window, shader, uniforms, positions)
        self.required_data = ['modelviewMatrix', 'projectionMatrix']
        self.name = "SimpleRendering"

    def run(self, program_data):
        """
        Display a cylinder, distorted using two bezier points
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(.1, .36, .36, 1)
        self.start_program()
        self.setup_uniforms(program_data)
        glDrawArrays(GL_LINE_STRIP, 0, 2)
        openglUtils.check_for_errors()
        self.stop_program()

    def init_attributes(self):
        openglUtils.enable_vertex_attributes(1)

        offset = ctypes.c_void_p(0)
        stride = self.positions.strides[0]
        glVertexAttribPointer(0, 3, GL_FLOAT, False, stride, offset)

    def setup_uniforms(self, program_data):
        mvp_matrix = program_data['modelviewMatrix'].dot(program_data['projectionMatrix'])
        glUniformMatrix4fv(self.uniforms['mvpMatrix'], 1, False, mvp_matrix)
