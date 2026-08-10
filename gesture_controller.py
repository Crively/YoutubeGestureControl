class GestureController:
    def __init__(self):
        self.gesture_map = {
            "fist": "play_pause",
            "open_hand": "fullscreen",
            "thumbs_up": "volume_up",
            "thumbs_down": "volume_down",
            "pinch": "toggle_captions",
            "v": "mute"
        }
        
        self.cooldown_time = 3.0  
        self.last_command_time = 0
        self.last_gesture = None

    def process_gesture(self, gesture_name, current_time):
        """
        Processa o gesto detectado e retorna o comando correspondente
        """
        if not gesture_name:
            return None

        if current_time - self.last_command_time < self.cooldown_time:
            return None
        
        if gesture_name in self.gesture_map:
            
            if gesture_name != self.last_gesture:
                self.last_gesture = gesture_name
                self.last_command_time = current_time
                return self.gesture_map[gesture_name]
        
        return None

    def get_gesture_name(self, gesture_key):
        """
        Retorna o nome legível do gesto
        """
        gesture_names = {
            "fist": "✊ Punho fechado",
            "open_hand": "🖐️ Mão aberta",
            "thumbs_up": "👍 Polegar para cima",
            "thumbs_down": "👎 Polegar para baixo",
            "pinch": "🤏 Pinça",
            "v": "✌️ Paz (V)"
        }
        return gesture_names.get(gesture_key, gesture_key)
