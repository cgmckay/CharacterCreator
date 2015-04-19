import glfw
import logging
from input import Input
import program
import configuration.programPipeline as pipeline
import configuration.shaders as environment
from OpenGL.GL import *

logging.basicConfig()

# Makes a window via glfw and renders to it with Opengl
class Window:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise Exception("Invalid size "+width+","+height)
        self.width = width
        self.height = height
        glfw.set_error_callback(self.error_callback)
        if not glfw.init():
            raise Exception("GLFW couldn't initialize.")
        self.window = self.glfw_create_window(self.width, self.height, "Character Creator")
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window couldn't initialize.")
        glfw.make_context_current(self.window)
        self.input = Input()
        glfw.set_key_callback(self.window, self.input.key_callback)
        glfw.set_mouse_button_callback(self.window, self.input.mouse_button_callback)
        glfw.set_window_size_callback(self.window, self.window_size_callback)
        self.print_opengl_data()
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        self.pipeline = pipeline.get_cylinder_pipeline(self)

    def window_size_callback(self, window, width, height):
        logging.info("dimensions are now "+str(width)+", "+str(height))
        self.width = width
        self.height = height
        glViewport(0, 0, self.width, self.height)

    def run(self):
        program_data = {'input': self.input}
        while not glfw.window_should_close(self.window):
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            for program in self.pipeline:
                program.run(program_data)
        glfw.terminate()

    @staticmethod
    def glfw_create_window(width, height, window_name):
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
        return glfw.create_window(width, height, window_name, None, None)

    @staticmethod
    def print_opengl_data():
        print("OpenGL version: " + str(glGetString(GL_VERSION)))
        print("GLSL version: " + str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
        print("OpenGL Vendor: " + str(glGetString(GL_VENDOR)))
        print("Renderer: " + str(glGetString(GL_RENDERER)))

    @staticmethod
    def error_callback(code, description):
        raise Exception("GLFW Exception "+code+": "+description)

