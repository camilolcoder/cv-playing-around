import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.draw_utils = mp.solutions.drawing_utils

    def aperture(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb)
        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0]
            t, i = lm.landmark[4], lm.landmark[8]
            return float(np.hypot(t.x - i.x, t.y - i.y))
        return None

    def draw(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb)
        if res.multi_hand_landmarks:
            self.draw_utils.draw_landmarks(
                frame, res.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS
            )
        return frame