import os
import numpy as np
from copy import deepcopy


from open3d_manage.Method.path import createFileFolder
from open3d_manage.Module.o3d_viewer import O3DViewer


class O3DRenderer(object):
    def __init__(
        self,
        window_name: str = "Open3D",
        width: int = 1920,
        height: int = 1080,
        left: int = 50,
        top: int = 50,
        visible: bool = True,
    ) -> None:
        self.o3d_viewer = O3DViewer()
        self.o3d_viewer.createWindow(window_name, width, height, left, top, visible)

        self.geometries = []
        return

    def loadGeometries(self, geometries: list) -> bool:
        self.geometries = geometries
        return True

    def sampleImage(
        self,
        save_file_path: str,
        z_rotate_angle: float = 0.0,
        y_rotate_angle: float = 0.0,
        x_rotate_angle: float = 0.0,
        overwrite: bool = False,
    ) -> bool:
        if len(self.geometries) == 0:
            print("[ERROR][O3DRenderer::sampleImage]")
            print("\t geometries not exist!")
            return False

        if not overwrite:
            if os.path.exists(save_file_path):
                return True

        z_rad = np.pi *  z_rotate_angle / 180.0
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


        y_rad = np.pi *  y_rotate_angle / 180.0
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

        x_rad = np.pi * x_rotate_angle / 180.0
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

        rotate_geometries = deepcopy(self.geometries)

        for geometry in rotate_geometries:
            geometry.rotate(rotate_matrix)

        self.o3d_viewer.clearGeometries(False)
        self.o3d_viewer.addGeometries(rotate_geometries, False)
        self.o3d_viewer.update()

        createFileFolder(save_file_path)

        self.o3d_viewer.captureScreenImage(save_file_path, overwrite)
        return True
