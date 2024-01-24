import torch
import torch.nn as nn
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from torchvision.models.detection import FasterRCNN
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from PIL import Image
import json
import os
import random
import matplotlib.pyplot as plt
import numpy as np

class CustomDataset(Dataset):
    def __init__(self, root_dir, annotation_file, transform=None):
        self.root_dir = root_dir
        self.transform = transform

        with open(annotation_file, 'r') as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data['images'])

    def __getitem__(self, idx):
        img_info = self.data['images'][idx]
        img_name = os.path.join(self.root_dir, img_info['file_name'])
        image = Image.open(img_name).convert('RGB')

        annotations = [ann for ann in self.data['annotations'] if ann['image_id'] == img_info['id']]

        # Extract relevant information from the annotation
        boxes = [ann['bbox'] for ann in annotations]
        labels = [ann['category_id'] for ann in annotations]

        # Check if there are any bounding boxes for this image
        if len(boxes) == 0:
            # If no bounding boxes, provide a dummy box and label
            boxes = [[0, 0, 1, 1]]  # Adjust the size of the dummy box based on your image size
            labels = [0]  # Assuming 0 is the background class or a default class

        target = {
            'boxes': torch.tensor(boxes, dtype=torch.float32),
            'labels': torch.tensor(labels, dtype=torch.int64),
            # Add other necessary keys such as 'image_id', 'area', 'iscrowd', etc.
        }

        # Ensure 'image_id' is an integer
        target['image_id'] = int(img_info['id'])

        sample = {'image': image, 'target': target}

        if self.transform:
            sample = self.transform(sample)

        return sample
        

class ToTensor(object):
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size

    def __call__(self, sample):
        image, target = sample['image'], sample['target']
        # Resize image
        resize_transform = transforms.Resize(self.target_size)
        image = resize_transform(image)

        # Convert image to tensor
        image = transforms.ToTensor()(image)

        return {'image': image, 'target': target}


class FasterRCNNModel(nn.Module):
    def __init__(self, num_classes):
        super(FasterRCNNModel, self).__init__()
        self.backbone = fasterrcnn_resnet50_fpn(pretrained=True)
        in_features = self.backbone.roi_heads.box_predictor.cls_score.in_features
        self.backbone.roi_heads.box_predictor = nn.Linear(in_features, num_classes + 1)

    def forward(self, x, target=None):
        if self.training and target is None:
            raise ValueError("In training mode, targets should be passed to the forward function.")

        return self.backbone(x, target)


# Training loop
def train_model(model, train_loader, criterion, optimizer, num_epochs=5, device='cuda'):
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        for batch_idx, batch_data in enumerate(train_loader):
            inputs, targets = batch_data['image'].to(device), batch_data['target']
            targets['boxes'] = targets['boxes'].to(device)
            targets['labels'] = targets['labels'].to(device)
            print(type(targets['boxes']),targets['boxes'])
            optimizer.zero_grad()
            outputs = model(inputs, targets)
            loss = sum(outputs.values())
            loss.backward()
            optimizer.step()
            print(f'Epoch [{epoch + 1}/{num_epochs}], Batch [{batch_idx + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')


if __name__ == "__main__":
    train_dataset = CustomDataset(root_dir='/home/shiv/Desktop/Projet_MOOREV/dataset/train',
                                  annotation_file='/home/shiv/Desktop/Projet_MOOREV/dataset/train/_annotations.json',
                                  transform=transforms.Compose([ToTensor()]))

    test_dataset = CustomDataset(root_dir='/home/shiv/Desktop/Projet_MOOREV/dataset/test',
                                 annotation_file='/home/shiv/Desktop/Projet_MOOREV/dataset/test/_annotations.json',
                                 transform=transforms.Compose([ToTensor()]))

   # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=2, shuffle=False)

    model = FasterRCNNModel(num_classes=1)

    # Move the model to CUDA
    model.to('cuda')

    # Define the loss function, optimizer, and number of epochs
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    num_epochs = 5

    # Train the model
    train_model(model, train_loader, criterion, optimizer, num_epochs)


    # Save the model
    model_path = '/home/shiv/Desktop/Projet_MOOREV/models/FRCNNresnet50.pth'
    torch.save({
        'model_state_dict': model.state_dict(),
    }, model_path)

    # Select a random image index for visualization
    random_index = random.randint(0, len(test_dataset) - 1)

    # Get the sample data for visualization
    sample = test_dataset[random_index]

    # Get the original bounding box
    original_bbox = sample['bbox']

    # Get the predicted bounding box using the trained model
    model.to('cuda')
    model.eval()
    with torch.no_grad():
        input_image = sample['image'].unsqueeze(0).to('cuda')
        output = model(input_image)
        # Modify this part according to your model's output format for bounding boxes
        predicted_bbox = output[0]['boxes'][0].cpu().numpy()

    # Ensure predicted bounding boxes are within the image boundaries
    predicted_bbox[0] = max(0, min(predicted_bbox[0], original_bbox[2] - 1))
    predicted_bbox[1] = max(0, min(predicted_bbox[1], original_bbox[3] - 1))
    predicted_bbox[2] = min(original_bbox[2] - 1, max(1, predicted_bbox[2]))
    predicted_bbox[3] = min(original_bbox[3] - 1, max(1, predicted_bbox[3]))

    # Plot the image with original and predicted bounding boxes
    image = transforms.ToPILImage()(sample['image'].cpu())  # Convert tensor to CPU before applying ToPILImage

    plt.imshow(image)
    plt.gca().add_patch(plt.Rectangle((original_bbox[0], original_bbox[1]),
                                      original_bbox[2] - original_bbox[0],
                                      original_bbox[3] - original_bbox[1],
                                      linewidth=2, edgecolor='r', facecolor='none', label='Original BBox'))
    plt.gca().add_patch(plt.Rectangle((predicted_bbox[0], predicted_bbox[1]),
                                      predicted_bbox[2] - predicted_bbox[0],
                                      predicted_bbox[3] - predicted_bbox[1],
                                      linewidth=2, edgecolor='b', facecolor='none', label='Predicted BBox'))
    plt.legend()
    plt.show()