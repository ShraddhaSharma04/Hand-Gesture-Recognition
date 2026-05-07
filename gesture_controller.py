def fingers_up(landmarks):
    fingers = []

    if len(landmarks) == 0:
        return []

    # Thumb
    if landmarks[4][1] > landmarks[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index finger
    if landmarks[8][2] < landmarks[6][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle finger
    if landmarks[12][2] < landmarks[10][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Ring finger
    if landmarks[16][2] < landmarks[14][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Little finger
    if landmarks[20][2] < landmarks[18][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers


def detect_gesture(landmarks):
    fingers = fingers_up(landmarks)

    if len(fingers) == 0:
        return "No Hand"

    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"

    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Hand"

    elif fingers == [0, 1, 0, 0, 0]:
        return "Index Finger"

    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace Sign"

    elif fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up"

    else:
        return "Unknown Gesture"


def perform_action(gesture):
    if gesture == "Fist":
        return "Action: Stop / Pause"

    elif gesture == "Open Hand":
        return "Action: Start / Play"

    elif gesture == "Index Finger":
        return "Action: Select / Point"

    elif gesture == "Peace Sign":
        return "Action: Screenshot"

    elif gesture == "Thumbs Up":
        return "Action: Volume Up"

    else:
        return "Action: None"