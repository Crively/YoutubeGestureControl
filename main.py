import cv2
import time
import sys
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from gesture_controller import GestureController

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Erro: Não foi possível acessar a webcam!")
        print("Verifique se a câmera está conectada e disponível.")
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    hand_tracker = HandTracker()
    gesture_detector = GestureDetector()
    gesture_controller = GestureController()
    
    print("🎬 YouTube Gesture Control iniciado!")
    print("📌 Gestos disponíveis:")
    print("  ✊ Punho fechado -> Play/Pausa")
    print("  🖐️ Mão aberta -> Tela cheia")
    print("  👍 Polegar cima -> Aumentar volume")
    print("  👎 Polegar baixo -> Diminuir volume")
    print("  🤏 Pinça -> Legendas")
    print("  ✌️ Paz (V) -> Mutar")
    print("\nPressione 'q' para sair.")
    print("-" * 50)
    
    prev_gesture = "none"
    stable_gesture = "none"
    stability_counter = 0
    STABILITY_THRESHOLD = 3 
    
    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Falha ao capturar frame. Tentando reconectar...")
            time.sleep(1)
            continue
        
        frame = cv2.flip(frame, 1)
        
        frame, landmarks = hand_tracker.find_hands(frame)
        
        gesture = "none"
        if landmarks is not None:
            gesture = gesture_detector.detect_gesture(landmarks)
        
        if gesture == prev_gesture:
            stability_counter += 1
        else:
            stability_counter = 0
            prev_gesture = gesture
        
        if stability_counter >= STABILITY_THRESHOLD:
            if gesture != stable_gesture:
                stable_gesture = gesture
                if gesture != "none":
                    gesture_controller.map_gesture(gesture)
        
        status_text = "🟢 Pronto" if gesture_controller.is_ready() else "⏳ Aguarde"
        cooldown = gesture_controller.get_cooldown_remaining()
        
        cv2.putText(frame, f"Gesto: {gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Status: {status_text}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        if cooldown > 0:
            cv2.putText(frame, f"Cooldown: {cooldown:.1f}s", (10, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("YouTube Gesture Control", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Programa finalizado.")

if __name__ == "__main__":
    main()
