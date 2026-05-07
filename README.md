# Hand Gesture Recognition System

A real-time hand gesture recognition project built using **Python, OpenCV, and MediaPipe**.  
This project uses a webcam to detect hand landmarks and recognize gestures such as Fist, Thumbs Up, Index Finger, Two Fingers, Three Fingers, Four Fingers, and Open Hand.

---

## Project Overview

This project detects hand gestures in real time using a webcam.  
It uses **MediaPipe Hand Landmarker** to detect 21 hand landmarks and then applies simple logic to identify which fingers are open or closed.

Based on the detected gesture, the system displays a related action on the screen.

---

## Features

- Real-time webcam-based hand detection
- Detects 21 hand landmarks using MediaPipe
- Recognizes multiple hand gestures
- Displays gesture name on the screen
- Displays one action for each gesture
- Uses stability logic to reduce wrong detection
- Simple and easy-to-understand Python code
- Useful for practical exams, mini projects, and viva

---

## Tech Stack

| Technology | Use |
|---|---|
| Python | Main programming language |
| OpenCV | Webcam access and image display |
| MediaPipe | Hand landmark detection |
| NumPy | Basic numerical support |

---

## Gestures and Actions

| Gesture | Action |
|---|---|
| Fist | Stop |
| Thumbs Up | Volume Up |
| Index Finger | Select |
| Two Fingers | Screenshot |
| Three Fingers | Next Slide |
| Four Fingers | Previous Slide |
| Open Hand | Start |

---

## Project Structure

```text
Hand-Gesture-Recognition/
│
├── main.py
├── requirements.txt
├── hand_landmarker.task
├── README.md
├── HandRecognition.ipynb
├── hand_detector.py
└── gesture_controller.py