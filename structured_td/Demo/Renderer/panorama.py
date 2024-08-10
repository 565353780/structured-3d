from structured_td.Module.Renderer.panorama import PanoramaRenderer

def demo():
    dataset_folder_path = "/home/chli/chLi/Dataset/Structured3D/Structured3D/"
    scene_id = "00000"
    save_folder_path = "./output/render_images/"
    overwrite = False

    panorama_renderer = PanoramaRenderer(dataset_folder_path)

    for i in range(100):
        scene_id = str(i).zfill(5)

        print('start process scene', scene_id, '...')
        if not panorama_renderer.loadScene(scene_id, save_folder_path, overwrite):
            continue
    return True
