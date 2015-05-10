from OpenGL.GL import *
"""
Environment specific properties, such as paths
"""
simpleShader = {GL_FRAGMENT_SHADER: "shaders\\simple\\simple.frag",
                GL_VERTEX_SHADER: "shaders\\simple\\simple.vert"}
cylinderShader = {GL_FRAGMENT_SHADER: "shaders\\cylinder\\cylinder.frag",
                  GL_GEOMETRY_SHADER: "shaders\\cylinder\\cylinder.geom",
                  GL_VERTEX_SHADER: "shaders\\cylinder\\cylinder.vert"}

