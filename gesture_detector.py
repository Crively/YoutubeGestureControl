import cv2
import mediapipe as mp
import numpy as np
import math

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
        
       
        self.FIST_THRESHOLD = 0.15  
        self.THUMB_UP_ANGLE_THRESHOLD = 30  
        self.THUMB_DOWN_ANGLE_THRESHOLD = 150  
        self.PINCH_THRESHOLD = 0.05 

    def detect_gesture(self, landmarks):
        """
        Detecta o gesto baseado nos landmarks da mão
        Retorna: string com o nome do gesto ou None
        """
        if not landmarks:
            return None
            
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        wrist = landmarks[0]

        fingers_extended = self._count_fingers_extended(landmarks)

        if fingers_extended == 0:
            return "fist"
        
        if fingers_extended >= 4:
            return "open_hand"
   
        if fingers_extended == 1 and self._is_thumb_up(landmarks):
            return "thumbs_up"

        if fingers_extended == 1 and self._is_thumb_down(landmarks):
            return "thumbs_down"
        
        if self._is_pinch(landmarks):
            return "pinch"
        
        if self._is_v_gesture(landmarks):
            return "v"
        
        return None

    def _count_fingers_extended(self, landmarks):
        """
        Conta quantos dedos estão esticados (excluindo o polegar)
        """
        count = 0
        

        finger_tips = [8, 12, 16, 20] 
        finger_pips = [6, 10, 14, 18] 
        
        for tip, pip in zip(finger_tips, finger_pips):

            if landmarks[tip].y < landmarks[pip].y:
                count += 1
        
        return count

    def _is_thumb_up(self, landmarks):
        """
        Verifica se o polegar está apontando para cima
        """
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        wrist = landmarks[0]
        
        dx = thumb_tip.x - thumb_ip.x
        dy = thumb_tip.y - thumb_ip.y
        
        angle = math.degrees(math.atan2(dx, -dy))
        
        return abs(angle) < self.THUMB_UP_ANGLE_THRESHOLD

    def _is_thumb_down(self, landmarks):
        """
        Verifica se o polegar está apontando para baixo
        """
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        wrist = landmarks[0]
        
        dx = thumb_tip.x - thumb_ip.x
        dy = thumb_tip.y - thumb_ip.y
        
        angle = math.degrees(math.atan2(dx, -dy))
        
        return abs(angle) > self.THUMB_DOWN_ANGLE_THRESHOLD

    def _is_pinch(self, landmarks):
        """
        Verifica se o gesto é de pinça (polegar e indicador se tocando)
        """
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = math.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        
        return distance < self.PINCH_THRESHOLD

    def _is_v_gesture(self, landmarks):
        """
        Verifica se o gesto é o V da paz (indicador e médio esticados)
        """
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        index_extended = index_tip.y < index_pip.y
        
        middle_extended = middle_tip.y < middle_pip.y
        
        ring_folded = ring_tip.y > landmarks[14].y
        pinky_folded = pinky_tip.y > landmarks[18].y
        
        return index_extended and middle_extended and ring_folded and pinky_folded

    def draw_landmarks(self, frame, landmarks, gesture_name):
        """
        Desenha os landmarks e o nome do gesto na tela
        """
        self.mp_drawing.draw_landmarks(
            frame, 
            landmarks, 
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )
    
        if gesture_name:
            h, w, _ = frame.shape
            cv2.putText(frame, f"Gesto: {gesture_name}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
