import os
import time
import cv2
import mediapipe as mp


MODEL_PATH = "hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("hand_landmarker.task file not found!")
    print("Download it first using:")
    print('Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "hand_landmarker.task"')
    exit()


# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = HandLandmarker.create_from_options(options)


# Landmark connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17)
]


def draw_landmarks(frame, landmarks):
    h, w, _ = frame.shape
    points = []

    for lm in landmarks:
        x = int(lm.x * w)
        y = int(lm.y * h)
        points.append((x, y))

    for start, end in HAND_CONNECTIONS:
        cv2.line(frame, points[start], points[end], (0, 255, 0), 2)

    for point in points:
        cv2.circle(frame, point, 5, (0, 0, 255), -1)


def fingers_up(landmarks):
    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index finger
    if landmarks[8].y < landmarks[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle finger
    if landmarks[12].y < landmarks[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Ring finger
    if landmarks[16].y < landmarks[14].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Little finger
    if landmarks[20].y < landmarks[18].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers


def detect_gesture(landmarks):
    fingers = fingers_up(landmarks)

    if fingers == [0, 0, 0, 0, 0]:
        return "Fist", "Stop"

    elif fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up", "Volume Up"

    elif fingers == [0, 1, 0, 0, 0]:
        return "Index Finger", "Select"

    elif fingers == [0, 1, 1, 0, 0]:
        return "Two Fingers", "Screenshot"

    elif fingers == [0, 1, 1, 1, 0]:
        return "Three Fingers", "Next Slide"

    elif fingers == [0, 1, 1, 1, 1]:
        return "Four Fingers", "Previous Slide"

    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Hand", "Start"

    else:
        return "Unknown Gesture", "None"


# Stable output variables
previous_gesture = ""
gesture_count = 0
confirmed_gesture = "No Hand"
confirmed_action = "None"


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found!")
    exit()


while True:
    success, frame = cap.read()

    if not success:
        print("Camera frame not received!")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms = int(time.time() * 1000)

    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    current_gesture = "No Hand"
    current_action = "None"

    if result.hand_landmarks:
        hand_landmarks = result.hand_landmarks[0]

        draw_landmarks(frame, hand_landmarks)

        current_gesture, current_action = detect_gesture(hand_landmarks)

    if current_gesture == previous_gesture:
        gesture_count += 1
    else:
        gesture_count = 0

    previous_gesture = current_gesture

    if gesture_count >= 5:
        confirmed_gesture = current_gesture
        confirmed_action = current_action

    cv2.putText(
        frame,
        "Gesture: " + confirmed_gesture,
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        "Action: " + confirmed_action,
        (30, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to exit",
        (30, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
landmarker.close()