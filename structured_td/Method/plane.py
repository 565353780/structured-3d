import numpy as np
import open3d as o3d

from structured_td.Config.colors import colormap_255
from structured_td.Method.polygon import convert_lines_to_vertices, clip_polygon

def toO3DPlane(annos, args, eps=0.9):
    colormap = np.array(colormap_255) / 255
    junctions = [item['coordinate'] for item in annos['junctions']]

    if args.color == 'manhattan':
        manhattan = dict()
        for planes in annos['manhattan']:
            for planeID in planes['planeID']:
                manhattan[planeID] = planes['ID']

    # extract hole vertices
    lines_holes = []
    for semantic in annos['semantics']:
        if semantic['type'] in ['window', 'door']:
            for planeID in semantic['planeID']:
                lines_holes.extend(np.where(np.array(annos['planeLineMatrix'][planeID]))[0].tolist())

    lines_holes = np.unique(lines_holes)
    _, vertices_holes = np.where(np.array(annos['lineJunctionMatrix'])[lines_holes])
    vertices_holes = np.unique(vertices_holes)

    # load polygons
    polygons = []
    for semantic in annos['semantics']:
        for planeID in semantic['planeID']:
            plane_anno = annos['planes'][planeID]
            lineIDs = np.where(np.array(annos['planeLineMatrix'][planeID]))[0].tolist()
            junction_pairs = [np.where(np.array(annos['lineJunctionMatrix'][lineID]))[0].tolist() for lineID in lineIDs]
            polygon = convert_lines_to_vertices(junction_pairs)
            vertices, faces = clip_polygon(polygon, vertices_holes, junctions, plane_anno)
            polygons.append([vertices, faces, planeID, plane_anno['normal'], plane_anno['type'], semantic['type']])

    plane_set = []
    for vertices, faces, planeID, normal, plane_type, semantic_type in polygons:
        # ignore the room ceiling
        if plane_type == 'ceiling' and semantic_type not in ['door', 'window']:
            continue

        plane_vis = o3d.geometry.TriangleMesh()

        plane_vis.vertices = o3d.utility.Vector3dVector(vertices)
        plane_vis.triangles = o3d.utility.Vector3iVector(faces)

        if args.color == 'normal':
            if np.dot(normal, [1, 0, 0]) > eps:
                plane_vis.paint_uniform_color(colormap[0])
            elif np.dot(normal, [-1, 0, 0]) > eps:
                plane_vis.paint_uniform_color(colormap[1])
            elif np.dot(normal, [0, 1, 0]) > eps:
                plane_vis.paint_uniform_color(colormap[2])
            elif np.dot(normal, [0, -1, 0]) > eps:
                plane_vis.paint_uniform_color(colormap[3])
            elif np.dot(normal, [0, 0, 1]) > eps:
                plane_vis.paint_uniform_color(colormap[4])
            elif np.dot(normal, [0, 0, -1]) > eps:
                plane_vis.paint_uniform_color(colormap[5])
            else:
                plane_vis.paint_uniform_color(colormap[6])
        elif args.color == 'manhattan':
            # paint each plane with manhattan world
            if planeID not in manhattan.keys():
                plane_vis.paint_uniform_color(colormap[6])
            else:
                plane_vis.paint_uniform_color(colormap[manhattan[planeID]])

        plane_set.append(plane_vis)

    return plane_set
