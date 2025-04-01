"""


requirements.txt: opencv-python cmake dlib-19.24.99-cp312-cp312-win_amd64.whl

Here, In the Drowsy dataset, An open mouth detected is most likely a yawn and not a laugh or someone talking,
so open mouth detected is used as part of the features for sorting a frame as drowsy, another feature used is if the eyes are open or closed eyes.

"""


import dlib
import cv2
from PIL import Image
import numpy as np
import logging
import os
import random
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DRAW_BOUNDING_BOXES = False


@dataclass
class DrowsinessEvent:
    name: str
    timestamp: float
    details: dict


class FeatureExtractor:
    frame_count = 0
    saved_count = 0

    def __init__(self):
        # Initialize the dlib face detector and landmark predictor
        self.face_detector = dlib.get_frontal_face_detector()
        my_path = os.path.abspath(__file__) # Get the filepath to the current script
        predictor_model = os.path.join(os.path.dirname(my_path), 'shape_predictor_68_face_landmarks.dat')
        logger.info(f"Found shape_predictor file: {os.path.exists(predictor_model)}")
        self.landmark_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # path to dlib landmark predictor
        logger.info(f"Loaded dlib face detector and landmark predictor")


    def detect_events(self, frame):
        """Detect drowsiness events in a frame using dlib"""
        event = None
        modified_frame = None
        face_boxes = []
        timestamp = datetime.now().timestamp()
        img_height, img_width = frame.shape[:2]
        # Small the frame
        frame =  cv2.resize(frame, (224, 224))

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_detector(gray)
        
        # Big the frame
        frame =  cv2.resize(frame, (img_width, img_height))

        if len(faces) > 0:
            for face in faces:
                # Get the bounding box for the face on the smaller frame
                x, y, w, h = (face.left(), face.top(), face.width(), face.height())

                # Scale bounding box coordinates back to the original frame size
                scale_x = img_width / 224
                scale_y = img_height / 224
                x = int(x * scale_x)
                y = int(y * scale_y)
                w = int(w * scale_x)
                h = int(h * scale_y)


                if DRAW_BOUNDING_BOXES:
                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
                face_boxes.append((x, y, w, h))

                # Detect landmarks
                landmarks = self.landmark_predictor(gray, face)
                eyes, eyes_distance = self.detect_eyes(landmarks)
                mouth_open, mouth_distance = self.detect_mouth(landmarks)

                if DRAW_BOUNDING_BOXES:
                    #Draw the facial landmarks on the frame
                    for i in range(68):
                        x = landmarks.part(i).x
                        y = landmarks.part(i).y
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)


                # Check if eyes are open and mouth is open (yawn detection)
                if eyes and not mouth_open:
                    event = DrowsinessEvent(
                        name="awake",
                        timestamp=timestamp,
                        details={"eyes_open": eyes, "eyes_distance": eyes_distance, "detected_faces": len(faces), "mouth_open": mouth_open, "mouth_distance": mouth_distance}
                    )
                elif eyes and mouth_open:
                    event = DrowsinessEvent(
                        name="drowsy",
                        timestamp=timestamp,
                        details={"eyes_open": eyes, "eyes_distance": eyes_distance, "detected_faces": len(faces), "mouth_open": mouth_open, "mouth_distance": mouth_distance}
                    )
                else:
                    event = DrowsinessEvent(
                        name="drowsy",
                        timestamp=timestamp,
                        details={"eyes_open": eyes, "eyes_distance": eyes_distance, "detected_faces": len(faces), "mouth_open": mouth_open, "mouth_distance": mouth_distance}
                    )
        else:
            event = DrowsinessEvent(
                name="unknown",
                timestamp=timestamp,
                details={"detected_faces": 0}
            )
        if DRAW_BOUNDING_BOXES:
            modified_frame = frame
        return event, modified_frame, face_boxes
        

    def eye_aspect_ratio(self, eye_points):
        # Calculate distances between the vertical eye landmarks
        A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
        B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
        # Calculate the distance between the horizontal eye landmarks
        C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
        # Calculate EAR
        ear = (A + B) / (2.0 * C)
        return ear

    def detect_eyes(self, landmarks):
        """Detect if eyes are open based on eye aspect ratio (EAR). Returns True if eyes are open, False if closed."""
        # Extract points for left and right eyes
        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

        # Calculate EAR for both eyes
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)

        # Average EAR and define threshold
        ear = (left_ear + right_ear) / 2.0
        EAR_THRESHOLD = 0.4

        eyes_open = ear > EAR_THRESHOLD
        return eyes_open, ear

    def detect_mouth(self, landmarks):
        """Detect if mouth is open based on the landmarks (mouth range is 48-67)"""
        mouth_open = None
        # Mouth corners (48-54) and mouth width (48-54 distances)
        top_lip = landmarks.part(51).y
        bottom_lip = landmarks.part(57).y
        mouth_height = bottom_lip - top_lip
        if mouth_height > 18:  # Threshold for mouth being open (adjust as needed)
            mouth_open = True
        else:
            mouth_open = False
        return mouth_open, mouth_height

    def normalize_bbox(self, x, y, w, h, img_width, img_height):
        """Convert bounding box to YOLO format (center_x, center_y, width, height) with normalized values."""
        x_center = (x + w / 2) / img_width
        y_center = (y + h / 2) / img_height
        w_norm = w / img_width
        h_norm = h / img_height
        return x_center, y_center, w_norm, h_norm

    def extract_frames(self, image_path: str, image_name: str, output_dir: str):
        """sort frames by drowsiness-related events"""
        img = Image.open(image_path)
        print(img.size)
        # convert image to numpy array, resize and gray out the color.           
        frame = np.asarray(img)

        # Detect drowsiness events
        event, modified_frame, face_boxes = self.detect_events(frame)
        event.details["name"] = image_name
        img_height, img_width = frame.shape[:2]

        if modified_frame is not None:
            frame = modified_frame

       # Create 2 new folders based on event.name
        output_folder = os.path.join(output_dir, "images", str(event.name))
        os.makedirs(output_folder, exist_ok=True)
        output_folder_labels = os.path.join(output_dir, "labels")
        os.makedirs(output_folder_labels, exist_ok=True)
        
        # write the image and labels annotation text file to disk
        output_path = os.path.join(output_folder, str(image_name))
        txt_output_path = os.path.join(output_folder_labels, str(image_name[:-4] + ".txt"))
        cv2.imwrite(str(output_path), frame)  

        # Write annotation in YOLO format
        with open(txt_output_path, "w") as file:
            for (x, y, w, h) in face_boxes:
                x_center, y_center, w_norm, h_norm = self.normalize_bbox(x, y, w, h, img_width, img_height)
                if event.name == "awake":
                    class_id = 0  
                else:
                    class_id = 1
                file.write(f"{class_id} {x_center} {y_center} {w_norm} {h_norm}\n")
        return event


        




def sort_images_dataset_by_features(input_dir: str, output_dir: str):
    # """Process all videos in a directory"""
    extractor = FeatureExtractor()
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frame_count = 1

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # skip glasses dataset, it's hard to sort drowsy images with glasses
            image_directory = os.path.basename(root)
            print(image_directory)
            if image_directory.lower().startswith('z'):
                print("The image folder starts with 'z' so it is a dataset with glasses, skipping")
                continue
            
            image_name = file
            image_path = os.path.join(root, file)
            event = extractor.extract_frames(str(image_path), str(image_name), str(output_dir))
            logger.info(f"No. {frame_count}:   Detected event: {(event.name, event.details)}")
            frame_count += 1




if __name__ == "__main__":
    input_dir=r'/storage/emulated/0/python/DrowsyDetection/TrainingDatasetImages/Drowsy'
    output_dir=r'/storage/emulated/0/python/DrowsyDetection/SortedDrowsy'
    os.makedirs(output_dir, exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create a formatter that includes timestamp, log level, and message
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    # Create a file handler that logs to a file (appending to 'app.log')
    file_handler = logging.FileHandler(os.path.join(output_dir, 'sort_images_by_features_drowsy.log'), mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    sort_images_dataset_by_features(input_dir, output_dir)
    

