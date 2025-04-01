

"""
# Optmiized way to delete all .txt files in a large directory and including its subdirectories
import fnmatch
import os 
def delete_txt_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.txt'):
            file_path = os.path.join(dirpath, filename)
            try:
                os.remove(file_path)
                print(f'Deleted: {file_path}')
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
                
input_dir=r'/storage/emulated/0/python/DrowsyDetection/TrainingDatasetImages'
delete_txt_files(input_dir)
"""


"""
#The code moves image files from a source folder to a destination folder and also moves their corresponding label text files based on matching filenames.
import os
import shutil

# Define source and destination directories
source_images = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete DrowsyDataset-Images\Awake\images\drowsy'
destination_images = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete DrowsyDataset-Images\Drowsy\images\drowsy'
source_labels = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete DrowsyDataset-Images\Awake\labels'
destination_labels = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete DrowsyDataset-Images\Drowsy\labels'

# Iterate through the image files in the source directory
for filename in os.listdir(source_images):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Assuming image files have .jpg or .png extension
        image_file = os.path.join(source_images, filename)
        label_file = os.path.join(source_labels, filename.replace('.jpg', '.txt').replace('.png', '.txt'))  # Assuming label files are .txt
        
        # Check if the corresponding label file exists
        if os.path.exists(label_file):
            # Define the destination paths for image and label
            destination_image_file = os.path.join(destination_images, filename)
            destination_label_file = os.path.join(destination_labels, os.path.basename(label_file))

            # Move the image file
            shutil.move(image_file, destination_image_file)
            print(f"Moved image file: {image_file} to {destination_image_file}")

            # Move the label file
            shutil.move(label_file, destination_label_file)
            print(f"Moved label file: {label_file} to {destination_label_file}")
        else:
            print(f"Label file for {filename} not found")
            raise

"""



"""
# This code will go through all the .txt files in a specified directory, check if they are empty, and delete those that are empty.
import os

# Define the directory where the text files are located
directory = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete DrowsyDataset-Images\Awake\labels'
files = []
# Iterate through each file in the directory
for filename in os.listdir(directory):
    # Create the full file path
    file_path = os.path.join(directory, filename)
    
    # Check if the file is a .txt file
    if filename.endswith('.txt'):
        # Open the file and check if it is empty
        with open(file_path, 'r') as file:
            if not file.read().strip():  # If the file is empty or contains only whitespace
                files.append(file_path)
                print(f"Appended empty file: {filename}")
                            
                            
                            
for file_path in files:
    os.remove(file_path)
    print(f"Deleted empty file: {file_path}")
"""


"""
# merge all dataset files to one images and labels folder.
import os
import shutil

source_images = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\Awake\images'
destination_images = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\Drowsy\images'
source_labels = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\Awake\labels'
destination_labels = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\Drowsy\labels'

# Iterate through the image files in the source directory
for filename in os.listdir(source_images):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Assuming image files have .jpg or .png extension
        image_file = os.path.join(source_images, filename)
        label_file = os.path.join(source_labels, filename.replace('.jpg', '.txt').replace('.png', '.txt'))  # Assuming label files are .txt
        
        # Check if the corresponding label file exists
        if os.path.exists(label_file):
            # Define the destination paths for image and label
            destination_image_file = os.path.join(destination_images, filename)
            destination_label_file = os.path.join(destination_labels, os.path.basename(label_file))

            # Move the image file
            shutil.move(image_file, destination_image_file)
            print(f"Moved image file: {image_file} to {destination_image_file}")

            # Move the label file
            shutil.move(label_file, destination_label_file)
            print(f"Moved label file: {label_file} to {destination_label_file}")
        else:
            print(f"Label file for {filename} not found")
            raise
"""

"""
# split 5% of the train dataset into a seperate val dataset
import os
import shutil
import random

# Define source and destination directories
source_images = r"C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\train\images"
destination_images = r"C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\val\images"
source_labels = r"C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\train\labels"
destination_labels = r"C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete YOLO Drowsy Images Dataset\val\labels"

os.makedirs(destination_images, exist_ok=True)
os.makedirs(destination_labels, exist_ok=True)

# Get a list of all image files in the 'images' directory
image_files = [f for f in os.listdir(source_images) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# Select 5% of the image files randomly
num_files_to_select = int(0.05 * len(image_files))  # 5% of the total number of files
selected_files = random.sample(image_files, num_files_to_select)

# Copy the selected images and corresponding labels to the destination directory
for image_name in selected_files:
    # Build paths for the image and its corresponding label file
    image_file = os.path.join(source_images, image_name)
    label_file = os.path.join(source_labels, image_name.replace('.jpg', '.txt').replace('.png', '.txt'))
    
    # Check if the corresponding label file exists
    if os.path.exists(label_file):
            # Define the destination paths for image and label
            destination_image_file = os.path.join(destination_images, image_name)
            destination_label_file = os.path.join(destination_labels, os.path.basename(label_file))

            # Move the image file
            shutil.move(image_file, destination_image_file)
            print(f"Moved image file: {image_file} to {destination_image_file}")

            # Move the label file
            shutil.move(label_file, destination_label_file)
            print(f"Moved label file: {label_file} to {destination_label_file}")
    else:
        print(f"Label file for {image_file} not found.")
        raise
"""
