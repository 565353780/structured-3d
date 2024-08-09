import pymesh
import numpy as np

from structured_td.Method.trans import project, project_inv
from structured_td.Method.triangle import triangulate

def convert_lines_to_vertices(lines):
    """convert line representation to polygon vertices
    """
    polygons = []
    lines = np.array(lines)

    polygon = None
    while len(lines) != 0:
        if polygon is None:
            polygon = lines[0].tolist()
            lines = np.delete(lines, 0, 0)

        lineID, juncID = np.where(lines == polygon[-1])
        vertex = lines[lineID[0], 1 - juncID[0]]
        lines = np.delete(lines, lineID, 0)

        if vertex in polygon:
            polygons.append(polygon)
            polygon = None
        else:
            polygon.append(vertex)

    return polygons

def clip_polygon(polygons, vertices_hole, junctions, meta):
    if len(polygons) == 1:
        junctions = [junctions[vertex] for vertex in polygons[0]]
        mesh_wall = triangulate(junctions)

        vertices = np.array(mesh_wall.vertices)
        faces = np.array(mesh_wall.faces)

        return vertices, faces

    else:
        wall = []
        holes = []
        for polygon in polygons:
            if np.any(np.intersect1d(polygon, vertices_hole)):
                holes.append(polygon)
            else:
                wall.append(polygon)

        # extract junctions on this plane
        indices = []
        junctions_wall = []
        for plane in wall:
            for vertex in plane:
                indices.append(vertex)
                junctions_wall.append(junctions[vertex])

        junctions_holes = []
        for plane in holes:
            junctions_hole = []
            for vertex in plane:
                indices.append(vertex)
                junctions_hole.append(junctions[vertex])
            junctions_holes.append(junctions_hole)

        junctions_wall = [project(x, meta) for x in junctions_wall]
        junctions_holes = [[project(x, meta) for x in junctions_hole] for junctions_hole in junctions_holes]

        mesh_wall = triangulate(junctions_wall)

        for hole in junctions_holes:
            mesh_hole = triangulate(hole)
            mesh_wall = pymesh.boolean(mesh_wall, mesh_hole, 'difference')

        vertices = [project_inv(vertex, meta) for vertex in mesh_wall.vertices]

        return vertices, np.array(mesh_wall.faces)
