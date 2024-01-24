import argparse
from roboflow import Roboflow
from ultralytics import YOLO
import torch


def download_dataset(api_key, project_name, workspace, version, format):
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(workspace).project(project_name)
    dataset = project.version(version).download(format)

    
def train_model(yaml_file, nb_epoch, nb_batch, nb_workers):
    # Check for CUDA device and set it
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')
    breakpoint()
    
    # Initialize YOLO model
    model = YOLO("yolov5s.pt").to(device)
    print("device", model.device.type)
    breakpoint()
    
    # Utilize the path to the YAML file when calling model.train()
    results = model.train(batch=nb_batch, data=yaml_file, epochs=nb_epoch, workers=nb_workers, device=0)

    
def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Training Script")
    parser.add_argument("--api_key", default ="MzaPLrymE8EEpeAsatt1", type=str, help="Roboflow API key")
    parser.add_argument("--project_name", type=str, help="Roboflow project name")
    parser.add_argument("--format", type=str, help="Format")
    parser.add_argument("--version", type=int, help="Number of epochs")
    parser.add_argument("--workspace", type=str, help="Roboflow workspace")
    
    parser.add_argument("--yaml_file", type=str, help="Path to the YAML file")
    parser.add_argument("--nb_epoch", default = 200, type=int, help="Number of epochs")
    parser.add_argument("--nb_batch", default = 16, type=int, help="Batch size")
    parser.add_argument("--nb_workers", default = 1, type=int, help="Number of workers")

    args = parser.parse_args()

    # Download dataset
    download_dataset(args.api_key, args.project_name, args.workspace, args.version, args.format)

    # Train model
    #train_model(args.yaml_file, args.nb_epoch, args.nb_batch, args.nb_workers)

if __name__ == "__main__":
    main()

    
    
    
    
# python train.py --yaml_file "data.yaml" --nb_epoch 200 --nb_batch 16 --nb_workers 1

# ---------------------------------------------------------------------------------------------------------------------------------------------
    
# alvini Ifremeria 15
# python train.py --api_key "MzaPLrymE8EEpeAsatt1" --project_name "alvini-detection" --format "yolov8" --version 1 --workspace "are-curiousinfo"

# Gibbule Lobtusata Llittorea troque 78
# python train.py --api_key "MzaPLrymE8EEpeAsatt1" --project_name "curious-moorev" --format "yolov8" --version 4 --workspace "curiousroboflow"
    
# Gibbula Actinia-equina (ouverte fermé)  2390
# python train.py --api_key "MzaPLrymE8EEpeAsatt1" --project_name "pfe-odrk4" --format "yolov8" --version 11 --workspace "lounesal"
    
# Actinia-equina 200
# python train.py --api_key "MzaPLrymE8EEpeAsatt1" --project_name "pfe-cru4x" --format "yolov8" --version 3 --workspace "sorbonne-universit-ebzhb"
    

    
