import os
import cv2

from structured_td.Method.path import createFileFolder, removeFile
from structured_td.Method.depth import depthFile2RGB

class DepthRenderer(object):
    def __init__(self, dataset_folder_path: str) -> None:
        self.dataset_folder_path = dataset_folder_path
        return

    def renderImagesWithTags(self, scene_id: str, perspective_folder_path: str, scene_tag: str, image_tag: str, save_folder_path: str, overwrite: bool = False) -> bool:
        scene_tag_folder_path = perspective_folder_path + scene_tag + '/'
        if not os.path.exists(scene_tag_folder_path):
            print('[WARN][PerspectiveRenderer::copyImagesWithTags]')
            print('\t scene tag folder not exist! will skip!')
            print('\t scene_tag_folder_path:', scene_tag_folder_path)
            return True

        image_id_list = os.listdir(scene_tag_folder_path)

        for image_id in image_id_list:
            save_image_file_path = save_folder_path + '/perspective/' + scene_tag + '/' + image_tag + '/' + scene_id + '_' + image_id + '.png'
            if os.path.exists(save_image_file_path):
                if not overwrite:
                    continue

                removeFile(save_image_file_path)

            image_file_path = scene_tag_folder_path + image_id + '/' + image_tag + '.png'
            if not os.path.exists(image_file_path):
                continue

            depth_image = depthFile2RGB(image_file_path)

            if depth_image is None:
                continue

            createFileFolder(save_image_file_path)

            cv2.imwrite(save_image_file_path, depth_image)
        return True

    def loadScene(self, scene_id: str,
                  save_folder_path: str,
                  overwrite: bool = False) -> bool:
        scene_folder_path = self.dataset_folder_path + "scene_" + scene_id + "/2D_rendering/"
        if not os.path.exists(scene_folder_path):
            print("[ERROR][perspectiveRenderer::loadScene]")
            print('\t scene folder not exist!')
            print('\t scene_folder_path:', scene_folder_path)
            return False

        room_id_list = os.listdir(scene_folder_path)

        for room_id in room_id_list:
            perspective_folder_path = scene_folder_path + room_id + "/perspective/"

            if not os.path.exists(perspective_folder_path):
                continue

            self.renderImagesWithTags(scene_id, perspective_folder_path, 'full', 'depth', save_folder_path, overwrite)
            # self.renderImagesWithTags(scene_id, perspective_folder_path, 'empty', 'depth', save_folder_path, overwrite)
        return True
