import pyautogui
import time

class YouTubeController:
    def __init__(self, debug=True):
        self.debug = debug
        pyautogui.FAILSAFE = True
        self.key_delay = 0.1

    def execute_command(self, command):
        """Executa um comando por nome"""
        commands = {
            "play_pause": self.play_pause,
            "fullscreen": self.fullscreen,
            "volume_up": self.volume_up,
            "volume_down": self.volume_down,
            "toggle_captions": self.toggle_captions,
            "mute": self.mute
        }
        
        if command in commands:
            commands[command]()
            return True
        return False
        
    def play_pause(self):
        """Alterna entre play e pause (tecla K)"""
        if self.debug: print("▶️ Play/Pause")
        pyautogui.press('k')
        time.sleep(self.key_delay)
        
    def forward(self, seconds=5):
        """Avança 5 segundos (tecla L)"""
        if self.debug: print(f"⏩ Avançar {seconds}s")
        pyautogui.press('l')
        time.sleep(self.key_delay)
        
    def rewind(self, seconds=5):
        """Volta 5 segundos (tecla J)"""
        if self.debug: print(f"⏪ Voltar {seconds}s")
        pyautogui.press('j')
        time.sleep(self.key_delay)
        
    def volume_up(self, steps=1): 
        """Aumenta volume (seta para cima)"""
        if self.debug: print("🔊 Aumentar Volume")
        pyautogui.press('up')
        time.sleep(self.key_delay)
        
    def volume_down(self, steps=1): 
        """Diminui volume (seta para baixo)"""
        if self.debug: print("🔉 Diminuir Volume")
        pyautogui.press('down')
        time.sleep(self.key_delay)
        
    def fullscreen(self):
        """Alterna tela cheia (tecla F)"""
        if self.debug: print("⛶ Tela Cheia")
        pyautogui.press('f')
        time.sleep(self.key_delay)
        
    def toggle_captions(self):
        """Alterna legendas (tecla C)"""
        if self.debug: print("📝 Legendas")
        pyautogui.press('c')
        time.sleep(self.key_delay)
        
    def mute(self):
        """Muta/desmuta (tecla M)"""
        if self.debug: print("🔇 Mutar")
        pyautogui.press('m')
        time.sleep(self.key_delay)
