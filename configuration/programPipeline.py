import program
"""
program pipelines
"""


def get_square_pipeline(window):
    """
    renders a square
    """
    return [
        program.SimpleMatricesSetupProgram(window),
        program.SimpleRenderingProgram(window)
    ]


def get_cylinder_pipeline(window):
    """
    renders a cylinder
    """
    return [
        program.SimpleMatricesSetupProgram(window),
        program.VectorCylinderProgram(window)
    ]
