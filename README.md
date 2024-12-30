# Drowsy Detection with YOLOv11

This repository contains the full implementation of a drowsy detection system, leveraging the YOLO (You Only Look Once) object detection algorithm fine-tuned for the "awake" and "drowsy" datasets. The project uses the Python `ultralytics` library for training and inference.

## Table of Contents
- [Dataset](#dataset)
- [Files and Structure](#files-and-structure)
- [Training Process Overview](#training-process-overview)
- [Dependencies and Requirements](#dependencies-and-requirements)
- [Key Results](#key-results)
- [Citation](#citation)

---

## Dataset

The dataset used for training can be downloaded from the following link:  
[Complete YOLO Drowsy Images Dataset](https://firebasestorage.googleapis.com/v0/b/electora-8c1d6.appspot.com/o/Complete%20YOLO%20Drowsy%20Images%20Dataset.zip?alt=media)

The dataset includes annotated images in YOLO format, with labels specifying the "awake" and "drowsy" states.

---

## Files and Structure

### Repository Structure:
```plaintext
│ notebook.ipynb               # Initial training session
│ notebook2.ipynb              # Resumed training session
├─training_and_testing_files:  # Outputs and intermediate results
│   args.yaml
│   confusion_matrix.png
│   confusion_matrix_normalized.png
│   F1_curve.png
│   labels.jpg
│   labels_correlogram.jpg
│   PR_curve.png
│   P_curve.png
│   results.csv
│   results.png
│   results1.png
│   results2.png
│   results3.png
│   results4.png
│   results5.png
│   R_curve.png
│   train_batch*.jpg
│   val_batch*_labels.jpg
│   val_batch*_pred.jpg
├─.ipynb_checkpoints:          # Checkpointed files
└─pics:                        # Selected visualization outputs
    confusion_matrix.png
    F1_curve.png
    labels.jpg
    train_batch34880.jpg
    val_batch1_pred.jpg
```

---

## Training Process Overview

1. **Dataset Loading:**
   - YOLO utilizes a `yaml` file to define the paths for training and validation datasets and their corresponding class labels.

2. **Key Parameters for Training:**
   - **Epochs:** The model was trained for 50 epochs to balance learning and avoiding overfitting.
   - **Image Size:** All input images were resized to 640x640 pixels to match YOLO's expected square input format.
   - **Batch Size:** A batch size of 16 was used to optimize training efficiency.

3. **Hardware and Framework:**
   - **Framework:** PyTorch backend via the `ultralytics` library.
   - **Hardware:** Training and inference were performed on an Nvidia RTX 3080 GPU.

---

## Dependencies and Requirements

- Python 3.8+
- Key Python libraries:
  - `ultralytics` for YOLO-based training and inference
  - `torch` and `torchvision` for PyTorch operations
  - `numpy`, `matplotlib`, and `pandas` for data processing and visualization
- GPU with CUDA support (recommended: Nvidia RTX 3080 or higher)

Install dependencies using the following command:
```bash
pip install ultralytics torch torchvision numpy matplotlib pandas
```

---

## Key Results

- **Performance Metrics:**
  - Confusion Matrix: `confusion_matrix.png` and `confusion_matrix_normalized.png`
  - Precision-Recall (PR) Curve: `PR_curve.png`
  - F1 Curve: `F1_curve.png`
  - Results stored in `results.csv` and visualized in `results*.png`

- **Visualizations:**
  - Training Batches: `train_batch*.jpg`
  - Validation Predictions: `val_batch*_pred.jpg`

---

## Citation

If you use this repository in your research, please cite it using the following DOI link:  
[DOI Placeholder]()

Feel free to open issues or pull requests if you encounter any problems or have suggestions for improvement.

--- 

**License:** This project is licensed under the MIT License. See `LICENSE` for details.
