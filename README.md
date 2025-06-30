### YOLO v11 for Driver Drowsiness Detection
This repository contains a complete, end-to-end pipeline for training a YOLO v11 classification model to detect driver drowsiness using the ultralytics library.  
The project covers every stage of the machine learning lifecycle, from automated data acquisition and cleaning to model evaluation and explainability using GradCAM.

![alt text](https://img.shields.io/badge/Python-3.10-blue.svg)


![alt text](https://img.shields.io/badge/Framework-PyTorch-orange.svg)


![alt text](https://img.shields.io/badge/License-MIT-green.svg)


![alt text](https://img.shields.io/badge/Data-Kaggle-blue.svg)

### Project Highlights
You can test the model in real time here: https://huggingface.co/spaces/mosesb/drowsiness-detection-demo

You can download the model here: https://huggingface.co/mosesb/drowsiness-detection-yolo-cls

### Quick Summary
Accuracy	99.80%	Overall correctness on the test set.
APCER	0.00%	Rate of 'Drowsy' drivers missed (False Negatives).
BPCER	0.41%	Rate of 'Non Drowsy' drivers flagged (False Positives).
ACER	0.21%	Average of APCER and BPCER.

### Acknowledgements

This project uses the following datasets from Kaggle:
Driver Drowsiness Dataset (DDD) by ISMAIL NASRI.
Drowsy Detection Dataset by YASHAR JEBRAEILY.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

