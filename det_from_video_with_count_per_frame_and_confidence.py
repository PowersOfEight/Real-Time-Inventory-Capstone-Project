import cv2
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import supervision as sv
import numpy as np

# Initialize the model
model = YOLO('car_det_model_0.6.pt')

# Create and hide the Tkinter root window
root = tk.Tk()
root.withdraw()

# Prompt the user to select a video file
video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4 *.avi")])

if not video_path:
    print("No video file selected.")
    exit()

# Open the video
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame through the model
    results = model(frame)
    detections = sv.Detections.from_ultralytics(results[0])

    # Directly filter detections based on confidence score > 0.8
    high_conf_detections = sv.Detections(
        xyxy=detections.xyxy[np.where(detections.confidence > 0.8)],
        confidence=detections.confidence[np.where(detections.confidence > 0.8)],
        class_id=detections.class_id[np.where(detections.confidence > 0.8)],
        data={'xyxyxyxy': detections.data['xyxyxyxy'][np.where(detections.confidence > 0.8)]}
    )

    # Annotate the frame with oriented bounding boxes for high confidence detections
    oriented_box_annotator = sv.OrientedBoxAnnotator(thickness=4)
    annotated_frame = oriented_box_annotator.annotate(
        scene=frame,
        detections=high_conf_detections
    )

    # Overlay the confidence score for each high confidence car detected
    font = cv2.FONT_HERSHEY_SIMPLEX
    for bbox, conf in zip(high_conf_detections.xyxy, high_conf_detections.confidence):
        x_center = int((bbox[0] + bbox[2]) / 2)
        y_center = int((bbox[1] + bbox[3]) / 2)
        cv2.putText(annotated_frame, f'{conf:.2f}', (x_center, y_center), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Display car count from high confidence detections only
    cv2.putText(annotated_frame, f'Car Count: {len(high_conf_detections)}', (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Video', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
