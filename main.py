from flask import Flask, request, Response, redirect, url_for
import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class SimpleColor:
    def __init__(self, rgb_tuple):
        # OpenCV uses BGR format, so we reverse the RGB tuple
        self.bgr = rgb_tuple[::-1]
    
    def as_bgr(self):
        return self.bgr


@app.route('/')
def index():
    # return app.send_static_file('./index.html')
    return app.send_static_file('index2.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video_file' not in request.files:
        return redirect(request.url)
    file = request.files['video_file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('stream', video_path=filepath))


@app.route('/stream')
def stream():
    video_path = request.args.get('video_path')
    if not video_path or not os.path.exists(video_path):
        return "Video file not found.", 404

    return Response(generate_frames(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames(video_path):
    model = YOLO('car_det_model_0.6.pt')
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Your existing processing logic here
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
        my_color = SimpleColor((255, 255, 0))
        oriented_box_annotator = sv.OrientedBoxAnnotator(color=my_color,thickness=4)
        annotated_frame = oriented_box_annotator.annotate(
            scene=frame,
            detections=high_conf_detections
        )

        # Overlay the confidence score for each high confidence car detected
        font = cv2.FONT_HERSHEY_SIMPLEX
        for bbox, conf in zip(high_conf_detections.xyxy, high_conf_detections.confidence):
            x_center = int((bbox[0] + bbox[2]) / 2)
            y_center = int((bbox[1] + bbox[3]) / 2)
            # To make the text appear as having a black border we will create 
            cv2.putText(annotated_frame, f'{conf:.2f}', (x_center, y_center), font, 0.5, (0, 0, 0), 4,
                        cv2.LINE_AA)
            cv2.putText(annotated_frame, f'{conf:.2f}', (x_center, y_center), font, 0.5, (255, 255, 255), 2,
                        cv2.LINE_AA)

        # Display car count from high confidence detections only
        cv2.putText(annotated_frame, f'Car Count: {len(high_conf_detections)}', (50, 50), font, 1,
                    (255, 255, 255),
                    2, cv2.LINE_AA)

        # Instead of displaying the frame using cv2.imshow, encode it as JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Yield the frame in the multipart/x-mixed-replace format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

    # Replace 'path/to/your/video.mp4' with the actual video path or consider a dynamic approach
    return Response(generate_frames('path/to/your/video.mp4'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)