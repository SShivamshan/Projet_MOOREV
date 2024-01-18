import argparse
import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import yaml
from PIL import Image
from torchvision.transforms import ToTensor
from tqdm import tqdm
from ultralytics import YOLO
from webcolors import hex_to_rgb, rgb_to_name


def parse_args():
    parser = argparse.ArgumentParser(description="Segmentation d'image")

    parser.add_argument(
        "--use-cuda",
        help="Use CUDA.",
        default=False,
        type=bool,
    )
    parser.add_argument(
        "--root-images",
        help="Directory path to images.",
        default="data/images/image.jpg",
        type=str,
    )
    parser.add_argument(
        "--model-fpath",
        default="test/models/best.pt",
        type=str,
        help="file path to load trained model",
    )
    parser.add_argument(
        "--use-CPU",
        default=True,
        type=bool,
        help="Specify whether you are loading trained models on a CPU",
    )
    parser.add_argument(
        "--task",
        default="segment",
        type=str,
        help="Specify the task of the trained model",
    )
    args = parser.parse_args()
    return args

def load_networks(args):
    if args.use_CPU:
        return YOLO( args.model_fpath 
)
    else:
        pass

def test_segmentation(args):
    
    model = load_networks(args)
    breakpoint()
    results = model.predict(
    args.root_images,
    task=args.task,
    save=True,
    show=True,
    conf=0.5,
)
    breakpoint()


if __name__ == "__main__":
    args = parse_args()
    test_segmentation(args)