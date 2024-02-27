import cv2
import tkinter as tk
from tkinter import filedialog


def resize_video(input_video_path, output_video_path, new_size=(1280, 720)):
    # Capture the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change 'mp4v' to 'XVID' if you prefer
    out = cv2.VideoWriter(output_video_path, fourcc, fps, new_size)

    # Read and resize each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if there are no frames left

        # Resize the frame
        resized_frame = cv2.resize(frame, new_size)

        # Write the resized frame to the output video
        out.write(resized_frame)

    # Release everything when the job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def select_file():
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Show an "Open" dialog box and return the path to the selected file
    file_path = filedialog.askopenfilename()
    return file_path


# Use the select_file function to choose the input video
input_video = select_file()
if input_video:  # Proceed only if a file was selected
    output_video = input_video.rsplit('.', 1)[0] + '_1280x720.mp4'  # Modify the output file name
    resize_video(input_video, output_video)
    print(f"Video saved as {output_video}")
else:
    print("No file selected.")
