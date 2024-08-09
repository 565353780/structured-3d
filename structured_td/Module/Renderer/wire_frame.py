import os
import cv2
import json
import numpy as np
import open3d as o3d
from math import ceil
from tqdm import tqdm, trange

from open3d_manage.Method.path import createFileFolder

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

            abb1 = junction_set.get_axis_aligned_bounding_box()
            abb2 = junction_set.get_axis_aligned_bounding_box()

            min_bound = np.min(np.vstack([abb1.min_bound, abb2.min_bound]), axis=0)
            max_bound = np.max(np.vstack([abb1.max_bound, abb2.max_bound]), axis=0)

            center = (min_bound + max_bound) / 2.0
            length = max_bound - min_bound
            height = length[2]
            radius = np.max(length[:2])

            cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height, resolution=100)
            cylinder.translate(center)

            z_rad = np.pi *  self.z_rotate_angle / 180.0
            cos_z = np.cos(z_rad)
            sin_z = np.sin(z_rad)

            z_rotate_matrix = np.array(
                [
                    [cos_z, -sin_z, 0],
                    [sin_z, cos_z, 0],
                    [0, 0, 1],
                ],
                dtype=float,
            )


            y_rad = np.pi *  self.y_rotate_angle / 180.0
            cos_y = np.cos(y_rad)
            sin_y = np.sin(y_rad)

            y_rotate_matrix = np.array(
                [
                    [cos_y, 0, -sin_y],
                    [0, 1, 0],
                    [sin_y, 0, cos_y],
                ],
                dtype=float,
            )

            x_rad = np.pi * self.x_rotate_angle / 180.0
            cos_x = np.cos(x_rad)
            sin_x = np.sin(x_rad)

            x_rotate_matrix = np.array(
                [
                    [1, 0, 0],
                    [0, cos_x, -sin_x],
                    [0, sin_x, cos_x],
                ],
                dtype=float,
            )

            rotate_matrix = x_rotate_matrix.dot(y_rotate_matrix).dot(z_rotate_matrix)
            cylinder.rotate(rotate_matrix)

            self.renderer.o3d_viewer.clearGeometries()
            self.renderer.o3d_viewer.addGeometry(cylinder)

            geometries = [junction_set, line_set]

            self.renderer.loadGeometries(geometries)
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

        if not overwrite:
            if os.path.exists(save_video_file_path):
                return True

        createFileFolder(save_video_file_path)

        bg_color = [255, 255, 255]

        image_filename_list = os.listdir(save_folder_path)
        image_filename_list.sort(key=lambda x: int(x.split('.')[0]))

        image_filepath_list = []

        for image_filename in image_filename_list:
            if image_filename[-4:] != ".png":
                continue

            image_file_path = save_folder_path + image_filename

            image_filepath_list.append(image_file_path)

        first_image = cv2.imread(image_filepath_list[0], cv2.IMREAD_UNCHANGED)
        height, width = first_image.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(save_video_file_path, fourcc, fps, (width, height))

        print('start convert images to video...')
        for image_file_path in tqdm(image_filepath_list):
            image = cv2.imread(image_file_path, cv2.IMREAD_UNCHANGED)

            if image.shape[2] == 3:
                video_writer.write(image)
                continue

            bgr = image[:, :, :3]
            alpha = image[:, :, 3]

            background = np.asarray(bg_color, dtype=np.uint8)

            alpha_mask = alpha / 255.0

            bgr = bgr * alpha_mask[:, :, np.newaxis] + background * (1 - alpha_mask[:, :, np.newaxis])
            bgr = bgr.astype(np.uint8)

            video_writer.write(bgr)

        video_writer.release()
        return True
