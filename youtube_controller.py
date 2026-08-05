import pyautogui
import time

class YouTubeController:
    def __init__(self, debug=True):
        self.debug = debug
        pyautogui.FAILSAFE = True  # Para emergências (mova o mouse para o canto)
        
    def play_pause(self):
        """Alterna entre play e pause (tecla K)"""
        if self.debug: print("▶️ Play/Pause")
        pyautogui.press('k')
        # Alternativa: pyautogui.press('space')
        
    def forward(self, seconds=5):
        """Avança 5 segundos (tecla L)"""
        if self.debug: print(f"⏩ Avançar {seconds}s")
        pyautogui.press('l')
        
    def rewind(self, seconds=5):
        """Volta 5 segundos (tecla J)"""
        if self.debug: print(f"⏪ Voltar {seconds}s")
        pyautogui.press('j')
        
    def volume_up(self, steps=5):
        """Aumenta volume (seta para cima)"""
        if self.debug: print("🔊 Aumentar Volume")
        for _ in range(steps):
            pyautogui.press('up')
            time.sleep(0.05)
        
    def volume_down(self, steps=5):
        """Diminui volume (seta para baixo)"""
        if self.debug: print("🔉 Diminuir Volume")
        for _ in range(steps):
            pyautogui.press('down')
            time.sleep(0.05)
        
    def fullscreen(self):
        """Alterna tela cheia (tecla F)"""
        if self.debug: print("⛶ Tela Cheia")
        pyautogui.press('f')
        
    def toggle_captions(self):
        """Alterna legendas (tecla C)"""
        if self.debug: print("📝 Legendas")
        pyautogui.press('c')
        
    def mute(self):
        """Muta/desmuta (tecla M)"""
        if self.debug: print("🔇 Mutar")
        pyautogui.press('m')