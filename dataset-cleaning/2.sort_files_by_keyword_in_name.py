import os
import shutil

def sort_files_by_keyword_in_name(parent_path):
    # Check if the parent path exists
    if not os.path.exists(parent_path):
        print(f"The provided path '{parent_path}' does not exist.")
        return

    # Create folder1 and folder2 inside the parent path if they don't exist
    folder1 = os.path.join(parent_path, 'Awake')
    folder2 = os.path.join(parent_path, 'Drowsy')

    # Create the folders if they do not exist
    os.makedirs(folder1, exist_ok=True)
    os.makedirs(folder2, exist_ok=True)

    # Iterate over all files in the parent directory
    for filename in os.listdir(parent_path):
        file_path = os.path.join(parent_path, filename)
        
        # Skip directories, only process files
        if os.path.isdir(file_path):
            continue
        
        # Check if the filename contains the word "nonsleepy"
        if "nonsleepy" in filename:
            # Move to folder1
            shutil.move(file_path, os.path.join(folder1, filename))
            print(f"Moved '{filename}' to folder1.")
        else:
            # Move to folder2
            shutil.move(file_path, os.path.join(folder2, filename))
            print(f"Moved '{filename}' to folder2.")

# use a raw string so it won’t try to treat backslashes as escape sequences
parent_path = r'C:\Users\Moses\Desktop\Movie Website\Drowsy Detection\Complete NTHU Video Dataset\Training Dataset'
sort_files_by_keyword_in_name(parent_path)
