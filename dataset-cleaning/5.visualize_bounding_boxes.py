import os
import cv2


input_dir=r'/storage/emulated/0/python/DrowsyDetection/SortedDrowsy/images'
labels_dir=r'/storage/emulated/0/python/DrowsyDetection/SortedDrowsy/labels'
output_dir=r'/storage/emulated/0/python/DrowsyDetection/VisualizeYOLOBoundingBoxes'
os.makedirs(output_dir, exist_ok=True)
    
    
    
# Loop through each image in the input folder
for root, dirs, files in os.walk(input_dir):
    for image_filename in files:
        image_path = os.path.join(root, image_filename)
        image_name, image_ext = os.path.splitext(image_filename)
        
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image {image_filename}")
            continue

        # Determine corresponding label file
        label_filename = f"{image_name}.txt"
        label_path = os.path.join(labels_dir, label_filename)

        # Only proceed if label file exists
        if not os.path.isfile(label_path):
            print(f"Label file {label_filename} not found for image {image_filename}")
            continue

        # Read the label file and parse bounding box coordinates
        with open(label_path, 'r') as f:
            for line in f.readlines():
                # Each line in the label file has: class_id, center_x, center_y, width, height
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Invalid format in {label_filename}: {line}")
                    continue
                
                class_id, x_center, y_center, width, height = map(float, parts)
                
                # Convert normalized coordinates to absolute pixel values
                img_h, img_w, _ = image.shape
                x_center_abs = int(x_center * img_w)
                y_center_abs = int(y_center * img_h)
                width_abs = int(width * img_w)
                height_abs = int(height * img_h)
                
                # Calculate the top-left and bottom-right points
                x1 = int(x_center_abs - width_abs / 2)
                y1 = int(y_center_abs - height_abs / 2)
                x2 = int(x_center_abs + width_abs / 2)
                y2 = int(y_center_abs + height_abs / 2)
                
                # Draw the bounding box on the image
                color = (0, 255, 0)  # Green color for the bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                # Optionally, you can put the class label text on the box
                label_text = f"Class {int(class_id)}"
                cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save the image with drawn bounding boxes to the output folder
        output_path = os.path.join(output_dir, image_filename)
        cv2.imwrite(output_path, image)
        print(f"Processed and saved {image_filename}")


