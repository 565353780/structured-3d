import os
import json
import argparse

from structured_td.Method.render import renderWireFrame, renderPlane, renderFloorPlan

def parse_args():
    parser = argparse.ArgumentParser(description="Structured3D 3D Visualization")
    parser.add_argument("--path", required=True,
                        help="dataset path", metavar="DIR")
    parser.add_argument("--scene", required=True,
                        help="scene id", type=int)
    parser.add_argument("--type", choices=("floorplan", "wireframe", "plane"),
                        default="plane", type=str)
    parser.add_argument("--color", choices=["normal", "manhattan"],
                        default="normal", type=str)
    return parser.parse_args()


def main():
    args = parse_args()

    # load annotations from json
    with open(os.path.join(args.path, f"scene_{args.scene:05d}", "annotation_3d.json")) as file:
        annos = json.load(file)

    if args.type == "wireframe":
        renderWireFrame(annos)
    elif args.type == "plane":
        renderPlane(annos, args)
    elif args.type == "floorplan":
        renderFloorPlan(annos)


if __name__ == "__main__":
    main()
