"""
requirements.txt: opencv-python scipy
"""
import cv2 
import numpy as np
from pathlib import Path




def extract_frames(video_path: str, video_name: str, output_dir: str):
        """Extract frames with drowsiness-related events"""
        _skipped_frames = 0
        skipped_frames = 0
        prev_frame = None

        print(f"Processing video: {video_path}")
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        frame_count = 0
        saved_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Frame difference detection
            if prev_frame is not None:
                frame_diff = cv2.absdiff(prev_frame, frame)
                non_zero_count = np.count_nonzero(frame_diff)        
                # If difference is small, skip
                if non_zero_count < 500000:  # Adjust threshold for sensitivity
                    _skipped_frames +=1
                    continue

            if skipped_frames != _skipped_frames:
                print(f"Skipped {abs(skipped_frames - _skipped_frames)} Frame/s")
                skipped_frames = _skipped_frames

            output_folder = output_dir
            output_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

            frame_name = f"frame_{frame_count:06d}_{video_name}"
            output_path = output_folder / f"{frame_name}.jpg"
            cv2.imwrite(str(output_path), frame)
            saved_count += 1
            prev_frame = frame
            frame_count += 1  
        cap.release()
        print(f"Extracted {saved_count} event frames from {frame_count} total frames")


def convert_videos_to_images(input_dir: str, output_dir: str):
    # """Process all videos in a directory"""
    input_dir = Path(input_dir)
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mpeg', '.mpg'}
    # Loop through each video extension and search for files
    for ext in VIDEO_EXTENSIONS:
        for video_path in input_dir.glob(f"*{ext}"):
            video_name = video_path.stem
            video_output_dir = Path(output_dir) / video_name
            extract_frames(str(video_path), str(video_name), str(video_output_dir))
    

input_dir=r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Training Dataset\Drowsy'
output_dir=r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Training Dataset Images\Drowsy'
convert_videos_to_images(input_dir, output_dir)

input_dir=r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Training Dataset\Awake'
output_dir=r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Training Dataset Images\Awake'
convert_videos_to_images(input_dir, output_dir)