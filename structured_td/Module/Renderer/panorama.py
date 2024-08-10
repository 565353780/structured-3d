import os
from shutil import copyfile

from structured_td.Method.path import createFileFolder, removeFile

class PanoramaRenderer(object):
    def __init__(self, dataset_folder_path: str) -> None:
        self.dataset_folder_path = dataset_folder_path
        return

    def copyImageWithTag(self, scene_id: str, panorama_folder_path: str, tag: str, save_folder_path: str, overwrite: bool = False) -> bool:
        save_tag_file_path = save_folder_path + '/panorama/' + tag + '/' + scene_id + '.png'
        if os.path.exists(save_tag_file_path):
            if not overwrite:
                return True

            removeFile(save_tag_file_path)

        tag_file_path = panorama_folder_path + tag + '.png'
        if not os.path.exists(tag_file_path):
            return True

        createFileFolder(save_tag_file_path)
        copyfile(tag_file_path, save_tag_file_path)
        return True

    def loadScene(self, scene_id: str,
                  save_folder_path: str,
                  overwrite: bool = False) -> bool:
        scene_folder_path = self.dataset_folder_path + "scene_" + scene_id + "/2D_rendering/"
        if not os.path.exists(scene_folder_path):
            print("[ERROR][PanoramaRenderer::loadScene]")
            print('\t scene folder not exist!')
            print('\t scene_folder_path:', scene_folder_path)
            return False

        room_id_list = os.listdir(scene_folder_path)

        for room_id in room_id_list:
            panorama_folder_path = scene_folder_path + room_id + "/panorama/"

            if not os.path.exists(panorama_folder_path):
                continue

            self.copyImageWithTag(scene_id, panorama_folder_path, 'simple/rgb_rawlight', save_folder_path, overwrite)
            self.copyImageWithTag(scene_id, panorama_folder_path, 'full/rgb_rawlight', save_folder_path, overwrite)
            self.copyImageWithTag(scene_id, panorama_folder_path, 'empty/rgb_rawlight', save_folder_path, overwrite)
        return True
