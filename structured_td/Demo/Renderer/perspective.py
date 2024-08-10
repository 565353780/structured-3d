from structured_td.Module.Renderer.perspective import PerspectiveRenderer

def demo():
    dataset_folder_path = "/home/chli/chLi/Dataset/Structured3D/Structured3D/"
    scene_id = "00000"
    save_folder_path = "./output/render_images/"
    overwrite = False

    perspective_renderer = PerspectiveRenderer(dataset_folder_path)

    for i in range(2):
        scene_id = str(i).zfill(5)

        print('start process scene', scene_id, '...')
        if not perspective_renderer.loadScene(scene_id, save_folder_path, overwrite):
            continue
    return True
