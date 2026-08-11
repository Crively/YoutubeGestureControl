import cv2
import mediapipe as mp
import numpy as np
import math

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
      
        self.FIST_THRESHOLD = 0.15 
        self.THUMB_UP_ANGLE_THRESHOLD = 45 
        self.THUMB_DOWN_ANGLE_THRESHOLD = 135  
        self.PINCH_THRESHOLD = 0.12 

    def detect_gesture(self, landmarks):
        """
        Detecta o gesto baseado nos landmarks da mão
        Retorna: string com o nome do gesto ou None
        """
        if not landmarks:
            return None
            
        if self._is_pinch(landmarks):
            return "pinch"
        
        if self._is_v_gesture(landmarks):
            return "v"
        
        if self._is_thumb_up(landmarks):
            return "thumbs_up"
        if self._is_thumb_down(landmarks):
            return "thumbs_down"
        
        fingers_extended = self._count_fingers_extended(landmarks)
        
        if fingers_extended == 0:
            return "fist"
        
        if fingers_extended >= 4:
            return "open_hand"
        
        return None

    def _count_fingers_extended(self, landmarks):
        """
        Conta quantos dedos estão esticados (AGORA incluindo o polegar)
        """
        count = 0
        
        if landmarks[4].x > landmarks[3].x: 
            count += 1
        
        finger_tips = [8, 12, 16, 20] 
        finger_pips = [6, 10, 14, 18] 
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                count += 1
        
        return count

    def _is_thumb_up(self, landmarks):
        """
        Verifica se o polegar está apontando para cima
        CORREÇÃO: Usa ângulo mais robusto
        """
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        
        dx = thumb_tip.x - thumb_ip.x
        dy = thumb_tip.y - thumb_ip.y
        
        angle = math.degrees(math.atan2(dx, -dy))
        
        is_up = abs(angle) < self.THUMB_UP_ANGLE_THRESHOLD
        
        thumb_extended = self._is_thumb_extended(landmarks)
        
        return is_up and thumb_extended

    def _is_thumb_down(self, landmarks):
        """
        Verifica se o polegar está apontando para baixo
        """
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        
        dx = thumb_tip.x - thumb_ip.x
        dy = thumb_tip.y - thumb_ip.y
        
        angle = math.degrees(math.atan2(dx, -dy))
        
        is_down = abs(angle) > self.THUMB_DOWN_ANGLE_THRESHOLD
        
        thumb_extended = self._is_thumb_extended(landmarks)
        
        return is_down and thumb_extended

    def _is_thumb_extended(self, landmarks):
        """
        Verifica se o polegar está esticado (separado da mão)
        """
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2] 
        
        distance = math.sqrt(
            (thumb_tip.x - thumb_mcp.x)**2 + 
            (thumb_tip.y - thumb_mcp.y)**2
        )
        return distance > 0.08  

    def _is_pinch(self, landmarks):
        """
        Verifica se o gesto é de pinça (polegar e indicador se tocando)
        CORREÇÃO: Threshold ajustado e verificação adicional
        """
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = math.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        
        if distance < self.PINCH_THRESHOLD:

            middle_tip = landmarks[12]
            middle_pip = landmarks[10]
            ring_tip = landmarks[16]
            ring_pip = landmarks[14]
            pinky_tip = landmarks[20]
            pinky_pip = landmarks[18]
            
            middle_extended = middle_tip.y < middle_pip.y
            ring_extended = ring_tip.y < ring_pip.y
            pinky_extended = pinky_tip.y < pinky_pip.y
            

            if not (middle_extended or ring_extended or pinky_extended):
                return True
        
        return False

    def _is_v_gesture(self, landmarks):
        """
        Verifica se o gesto é o V da paz (indicador e médio esticados)
        """
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]


        index_extended = index_tip.y < index_pip.y
        middle_extended = middle_tip.y < middle_pip.y
        
        ring_folded = ring_tip.y > ring_pip.y
        pinky_folded = pinky_tip.y > pinky_pip.y
        
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_folded = thumb_tip.y > thumb_ip.y  # Simplificado
        
        return index_extended and middle_extended and ring_folded and pinky_folded

    def draw_landmarks(self, frame, landmarks, gesture_name):
        """
        Desenha os landmarks e o nome do gesto na tela
        """
        if landmarks:
          
            landmark_list = mp.solutions.framework_public.pb2.NormalizedLandmarkList()
            for lm in landmarks:
                landmark = landmark_list.landmark.add()
                landmark.x = lm.x
                landmark.y = lm.y
                landmark.z = lm.z if hasattr(lm, 'z') else 0
            
            self.mp_drawing.draw_landmarks(
                frame, 
                landmark_list, 
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        if gesture_name:
            h, w, _ = frame.shape
            
            overlay = frame.copy()
            cv2.rectangle(overlay, (5, 5), (350, 60), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
            
            cv2.putText(frame, f"Gesto: {gesture_name.upper()}", (10, 45), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
