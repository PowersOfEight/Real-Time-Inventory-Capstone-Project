import cv2
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import supervision as sv

# Initialize the model
model = YOLO('car_det_model_0.3.pt')

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

    # Annotate the frame
    oriented_box_annotator = sv.OrientedBoxAnnotator()
    annotated_frame = oriented_box_annotator.annotate(
        scene=frame,
        detections=detections
    )

    # Display the frame
    cv2.imshow('Video', annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when the job is finished
cap.release()
cv2.destroyAllWindows()
