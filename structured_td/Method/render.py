import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, mapping

from structured_td.Config.colors import semantics_cmap
from structured_td.Method.figures import plot_coords
from structured_td.Method.wire_frame import toO3DWireFrame
from structured_td.Method.plane import toO3DPlane
from structured_td.Method.floor_plan import toFloorPlan

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

def plot_floorplan(annos, polygons):
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
    # plt.show()
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
    plot_floorplan(annos, polygons)
    plt.show()
    plt.close()
    return True
