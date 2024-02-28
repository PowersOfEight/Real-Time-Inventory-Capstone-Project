import os
import cv2
from ultralytics import YOLO
import supervision as sv
import tkinter as tk
from tkinter import filedialog

# Load the YOLOv8 model
model = YOLO('car_det_model_0.3.pt')

# Create and hide the Tkinter root window
root = tk.Tk()
root.withdraw()

# Prompt the user to select the directory containing images
images_dir = filedialog.askdirectory(title="Select Directory Containing Images")
annotations_dir = os.path.join(images_dir, "annotations")

# Ensure the annotations directory exists
os.makedirs(annotations_dir, exist_ok=True)

if images_dir:
    for img_name in os.listdir(images_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(images_dir, img_name)
            image = cv2.imread(file_path)
            height, width = image.shape[:2]  # Get image dimensions
            results = model(image)
            detections = sv.Detections.from_ultralytics(results[0])  # Extract detections

            # Use OBB data from detections.data['xyxyxyxy'] if available
            if 'xyxyxyxy' in detections.data:
                obb_coords = detections.data['xyxyxyxy']

                annotation_path = os.path.join(annotations_dir, os.path.splitext(img_name)[0] + ".txt")
                with open(annotation_path, 'w') as f:
                    for obb in obb_coords:
                        # Normalize coordinates to be between 0 and 1
                        normalized_obb = obb.flatten()
                        normalized_obb[::2] /= width  # Normalize x-coordinates
                        normalized_obb[1::2] /= height  # Normalize y-coordinates
                        coords_str = ' '.join(map(str, normalized_obb))
                        # Write class_id (0 for cars) followed by the normalized OBB coordinates
                        f.write(f"0 {coords_str}\n")
else:
    print("No directory selected.")
