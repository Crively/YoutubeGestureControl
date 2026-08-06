import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.landmarks = None
        self.handedness = None

    def find_hands(self, frame, draw=True):
        """Detecta as mãos no frame e retorna os landmarks"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                self.landmarks = hand_landmarks.landmark
                self.handedness = self.results.multi_handedness[0].classification[0].label
        else:
            self.landmarks = None
            
        return frame

    def get_landmarks(self):
        """Retorna os 21 pontos da mão em coordenadas normalizadas (0-1)"""
        if self.landmarks:
            return [(lm.x, lm.y, lm.z) for lm in self.landmarks]
        return None

    def get_finger_positions(self, frame_shape):
        """Retorna as posições dos dedos em pixels (para desenho)"""
        h, w, _ = frame_shape
        if self.landmarks:
            return [(int(lm.x * w), int(lm.y * h)) for lm in self.landmarks]
        return None
