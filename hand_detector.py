import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def find_hand_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb_frame)

        landmarks = []

        if result.multi_hand_landmarks:
            hand_landmark = result.multi_hand_landmarks[0]

            for id, lm in enumerate(hand_landmark.landmark):
                h, w, c = frame.shape
                x = int(lm.x * w)
                y = int(lm.y * h)
                landmarks.append((id, x, y))

            self.mp_draw.draw_landmarks(
                frame,
                hand_landmark,
                self.mp_hands.HAND_CONNECTIONS
            )

        return landmarks