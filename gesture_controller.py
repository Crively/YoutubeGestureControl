import time

class GestureController:
    def __init__(self, youtube_controller, cooldown_time=1.5):
        self.youtube = youtube_controller
        self.cooldown_time = cooldown_time
        self.last_command_time = 0
        self.last_gesture = None
        
    def process_gesture(self, gesture, landmarks=None, prev_landmarks=None):
        """
        Processa o gesto e executa o comando correspondente com cooldown
        """
        current_time = time.time()
        
        # Verifica cooldown
        if current_time - self.last_command_time < self.cooldown_time:
            return
        
        # Mapeamento gesto -> comando
        gesture_map = {
            "FIST": self.youtube.play_pause,
            "SWIPE_RIGHT": self.youtube.forward,
            "SWIPE_LEFT": self.youtube.rewind,
            "THUMB_UP": self.youtube.volume_up,
            "THUMB_DOWN": self.youtube.volume_down,
            "OPEN_HAND": self.youtube.fullscreen,
            "PINCH": self.youtube.toggle_captions,
            "PEACE": self.youtube.mute,
        }
        
        # Verifica swipe (movimento) separadamente
        if gesture not in ["SWIPE_RIGHT", "SWIPE_LEFT"] and landmarks and prev_landmarks:
            swipe = self.detect_swipe(landmarks, prev_landmarks)
            if swipe:
                gesture = swipe
        
        # Executa o comando se o gesto for válido
        if gesture in gesture_map:
            gesture_map[gesture]()
            self.last_command_time = current_time
            self.last_gesture = gesture
            
    def detect_swipe(self, landmarks, prev_landmarks, threshold=0.08):
        """Detecta swipe baseado no movimento do centro da mão"""
        if landmarks is None or prev_landmarks is None:
            return None
            
        current_x = landmarks[0][0]
        prev_x = prev_landmarks[0][0]
        
        if current_x - prev_x > threshold:
            return "SWIPE_RIGHT"
        elif prev_x - current_x > threshold:
            return "SWIPE_LEFT"
        return None