# main_script.py
import os
import argparse
import yaml
from PIL import Image
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="Segmentation d'image")
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        type=str,
        help="Path to the YAML configuration file.",
    )
    args = parser.parse_args()
    return args

def load_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def load_networks(args):
    if args["use_CPU"]:
        return YOLO(args["model_fpath"])
    else:
        pass

def test_segmentation(args):
    model = load_networks(args)
    results = model.predict(
        args["root_images"],
        task=args["task"],
        save=args["save"],
        show=args["show"],
        conf=0.5,
    )

    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
        im.save('results.jpg')  # save image

if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    test_segmentation(config)
