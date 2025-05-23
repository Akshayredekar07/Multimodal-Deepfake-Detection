# -*- coding: utf-8 -*-
"""model_training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11qz6xiVHPP8cOkPvhV8OQQK1regsRcEl
"""

#!/bin/bash
!kaggle datasets download alaaeddineayadi/real-vs-ai-generated-faces

#!/bin/bash
!kaggle datasets download xhlulu/140k-real-and-fake-faces

!unzip 140k-real-and-fake-faces.zip

!unzip real-vs-ai-generated-faces.zip

from pathlib import Path

# Specify the directory you want to check
directory_path = Path('real_vs_fake')  # Replace with your directory name

# Print the subdirectories and files
for item in directory_path.iterdir():
    if item.is_dir():
        print(f"Directory: {item.name}")
    else:
        print(f"File: {item.name}")

from pathlib import Path

# Specify the directory to check
directory_path = Path('real_vs_fake')  # Replace with your directory name

# Function to print directory tree without files
def print_directory_tree(path, indent=0):
    for item in path.iterdir():
        # Only print if the item is a directory
        if item.is_dir():
            print(' ' * indent + f"__ {item.name}")  # Use + to indicate a directory
            # Recursively print its subdirectories
            print_directory_tree(item, indent + 4)

# Call the function
print_directory_tree(directory_path)

from pathlib import Path

# Specify the directory to check
directory_path = Path('dataset')  # Replace with your directory name

# Function to print directory tree without files
def print_directory_tree(path, indent=0):
    for item in path.iterdir():
        # Only print if the item is a directory
        if item.is_dir():
            print(' ' * indent + f"__ {item.name}")  # Use + to indicate a directory
            # Recursively print its subdirectories
            print_directory_tree(item, indent + 4)

# Call the function
print_directory_tree(directory_path)

import os

def count_images(directory):
    count_dict = {}
    for root, dirs, files in os.walk(directory):
        if files:
            count_dict[root] = len([f for f in files if f.lower().endswith(('jpg', 'jpeg', 'png'))])
    return count_dict

def print_counts(count_dict, dataset_name):
    print(f"\nDataset: {dataset_name}")
    print("-" * 50)
    for folder, count in sorted(count_dict.items()):
        print(f"{folder}: {count} images")

# Paths to your datasets
dataset_1_path = "dataset"
dataset_2_path = "real_vs_fake"

# Counting images
dataset_1_counts = count_images(dataset_1_path)
dataset_2_counts = count_images(dataset_2_path)

# Displaying results
print_counts(dataset_1_counts, "Dataset 1")
print_counts(dataset_2_counts, "Real vs Fake")

import os
import shutil
from tqdm import tqdm  # Import tqdm for progress bar

# Define source directories
dataset_1_path = "dataset"
dataset_2_path = "real_vs_fake"

# Define destination directory
destination_fake = "DATA/fake"

# Ensure destination directory exists
os.makedirs(destination_fake, exist_ok=True)

# Function to copy all fake images from datasets with tqdm
def merge_fake_images(source_dirs, destination):
    all_images = []

    # Collect all fake image paths
    for folder in source_dirs:
        fake_path = os.path.join(folder, "fake")
        if os.path.exists(fake_path):
            images = [os.path.join(fake_path, img) for img in os.listdir(fake_path)]
            all_images.extend(images)

    # Copy images with progress bar
    for src in tqdm(all_images, desc="Copying fake images", unit="file"):
        dst = os.path.join(destination, os.path.basename(src))
        shutil.copy2(src, dst)  # Copy with metadata

# Define paths to fake image folders
fake_folders = [
    os.path.join(dataset_1_path, "train"),
    os.path.join(dataset_1_path, "test"),
    os.path.join(dataset_1_path, "val"),
    os.path.join(dataset_2_path, "real-vs-fake/train"),
    os.path.join(dataset_2_path, "real-vs-fake/test"),
    os.path.join(dataset_2_path, "real-vs-fake/valid")
]

# Merge fake images with progress bar
merge_fake_images(fake_folders, destination_fake)

print("\nAll fake images have been merged into:", destination_fake)

import os
import shutil
from tqdm import tqdm  # Import tqdm for progress bar

# Define source directories
dataset_1_path = "dataset"
dataset_2_path = "real_vs_fake"

# Define destination directory for real images
destination_real = "DATA/real"

# Ensure destination directory exists
os.makedirs(destination_real, exist_ok=True)

# Function to copy all real images with tqdm progress bar
def merge_real_images(source_dirs, destination):
    all_images = []

    # Collect all real image paths
    for folder in source_dirs:
        real_path = os.path.join(folder, "real")
        if os.path.exists(real_path):
            images = [os.path.join(real_path, img) for img in os.listdir(real_path)]
            all_images.extend(images)

    # Copy images with progress bar
    for src in tqdm(all_images, desc="Copying real images", unit="file"):
        dst = os.path.join(destination, os.path.basename(src))
        shutil.copy2(src, dst)  # Copy with metadata

# Define paths to real image folders
real_folders = [
    os.path.join(dataset_1_path, "train"),
    os.path.join(dataset_1_path, "test"),
    os.path.join(dataset_1_path, "val"),
    os.path.join(dataset_2_path, "real-vs-fake/train"),
    os.path.join(dataset_2_path, "real-vs-fake/test"),
    os.path.join(dataset_2_path, "real-vs-fake/valid")
]

# Merge real images with progress bar
merge_real_images(real_folders, destination_real)

print("\nAll real images have been merged into:", destination_real)

import os

# Define paths to merged fake and real image folders
data_path = "DATA"
folders = ["fake", "real"]

# Function to count images in a folder
def count_images(folder_path):
    return len([img for img in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, img))]) if os.path.exists(folder_path) else 0

# Print the total image count for each category
print("\nMerged Dataset in DATA Folder")
print("-" * 50)

for folder in folders:
    folder_path = os.path.join(data_path, folder)
    image_count = count_images(folder_path)
    print(f"{folder_path}: {image_count} images")

import os
import random

# Define paths
real_folder = "DATA/real"
target_count = 75000  # Target image count to match DATA/fake

# Get all images in the real folder
all_images = [img for img in os.listdir(real_folder) if os.path.isfile(os.path.join(real_folder, img))]

# Calculate how many images to remove
extra_images = len(all_images) - target_count

if extra_images > 0:
    print(f"Removing {extra_images} extra images from {real_folder}...")

    # Randomly select images to remove
    images_to_remove = random.sample(all_images, extra_images)

    # Delete selected images
    for img in images_to_remove:
        os.remove(os.path.join(real_folder, img))

    print(f"Successfully reduced {real_folder} to {target_count} images.")
else:
    print(f"No extra images to remove. {real_folder} already has {target_count} or fewer images.")

import os

# Define paths to merged fake and real image folders
data_path = "DATA"
folders = ["fake", "real"]

# Function to count images in a folder
def count_images(folder_path):
    return len([img for img in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, img))]) if os.path.exists(folder_path) else 0

# Print the total image count for each category
print("\nMerged Dataset in DATA Folder")
print("-" * 50)

for folder in folders:
    folder_path = os.path.join(data_path, folder)
    image_count = count_images(folder_path)
    print(f"{folder_path}: {image_count} images")



import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
from sklearn.model_selection import train_test_split
import shutil
import numpy as np
from PIL import Image
from tqdm import tqdm

# 1. Dataset Class
class DeepFakeDataset(Dataset):
    def __init__(self, dataset_dir, transform=None):
        self.dataset_dir = dataset_dir
        self.transform = transform
        self.images = []
        self.labels = []

        # Prepare list of image paths and their corresponding labels (0 for real, 1 for fake)
        for label_dir in os.listdir(dataset_dir):
            label_path = os.path.join(dataset_dir, label_dir)
            if os.path.isdir(label_path):
                label = 0 if label_dir == "real" else 1  # 0 for real, 1 for fake
                for image_name in os.listdir(label_path):
                    image_path = os.path.join(label_path, image_name)
                    if image_path.endswith(('.jpg', '.jpeg', '.png')):
                        self.images.append(image_path)
                        self.labels.append(label)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = Image.open(self.images[idx])

        # Handle transparency or palette-based images
        if image.mode in ["RGBA", "LA", "P"]:
            image = image.convert("RGBA").convert("RGB")  # Convert to RGBA first, then RGB to discard alpha

        # Handle grayscale images (L mode)
        elif image.mode == "L":
            image = image.convert("RGB")  # Convert grayscale to RGB

        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

# 2. Define Transforms (Augmentation and Normalization)
def get_transforms():
    # Data augmentation for training
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to fit EfficientNetV2
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),  # Random crop for augmentation
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Pre-trained EfficientNetV2 mean
                             std=[0.229, 0.224, 0.225])  # Pre-trained EfficientNetV2 std
    ])

    # Validation and Test transforms (only resizing and normalization)
    valid_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    return train_transform, valid_transform

# 3. Dataset Preparation (Split, Apply Transforms, Create Folders)
def prepare_data(dataset_dir, batch_size=32):
    try:
        # Check if the split data already exists
        split_data_dir = os.path.join(dataset_dir, "split_data")

        if not os.path.exists(split_data_dir):
            # Step 1: Manually create the directory structure for train, val, and test
            os.makedirs(split_data_dir, exist_ok=True)
            train_dir = os.path.join(split_data_dir, "train")
            val_dir = os.path.join(split_data_dir, "val")
            test_dir = os.path.join(split_data_dir, "test")
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(val_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            for dir_name in ["real", "fake"]:
                os.makedirs(os.path.join(train_dir, dir_name), exist_ok=True)
                os.makedirs(os.path.join(val_dir, dir_name), exist_ok=True)
                os.makedirs(os.path.join(test_dir, dir_name), exist_ok=True)



        # Step 4: Create the datasets with proper transforms
        train_transform, valid_transform = get_transforms()

        train_dataset = DeepFakeDataset(os.path.join(split_data_dir, "train"), transform=train_transform)
        valid_dataset = DeepFakeDataset(os.path.join(split_data_dir, "val"), transform=valid_transform)
        test_dataset = DeepFakeDataset(os.path.join(split_data_dir, "test"), transform=valid_transform)

        # Step 5: Create DataLoader for each dataset
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)
        valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)

        return train_loader, valid_loader, test_loader

    except Exception as e:
        print(f"Error preparing dataset: {str(e)}")
        raise



# Define the path to your dataset
dataset_directory = "DATA"  # Replace with your actual dataset directory path

# Define the batch size
batch_size = 64  # You can change this based on your GPU/CPU memory capacity

# Call the function to prepare data and get DataLoaders
train_loader, valid_loader, test_loader = prepare_data(dataset_directory, batch_size)

# Print a sample batch to verify
for images, labels in train_loader:
    print(f"Batch Image Tensor Shape: {images.shape}")
    print(f"Batch Labels: {labels}")
    break  # Only display the first batch


import torch
import torch.nn as nn
from timm import create_model

class EfficientNetV2(nn.Module):
    def __init__(self, num_classes=1, dropout_rate=0.3, pretrained=True):
        super(EfficientNetV2, self).__init__()

        # Load the base model (EfficientNetV2) without the final classification layer
        self.base_model = create_model(
            'tf_efficientnetv2_l',  # Large version of EfficientNetV2
            pretrained=pretrained,  # Use pretrained weights
            num_classes=0  # Remove classification head for custom modifications
        )

        # Get the number of features from the base model
        num_features = self.base_model.num_features

        # Custom classifier
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),  # Global average pooling
            nn.Flatten(),  # Flatten tensor
            nn.Linear(num_features, 512),  # Fully connected layer
            nn.SiLU(),  # Activation
            nn.BatchNorm1d(512),  # Batch normalization
            nn.Dropout(dropout_rate),  # Dropout for regularization
            nn.Linear(512, num_classes),  # Output layer
            nn.Sigmoid() if num_classes == 1 else nn.Identity()  # Sigmoid for binary classification
        )

        # Freeze layers initially
        self.freeze_layers()

    def freeze_layers(self):
        """Freeze all layers except the last few"""
        for param in self.base_model.parameters():
            param.requires_grad = False

        # Unfreeze the last 30 layers
        for param in list(self.base_model.parameters())[-30:]:
            param.requires_grad = True

    def forward(self, x):
        """Forward pass"""
        features = self.base_model.forward_features(x)  # Extract features from base model
        out = self.classifier(features)  # Pass through classifier

        # Fix TracerWarning issue safely
        if not torch.jit.is_scripting():  # Ensures no tracing issues
            if out.dim() > 1 and out.size(1) == 1:  # Use `size(1)` instead of `shape[1]`
                return out.squeeze(1)  # Squeeze only second dimension safely
        return out

    def unfreeze_all(self):
        """Unfreeze all layers"""
        for param in self.parameters():
            param.requires_grad = True

    def freeze_all(self):
        """Freeze all layers"""
        for param in self.parameters():
            param.requires_grad = False

import torch
import torch.optim as optim
import torch.nn as nn
import os
import shutil
from tqdm import tqdm  # Import tqdm for progress bar

# Initialize the model
model = EfficientNetV2(num_classes=1)  # 1 output for binary classification (real vs fake)

# Check if CUDA (GPU) is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Move the model to the selected device (GPU or CPU)
model = model.to(device)

# Define the Loss function (Binary Cross Entropy with logits)
criterion = nn.BCEWithLogitsLoss()  # For binary classification (real/fake)

# Define the Optimizer (Adam optimizer)
optimizer = optim.Adam(model.parameters(), lr=1e-4)  # Learning rate is a hyperparameter

# Scheduler (optional for learning rate decay)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

# Early stopping parameters
patience = 5
best_val_loss = float('inf')
epochs_without_improvement = 0

# Directory to save models
os.makedirs("saved_models", exist_ok=True)

# Tracking lists for plotting
train_losses = []
valid_losses = []
train_accuracies = []
valid_accuracies = []

# Training loop
def train_model(train_loader, valid_loader, num_epochs=20):
    global epochs_without_improvement, best_val_loss

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        # Training phase
        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs} - Training", unit="batch"):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)

            # BCEWithLogitsLoss expects outputs and labels to have the same shape
            loss = criterion(outputs, labels.float())  # Fix: No need for .view(-1, 1) here
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            predicted = (torch.sigmoid(outputs) > 0.5).long()
            train_correct += (predicted == labels.view(-1)).sum().item()  # Fix: Flatten labels for comparison
            train_total += labels.size(0)

        # Calculate training loss and accuracy
        train_loss = train_loss / train_total
        train_accuracy = train_correct / train_total

        # Validation phase
        model.eval()
        valid_loss = 0.0
        valid_correct = 0
        valid_total = 0

        with torch.no_grad():
            for images, labels in tqdm(valid_loader, desc=f"Epoch {epoch+1}/{num_epochs} - Validation", unit="batch"):
                images, labels = images.to(device), labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels.float())  # Fix: No need for .view(-1, 1) here
                valid_loss += loss.item() * images.size(0)

                predicted = (torch.sigmoid(outputs) > 0.5).long()
                valid_correct += (predicted == labels.view(-1)).sum().item()  # Fix: Flatten labels for comparison
                valid_total += labels.size(0)

        # Calculate validation loss and accuracy
        valid_loss = valid_loss / valid_total
        valid_accuracy = valid_correct / valid_total

        # Save metrics for plotting
        train_losses.append(train_loss)
        valid_losses.append(valid_loss)
        train_accuracies.append(train_accuracy)
        valid_accuracies.append(valid_accuracy)

        # Print metrics for each epoch
        print(f"Epoch {epoch+1}/{num_epochs} - Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}")
        print(f"Epoch {epoch+1}/{num_epochs} - Validation Loss: {valid_loss:.4f}, Validation Accuracy: {valid_accuracy:.4f}")

        # Early Stopping: If validation loss has not improved
        if valid_loss < best_val_loss:
            best_val_loss = valid_loss
            epochs_without_improvement = 0

            # Save all model formats (state_dict, full model, checkpoint, TorchScript, ONNX)
            save_model(epoch, model, optimizer, train_loss, valid_loss)
        else:
            epochs_without_improvement += 1

        # If patience is reached, stop training early
        if epochs_without_improvement >= patience:
            print("Early stopping triggered. Stopping training.")
            break

        # Step the learning rate scheduler
        scheduler.step()

    return train_losses, valid_losses, train_accuracies, valid_accuracies



# Model saving function for all formats except ONNX
def save_model(epoch, model, optimizer, train_loss, valid_loss):
    # Save state_dict (weights only)
    torch.save(model.state_dict(), f'saved_models/model_epoch_{epoch+1}_weights.pth')

    # Save the full model (architecture + weights)
    torch.save(model, f'saved_models/model_epoch_{epoch+1}_full.pth')

    # Save checkpoint (model + optimizer states)
    checkpoint = {
        'epoch': epoch + 1,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'train_loss': train_loss,
        'valid_loss': valid_loss
    }
    torch.save(checkpoint, f'saved_models/checkpoint_epoch_{epoch+1}.pth')

    # Save the model for inference (TorchScript)
    model.eval()
    example_input = torch.randn(1, 3, 224, 224).to(device)
    traced_model = torch.jit.trace(model, example_input)
    traced_model.save(f'saved_models/model_epoch_{epoch+1}_traced.pt')

    print(f"Model and checkpoint saved for epoch {epoch+1}")

# %pip install onnx
# %pip install onnxruntime
# import onnx
# print(onnx.__version__)

import matplotlib.pyplot as plt

# Plot loss and accuracy graphs for future use
def plot_metrics():
    epochs = range(1, len(train_losses) + 1)

    # Loss Plot
    plt.figure()
    plt.plot(epochs, train_losses, label='Train Loss')
    plt.plot(epochs, valid_losses, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss per Epoch')
    plt.legend()
    plt.savefig('train_validation_loss.png')

    # Accuracy Plot
    plt.figure()
    plt.plot(epochs, train_accuracies, label='Train Accuracy')
    plt.plot(epochs, valid_accuracies, label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Accuracy per Epoch')
    plt.legend()
    plt.savefig('train_validation_accuracy.png')

    print("Graphs saved as images.")

train_losses, valid_losses, train_accuracies, valid_accuracies = train_model(train_loader, valid_loader, num_epochs=20)

# After training, plot the graphs for loss and accuracy
plot_metrics()

