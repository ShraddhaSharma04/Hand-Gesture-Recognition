import cv2
from hand_detector import HandDetector
from gesture_controller import detect_gesture, perform_action


detector = HandDetector()

cap = cv2.VideoCapture(0)

previous_gesture = ""
gesture_count = 0
confirmed_gesture = "No Hand"

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.flip(frame, 1)

    landmarks = detector.find_hand_landmarks(frame)

    gesture = detect_gesture(landmarks)

    # This makes gesture detection stable
    if gesture == previous_gesture:
        gesture_count += 1
    else:
        gesture_count = 0

    previous_gesture = gesture

    if gesture_count > 10:
        confirmed_gesture = gesture

    action = perform_action(confirmed_gesture)

    cv2.putText(
        frame,
        "Gesture: " + confirmed_gesture,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        action,
        (30, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()