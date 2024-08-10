import os
import argparse

import numpy as np

from structured_td.Method.render import renderPanoramaLayout, renderPerspectiveLayout


def visualize_panorama(args):
    scene_path = os.path.join(args.path, f"scene_{args.scene:05d}", "2D_rendering")

    for room_id in np.sort(os.listdir(scene_path)):
        room_path = os.path.join(scene_path, room_id, "panorama")

        renderPanoramaLayout(room_path)

def visualize_perspective(args):
    scene_path = os.path.join(args.path, f"scene_{args.scene:05d}", "2D_rendering")

    for room_id in np.sort(os.listdir(scene_path)):
        room_path = os.path.join(scene_path, room_id, "perspective", "full")

        if not os.path.exists(room_path):
            continue

        for position_id in np.sort(os.listdir(room_path)):
            position_path = os.path.join(room_path, position_id)

            renderPerspectiveLayout(position_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Structured3D 2D Layout Visualization")
    parser.add_argument("--path", required=True,
                        help="dataset path", metavar="DIR")
    parser.add_argument("--scene", required=True,
                        help="scene id", type=int)
    parser.add_argument("--type", choices=["perspective", "panorama"], required=True,
                        help="type of camera", type=str)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.type == 'panorama':
        visualize_panorama(args)
    elif args.type == 'perspective':
        visualize_perspective(args)


if __name__ == "__main__":
    main()
