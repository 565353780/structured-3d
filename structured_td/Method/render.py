import os
import cv2
import json
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, mapping

from structured_td.Config.colors import colormap_255, semantics_cmap
from structured_td.Method.figures import plot_coords
from structured_td.Method.wire_frame import toO3DWireFrame
from structured_td.Method.plane import toO3DPlane
from structured_td.Method.floor_plan import toFloorPlan
from structured_td.Method.panorama import draw_boundary_from_cor_id

def draw_geometries_with_back_face(geometries: list) -> bool:
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    render_option = vis.get_render_option()
    render_option.mesh_show_back_face = True
    for geometry in geometries:
        vis.add_geometry(geometry)
    vis.run()
    vis.destroy_window()
    return True

def plotFloorplan(annos, polygons):
    """plot floorplan
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    junctions = np.array([junc['coordinate'][:2] for junc in annos['junctions']])
    for (polygon, poly_type) in polygons:
        polygon = Polygon(junctions[np.array(polygon)])
        geojson_data = mapping(polygon)
        plot_coords(ax, polygon.exterior, alpha=0.5)
        if poly_type == 'outwall':
            patch = PolygonPatch(geojson_data, facecolor=semantics_cmap[poly_type], alpha=0)
        else:
            patch = PolygonPatch(geojson_data, facecolor=semantics_cmap[poly_type], alpha=0.5)
        ax.add_patch(patch)

    plt.axis('equal')
    plt.axis('off')
    return True

def drawPanoramaLayout(room_path: str) -> np.ndarray:
    cor_id = np.loadtxt(os.path.join(room_path, "layout.txt"))
    img_src = cv2.imread(os.path.join(room_path, "full", "rgb_rawlight.png"))
    img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB)
    img_viz = draw_boundary_from_cor_id(cor_id, img_src)
    return img_viz

def plotPerspectiveLayout(position_path: str) -> bool:
    colors = np.array(colormap_255) / 255

    image = cv2.imread(os.path.join(position_path, "rgb_rawlight.png"))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with open(os.path.join(position_path, "layout.json")) as f:
        annos = json.load(f)

    fig = plt.figure()
    for i, key in enumerate(['amodal_mask', 'visible_mask']):
        ax = fig.add_subplot(2, 1, i + 1)
        plt.axis('off')
        plt.imshow(image)

        for i, planes in enumerate(annos['planes']):
            if len(planes[key]):
                for plane in planes[key]:
                    polygon = Polygon([annos['junctions'][id]['coordinate'] for id in plane])
                    geojson_data = mapping(polygon)
                    patch = PolygonPatch(geojson_data, facecolor=colors[i], alpha=0.5)
                    ax.add_patch(patch)

        plt.title(key)
    return True

def renderWireFrame(annos: dict) -> bool:
    junction_set, line_set = toO3DWireFrame(annos)
    o3d.visualization.draw_geometries([junction_set, line_set])
    return True

def renderPlane(annos: dict, color_mode: str = 'normal', eps: float =0.9) -> bool:
    plane_set = toO3DPlane(annos, color_mode, eps)
    draw_geometries_with_back_face(plane_set)
    return True

def renderFloorPlan(annos: dict) -> bool:
    polygons = toFloorPlan(annos)
    plotFloorplan(annos, polygons)
    plt.show()
    plt.close()
    return True

def renderPanoramaLayout(room_path: str) -> bool:
    image = drawPanoramaLayout(room_path)
    plt.axis('off')
    plt.imshow(image)
    plt.show()
    plt.close()
    return True

def renderPerspectiveLayout(position_path: str) -> bool:
    plotPerspectiveLayout(position_path)
    plt.show()
    plt.close()
    return True
