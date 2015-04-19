from OpenGL.GL import *
import OpenGL.GLU as GLU
"""
OpenGL utility functions
"""


def create_vertex_array():
    """
    create a vertex array, and initialize its attributes
    """
    vertex_array_id = glGenVertexArrays(1)
    check_for_errors()
    return vertex_array_id


def enable_vertex_attributes(count):
    for i in range(0, count):
        glEnableVertexAttribArray(i)




def check_for_errors():
    """
    look for opengl errors.  list the first 10 errors, then throw an exception
    """
    error_id = glGetError()
    # Only print the first 10 errors
    error_count = 0
    for error_count in range(0, 10):
        if error_id == GL_NO_ERROR:
            break
        print("OpenGL exception "+error_id+": "+GLU.gluErrorString(error_id))
        error_id = glGetError()
    if error_count > 0:
        raise Exception("OpenGL error has occurred.")
