import os
import cv2
import numpy as np
from typing import Union

def depth2RGB(depth_map: np.ndarray) -> Union[np.ndarray, None]:
    depth_normalized = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    depth_colored = cv2.applyColorMap((depth_normalized * 255).astype(np.uint8), cv2.COLORMAP_JET)

    return depth_colored

def depthFile2RGB(depth_file_path: str) -> Union[np.ndarray, None]:
    if not os.path.exists(depth_file_path):
        print('[ERROR][depth::depthFile2RGB]')
        print('\t depth file not exist!')
        print('\t depth_file_path:', depth_file_path)
        return None

    depth_map = cv2.imread(depth_file_path, cv2.IMREAD_UNCHANGED)

    if depth_map is None:
        print('[ERROR][depth::depthFile2RGB]')
        print('\t depth image load failed!')
        print('\t depth_file_path:', depth_file_path)
        return None

    return depth2RGB(depth_map)
