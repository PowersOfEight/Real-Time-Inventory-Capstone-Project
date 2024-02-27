import cv2
import os


def extract_frames(video_path, output_folder, frame_rate):
    # Make sure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Capture video
    vidcap = cv2.VideoCapture(video_path)

    # Get video FPS (Frames Per Second)
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    success, image = vidcap.read()
    count = 0
    extracted_count = 515

    while success:
        # Current frame number
        frame_id = int(round(vidcap.get(1)))

        # Check if the current frame number is divisible by the number of frames to skip
        if frame_id % int(round(fps / frame_rate)) == 0:
            # Save frame as JPEG file
            cv2.imwrite(os.path.join(output_folder, f"car_det_{extracted_count:04d}.jpg"), image)
            print(f'Extracted frame {extracted_count} at second {frame_id // fps}')
            extracted_count += 1

        success, image = vidcap.read()
        count += 1


if __name__ == "__main__":
    video_path = 'dji_air2_02212024_25meter_06_1280x720.mp4'  # Update this to the path of your video
    output_folder = 'venv/image output8'  # Update this to your desired output folder
    frame_rate = 0.5  # Extract one frame per second
    extract_frames(video_path, output_folder, frame_rate)
