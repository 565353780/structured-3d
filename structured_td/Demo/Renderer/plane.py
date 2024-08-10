import sys
sys.path.append('../open3d-manage')

from structured_td.Module.Renderer.plane import PlaneRenderer

def demo():
    dataset_folder_path = "/home/chli/chLi/Dataset/Structured3D/Structured3D/"
    window_name = "PlaneRenderer"
    width = 1920
    height = 1080
    left = 10
    top = 10
    visible = True
    scene_id = "00000"
    save_folder_path = "./output/images/" + scene_id + "/plane/"
    save_video_file_path = "./output/video/plane/" + scene_id + ".mp4"
    rotate_one_cycle_second = 10.0
    fps = 30
    overwrite = False

    plane_renderer = PlaneRenderer(dataset_folder_path,
                                            window_name,
                                            width, height,
                                            left, top, visible)
    for i in range(200):
        if i in [5]:
            continue

        scene_id = str(i).zfill(5)
        save_folder_path = "./output/images/" + scene_id + "/plane/"
        save_video_file_path = "./output/video/plane/" + scene_id + ".mp4"

        print('start process scene', scene_id, '...')
        if not plane_renderer.loadScene(scene_id):
            continue
        plane_renderer.renderVideo(save_folder_path, save_video_file_path, rotate_one_cycle_second, fps, overwrite)
    return True
