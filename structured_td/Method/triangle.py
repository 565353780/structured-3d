import pymesh
import numpy as np

def triangulate(points):
    """ triangulate the plane for operation and visualization
    """

    num_points = len(points)
    indices = np.arange(num_points, dtype=int)
    segments = np.vstack((indices, np.roll(indices, -1))).T

    tri = pymesh.triangle()
    tri.points = np.array(points)

    tri.segments = segments
    tri.verbosity = 0
    tri.run()

    return tri.mesh
