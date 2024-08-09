import os
import json
from math import ceil
from tqdm import trange

from open3d_manage.Method.video import createVideoFromImages

from structured_td.Method.wire_frame import toO3DWireFrame
from structured_td.Module.Renderer.o3d import O3DRenderer

class WireFrameRenderer(object):
    def __init__(self,
                 dataset_folder_path: str,
        window_name: str = "WireFrameRenderer",
        width: int = 1920,
        height: int = 1080,
        left: int = 50,
        top: int = 50,
        visible: bool = True) -> None:
        self.dataset_folder_path = dataset_folder_path

        self.renderer = O3DRenderer(window_name, width, height, left, top, visible)

        self.z_rotate_angle = 0.0
        self.y_rotate_angle = 0.0
        self.x_rotate_angle = -45.0
        return

    def loadScene(self, scene_id: str) -> bool:
        json_file_path = self.dataset_folder_path + "scene_" + scene_id + "/annotation_3d.json"
        if not os.path.exists(json_file_path):
            print("[ERROR][WireFrameRenderer::loadScene]")
            print('\t json file not exist!')
            print('\t json_file_path:', json_file_path)
            return False

        with open(json_file_path) as file:
            annos = json.load(file)

            junction_set, line_set = toO3DWireFrame(annos)

            geometries = [junction_set, line_set]

            self.renderer.loadGeometries(geometries, self.z_rotate_angle, self.y_rotate_angle, self.x_rotate_angle)
        return True

    def renderImages(self,
                     save_folder_path: str,
                     rotate_one_cycle_second: float = 1.0,
                     fps: int = 30,
                     overwrite: bool = False) -> bool:
        os.makedirs(save_folder_path, exist_ok=True)

        total_render_image_num = ceil(rotate_one_cycle_second * fps)
        delta_rotate_angle = 360.0 / total_render_image_num

        for z_rotate_idx in trange(total_render_image_num):
            current_z_rotate_angle = self.z_rotate_angle + delta_rotate_angle * z_rotate_idx

            current_save_file_path = save_folder_path + str(z_rotate_idx) + '.png'

            self.renderer.sampleImage(current_save_file_path, current_z_rotate_angle, self.y_rotate_angle, self.x_rotate_angle, overwrite)
        return True

    def renderVideo(self,
                    save_folder_path: str,
                    save_video_file_path: str,
                    rotate_one_cycle_second: float = 1.0,
                    fps: int = 30,
                    overwrite: bool = False) -> bool:
        if not self.renderImages(save_folder_path, rotate_one_cycle_second, fps, overwrite):
            print('[ERROR][WireFrameRenderer::renderVideo]')
            print('\t renderImages failed!')
            return False

        bg_color = [255, 255, 255]

        if not createVideoFromImages(save_folder_path, save_video_file_path, bg_color, fps, overwrite):
            print('[ERROR][WireFrameRenderer::renderVideo]')
            print('\t createVideoFromImages failed!')
            return False

        return True
