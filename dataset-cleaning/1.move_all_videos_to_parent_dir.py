import os
import shutil

# List of video file extensions to look for
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mpeg', '.mpg'}

def move_videos_to_parent_dir(parent_dir):
    # Walk through the directory tree starting from the parent directory
    for dirpath, dirnames, filenames in os.walk(parent_dir, topdown=False):
        # Loop through all files in the current directory
        for filename in filenames:
            # Get the full path of the file
            file_path = os.path.join(dirpath, filename)
            # Check if the file is a video by its extension
            if any(file_path.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                # Move the video to the parent directory
                try:
                    parent_file_path = os.path.join(parent_dir, filename)
                    # Avoid overwriting by renaming if a file with the same name already exists
                    counter = 1
                    while os.path.exists(parent_file_path):
                        new_filename = f"{os.path.splitext(filename)[0]}_{counter}{os.path.splitext(filename)[1]}"
                        parent_file_path = os.path.join(parent_dir, new_filename)
                        counter += 1
                    # Move the video file
                    shutil.move(file_path, parent_file_path)
                    print(f"Moved: {file_path} -> {parent_file_path}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")

# use a raw string so it won’t try to treat backslashes as escape sequences
parent_directory = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Evaluation Dataset'

move_videos_to_parent_dir(parent_directory)
