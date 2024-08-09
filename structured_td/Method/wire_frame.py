import numpy as np
import open3d as o3d
from typing import Tuple

from structured_td.Config.colors import colormap_255

def toO3DWireFrame(annos: dict) -> Tuple[o3d.geometry.PointCloud, o3d.geometry.LineSet]:
    """visualize wireframe
    """
    colormap = np.array(colormap_255) / 255

    junctions = np.array([item['coordinate'] for item in annos['junctions']])
    _, junction_pairs = np.where(np.array(annos['lineJunctionMatrix']))
    junction_pairs = junction_pairs.reshape(-1, 2)

    # extract hole lines
    lines_holes = []
    for semantic in annos['semantics']:
        if semantic['type'] in ['window', 'door']:
            for planeID in semantic['planeID']:
                lines_holes.extend(np.where(np.array(annos['planeLineMatrix'][planeID]))[0].tolist())
    lines_holes = np.unique(lines_holes)

    # extract cuboid lines
    cuboid_lines = []
    for cuboid in annos['cuboids']:
        for planeID in cuboid['planeID']:
            cuboid_lineID = np.where(np.array(annos['planeLineMatrix'][planeID]))[0].tolist()
            cuboid_lines.extend(cuboid_lineID)
    cuboid_lines = np.unique(cuboid_lines)
    cuboid_lines = np.setdiff1d(cuboid_lines, lines_holes)

    # visualize junctions
    connected_junctions = junctions[np.unique(junction_pairs)]
    connected_colors = np.repeat(colormap[0].reshape(1, 3), len(connected_junctions), axis=0)

    junction_set = o3d.geometry.PointCloud()
    junction_set.points = o3d.utility.Vector3dVector(connected_junctions)
    junction_set.colors = o3d.utility.Vector3dVector(connected_colors)

    # visualize line segments
    line_colors = np.repeat(colormap[5].reshape(1, 3), len(junction_pairs), axis=0)

    # color holes
    if len(lines_holes) != 0:
        line_colors[lines_holes] = colormap[6]

    # color cuboids
    if len(cuboid_lines) != 0:
        line_colors[cuboid_lines] = colormap[2]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(junctions)
    line_set.lines = o3d.utility.Vector2iVector(junction_pairs)
    line_set.colors = o3d.utility.Vector3dVector(line_colors)

    return junction_set, line_set
