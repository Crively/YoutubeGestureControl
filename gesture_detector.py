import cv2
import numpy as np
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.PINCH_THRESHOLD = 0.08
        self.THUMB_ANGLE_THRESHOLD = 0.02
        self.FIST_THRESHOLD = 0.15
        
    def detect_gesture(self, landmarks):
        """Detecta e classifica o gesto baseado nos landmarks"""
        if landmarks is None:
            return "none"
            
    
        if self._is_fist(landmarks):
            return "fist"
        elif self._is_open_hand(landmarks):
            return "open_hand"
        elif self._is_pinch(landmarks):
            return "pinch"
        elif self._is_peace(landmarks):
            return "peace"
        elif self._is_thumb_up(landmarks):
            return "thumb_up"
        elif self._is_thumb_down(landmarks):
            return "thumb_down"
        else:
            return "none"
    
    def _is_fist(self, landmarks):
        """Detecta punho fechado - todos os dedos dobrados"""
      
        tips = [4, 8, 12, 16, 20]
        bases = [2, 5, 9, 13, 17]
        
        folded_count = 0
        for tip, base in zip(tips, bases):
            
            dist = np.sqrt(
                (landmarks[tip].x - landmarks[base].x)**2 +
                (landmarks[tip].y - landmarks[base].y)**2
            )
            if dist < self.FIST_THRESHOLD:
                folded_count += 1
        
        return folded_count >= 4
    
    def _is_open_hand(self, landmarks):
        """Detecta mão aberta - todos os dedos estendidos"""
        tips = [8, 12, 16, 20] 
        bases = [5, 9, 13, 17]
        
        extended_count = 0
        for tip, base in zip(tips, bases):
            dist = np.sqrt(
                (landmarks[tip].x - landmarks[base].x)**2 +
                (landmarks[tip].y - landmarks[base].y)**2
            )
            if dist > self.FIST_THRESHOLD * 1.5:
                extended_count += 1
        
        return extended_count >= 3 
    
    def _is_pinch(self, landmarks):
        """Detecta gesto de pinça - polegar e indicador juntos"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        dist = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 +
            (thumb_tip.y - index_tip.y)**2
        )
        
        return dist < self.PINCH_THRESHOLD
    
    def _is_peace(self, landmarks):
        """Detecta gesto de paz (V) - indicador e médio estendidos"""
        index_tip = landmarks[8]
        index_base = landmarks[5]
        middle_tip = landmarks[12]
        middle_base = landmarks[9]
        ring_tip = landmarks[16]
        ring_base = landmarks[13]
        pinky_tip = landmarks[20]
        pinky_base = landmarks[17]
        
        index_extended = np.sqrt(
            (index_tip.x - index_base.x)**2 +
            (index_tip.y - index_base.y)**2
        ) > self.FIST_THRESHOLD * 1.5
        
        middle_extended = np.sqrt(
            (middle_tip.x - middle_base.x)**2 +
            (middle_tip.y - middle_base.y)**2
        ) > self.FIST_THRESHOLD * 1.5
        
        ring_folded = np.sqrt(
            (ring_tip.x - ring_base.x)**2 +
            (ring_tip.y - ring_base.y)**2
        ) < self.FIST_THRESHOLD
        
        pinky_folded = np.sqrt(
            (pinky_tip.x - pinky_base.x)**2 +
            (pinky_tip.y - pinky_base.y)**2
        ) < self.FIST_THRESHOLD
        
        return index_extended and middle_extended and ring_folded and pinky_folded
    
    def _is_thumb_up(self, landmarks):
        """Detecta polegar para cima usando ângulo"""
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        vec_tip = np.array([
            thumb_tip.x - thumb_mcp.x,
            thumb_tip.y - thumb_mcp.y
        ])
        
        vec_ip = np.array([
            thumb_ip.x - thumb_mcp.x,
            thumb_ip.y - thumb_mcp.y
        ])
        
        cross = vec_tip[0] * vec_ip[1] - vec_tip[1] * vec_ip[0]
        
        tips = [8, 12, 16, 20]
        bases = [5, 9, 13, 17]
        folded_count = 0
        for tip, base in zip(tips, bases):
            dist = np.sqrt(
                (landmarks[tip].x - landmarks[base].x)**2 +
                (landmarks[tip].y - landmarks[base].y)**2
            )
            if dist < self.FIST_THRESHOLD:
                folded_count += 1
        
        return cross < -self.THUMB_ANGLE_THRESHOLD and folded_count >= 3
    
    def _is_thumb_down(self, landmarks):
        """Detecta polegar para baixo usando ângulo"""
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        vec_tip = np.array([
            thumb_tip.x - thumb_mcp.x,
            thumb_tip.y - thumb_mcp.y
        ])
        
        vec_ip = np.array([
            thumb_ip.x - thumb_mcp.x,
            thumb_ip.y - thumb_mcp.y
        ])
        
        cross = vec_tip[0] * vec_ip[1] - vec_tip[1] * vec_ip[0]
        
        tips = [8, 12, 16, 20]
        bases = [5, 9, 13, 17]
        folded_count = 0
        for tip, base in zip(tips, bases):
            dist = np.sqrt(
                (landmarks[tip].x - landmarks[base].x)**2 +
                (landmarks[tip].y - landmarks[base].y)**2
            )
            if dist < self.FIST_THRESHOLD:
                folded_count += 1
        
        return cross > self.THUMB_ANGLE_THRESHOLD and folded_count >= 3
