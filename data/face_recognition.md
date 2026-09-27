# Face Recognition V2

A real time face recognition system built with Python, OpenCV, and InsightFace.

The program creates facial embeddings from a local image dataset and uses them to recognize known individuals from a webcam feed. Recognition events are automatically logged to a CSV file.

---

## Features

* Generate facial embeddings from a local image dataset.
* Perform real time webcam face recognition.
* Classify faces as **Recognized** or **Unknown**.
* Log recognition events to a CSV file.

---

## Technologies

* Python
* OpenCV
* InsightFace
* ONNX Runtime
* NumPy

---

## Dataset

The project uses three datasets:

* Images used to generate the facial embedding database.
* Single-face images used for controlled evaluation.
* Group images used for stress testing.

The stress-test dataset includes manually created ground truth containing the expected known identities for each image.

---

## Evaluation

The recognition system was evaluated using two dedicated evaluation processes:

* controlled testing,
* look-alike and group-image stress testing.

The evaluation uses dedicated controlled and stress-test datasets.

### Controlled Evaluation Results

| Metric                 |  Result |
| ---------------------- | ------: |
| Known Accuracy         | 100.00% |
| Unknown Rejection Rate | 100.00% |
| Overall Accuracy       | 100.00% |

---

## Stress Testing

To evaluate the system under more realistic conditions, additional stress tests were performed using group images containing multiple known and unknown individuals.

Each stress-test image is paired with manually created ground truth containing the expected known identities. This allows the system to compare predictions against the expected results and calculate recognition accuracy.

### Stress Test Results

| Metric                           | Result |
| -------------------------------- | -----: |
| Stress Test Images               |     24 |
| Detected Faces                   |    183 |
| Expected Known Faces             |     29 |
| Correctly Recognized Known Faces |     27 |
| False Positive Identities        |      0 |
| Known-Face Stress Accuracy       | 93.10% |
