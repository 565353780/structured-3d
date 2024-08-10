import os
from shutil import copyfile

from structured_td.Method.path import createFileFolder, removeFile

class PerspectiveRenderer(object):
    def __init__(self, dataset_folder_path: str) -> None:
        self.dataset_folder_path = dataset_folder_path
        return

    def copyImagesWithTags(self, scene_id: str, perspective_folder_path: str, scene_tag: str, image_tag: str, save_folder_path: str, overwrite: bool = False) -> bool:
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

            createFileFolder(save_image_file_path)
            copyfile(image_file_path, save_image_file_path)
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

            # self.copyImagesWithTags(scene_id, perspective_folder_path, 'empty', 'rgb_rawlight', save_folder_path, overwrite)
            self.copyImagesWithTags(scene_id, perspective_folder_path, 'full', 'rgb_rawlight', save_folder_path, overwrite)
            self.copyImagesWithTags(scene_id, perspective_folder_path, 'full', 'semantic', save_folder_path, overwrite)
            self.copyImagesWithTags(scene_id, perspective_folder_path, 'full', 'normal', save_folder_path, overwrite)
        return True
