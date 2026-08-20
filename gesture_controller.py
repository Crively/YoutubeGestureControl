import time
from youtube_controller import YouTubeController

class GestureController:
    def __init__(self):
        self.youtube = YouTubeController()
        self.last_command_time = 0
        self.cooldown = 2.0  
        self.last_gesture = None
        self.ready = True
        
        self.gesture_map = {
            "fist": self.youtube.toggle_play_pause,
            "open_hand": self.youtube.toggle_fullscreen,
            "thumb_up": self.youtube.volume_up,
            "thumb_down": self.youtube.volume_down,
            "pinch": self.youtube.toggle_captions,
            "peace": self.youtube.toggle_mute
        }
        
        self.continuous_gestures = ["thumb_up", "thumb_down"]
        
    def map_gesture(self, gesture):
        """Mapeia um gesto para uma ação, respeitando o cooldown"""
        if gesture == "none" or gesture not in self.gesture_map:
            return
            
        current_time = time.time()
        time_since_last = current_time - self.last_command_time
        
        if gesture in self.continuous_gestures:
            self._execute_gesture(gesture)
            return
            
        if time_since_last >= self.cooldown:
            self._execute_gesture(gesture)
            self.last_command_time = current_time
            self.ready = False
            self._schedule_ready()
        else:
            self.ready = False
            print(f"⏳ Cooldown ativo. Aguarde {self.cooldown - time_since_last:.1f}s")
    
    def _execute_gesture(self, gesture):
        """Executa a ação do gesto"""
        if gesture in self.gesture_map:
            action = self.gesture_map[gesture]
            action()
            self.last_gesture = gesture
            print(f"✅ Gesto executado: {gesture}")
    
    def _schedule_ready(self):
        """Agenda o estado ready para depois do cooldown"""
        import threading
        def set_ready():
            time.sleep(self.cooldown)
            self.ready = True
        
        threading.Thread(target=set_ready, daemon=True).start()
    
    def is_ready(self):
        """Verifica se o sistema está pronto para novo comando"""
        return self.ready
    
    def get_cooldown_remaining(self):
        """Retorna o tempo restante do cooldown"""
        if self.ready:
            return 0
        elapsed = time.time() - self.last_command_time
        return max(0, self.cooldown - elapsed)
