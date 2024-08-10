import sys
sys.path.append('../open3d-manage')

from structured_td.Module.Renderer.wire_frame import WireFrameRenderer

def demo():
    dataset_folder_path = "/home/chli/chLi/Dataset/Structured3D/Structured3D/"
    window_name = "WireFrameRenderer"
    width = 1920
    height = 1080
    left = 10
    top = 10
    visible = True
    scene_id = "00000"
    save_folder_path = "./output/images/" + scene_id + "/wire_frame/"
    save_video_file_path = "./output/video/wire_frame/" + scene_id + ".mp4"
    rotate_one_cycle_second = 10.0
    fps = 30
    overwrite = False

    wire_frame_renderer = WireFrameRenderer(dataset_folder_path,
                                            window_name,
                                            width, height,
                                            left, top, visible)
    for i in range(200):
        scene_id = str(i).zfill(5)
        save_folder_path = "./output/images/" + scene_id + "/wire_frame/"
        save_video_file_path = "./output/video/wire_frame/" + scene_id + ".mp4"

        print('start process scene', scene_id, '...')
        if not wire_frame_renderer.loadScene(scene_id):
            continue
        wire_frame_renderer.renderVideo(save_folder_path, save_video_file_path, rotate_one_cycle_second, fps, overwrite)
    return True
