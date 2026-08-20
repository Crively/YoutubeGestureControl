import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, static_mode=False, max_hands=1, min_detection_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.smooth_factor = 0.3
        self.prev_landmarks = None
        self.detected = False
        
    def find_hands(self, frame, draw=True):
        """Detecta mãos no frame e desenha se solicitado"""
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
                    
                if self.prev_landmarks is not None:
                    smoothed_landmarks = []
                    for i, point in enumerate(hand_landmarks.landmark):
                        smoothed_point = type('', (), {})()
                        smoothed_point.x = self.prev_landmarks[i].x * (1 - self.smooth_factor) + point.x * self.smooth_factor
                        smoothed_point.y = self.prev_landmarks[i].y * (1 - self.smooth_factor) + point.y * self.smooth_factor
                        smoothed_point.z = self.prev_landmarks[i].z * (1 - self.smooth_factor) + point.z * self.smooth_factor
                        smoothed_landmarks.append(smoothed_point)
                    
                    self.prev_landmarks = smoothed_landmarks
                    self.detected = True
                    return frame, smoothed_landmarks
                else:
                    self.prev_landmarks = list(hand_landmarks.landmark)
                    self.detected = True
                    return frame, hand_landmarks.landmark
        
        self.detected = False
        self.prev_landmarks = None
        return frame, None
    
    def get_landmarks(self):
        """Retorna os landmarks atuais ou None se não detectado"""
        return self.prev_landmarks if self.detected else None
