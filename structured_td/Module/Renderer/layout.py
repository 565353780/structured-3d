import os
import json
import matplotlib.pyplot as plt


from structured_td.Method.path import createFileFolder
from structured_td.Method.floor_plan import toFloorPlan
from structured_td.Method.render import drawPanoramaLayout, plotPerspectiveLayout

class LayoutRenderer(object):
    def __init__(self, dataset_folder_path: str) -> None:
        self.dataset_folder_path = dataset_folder_path
        return

    def loadScene(self, scene_id: str,
                  save_file_path: str,
                  overwrite: bool = False) -> bool:
        if not overwrite:
            if os.path.exists(save_file_path):
                return True

        json_file_path = self.dataset_folder_path + "scene_" + scene_id + "/annotation_3d.json"
        if not os.path.exists(json_file_path):
            print("[ERROR][PlaneRenderer::loadScene]")
            print('\t json file not exist!')
            print('\t json_file_path:', json_file_path)
            return False

        with open(json_file_path) as file:
            annos = json.load(file)

            polygons = toFloorPlan(annos)

            plot_floorplan(annos, polygons)

        createFileFolder(save_file_path)

        plt.savefig(save_file_path, transparent=True, bbox_inches='tight')
        plt.close()
        return True
