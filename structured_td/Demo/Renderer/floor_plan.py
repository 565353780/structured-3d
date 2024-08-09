import sys
sys.path.append('../open3d-manage')

from structured_td.Module.Renderer.floor_plan import FloorPlanRenderer

def demo():
    dataset_folder_path = "/home/chli/chLi/Dataset/Structured3D/Structured3D/"
    scene_id = "00000"
    overwrite = False

    floor_plan_renderer = FloorPlanRenderer(dataset_folder_path)

    for i in range(100):
        scene_id = str(i).zfill(5)
        save_image_file_path = "./output/images/floor_plan/" + scene_id + ".png"

        print('start process scene', scene_id, '...')
        if not floor_plan_renderer.loadScene(scene_id, save_image_file_path, overwrite):
            continue
    return True
