import cv2
import time
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from gesture_controller import GestureController
from youtube_controller import YouTubeController

def main():
    hand_tracker = HandTracker()
    gesture_detector = GestureDetector()
    gesture_controller = GestureController()
    youtube_controller = YouTubeController()
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("🎬 YouTube Gesture Control iniciado!")
    print("Gestos disponíveis:")
    print("  ✊ Punho fechado -> Play/Pausa")
    print("  🖐️ Mão aberta -> Tela cheia")
    print("  👍 Polegar para cima -> Aumentar volume")
    print("  👎 Polegar para baixo -> Diminuir volume")
    print("  🤏 Pinça -> Legendas")
    print("  ✌️ Paz (V) -> Mutar/Desmutar")
    print(f"\n⏱️ Cooldown: {gesture_controller.cooldown_time} segundos entre comandos")
    print("\nPressione 'q' para sair")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            landmarks = hand_tracker.detect_hand(rgb_frame)
            
            current_time = time.time()
            gesture_name = None
            
            if landmarks:
                gesture_name = gesture_detector.detect_gesture(landmarks)
                
                frame = gesture_detector.draw_landmarks(frame, landmarks, gesture_name)
                
                if gesture_name:
                    command = gesture_controller.process_gesture(gesture_name, current_time)
                    if command:
                        print(f"✅ Comando executado: {command} (gesto: {gesture_name})")
                        youtube_controller.execute_command(command)
            
            h, w, _ = frame.shape
            
            time_since_last = current_time - gesture_controller.last_command_time
            if time_since_last < gesture_controller.cooldown_time:
                remaining = gesture_controller.cooldown_time - time_since_last
                cooldown_text = f"⏳ Cooldown: {remaining:.1f}s"
                cv2.putText(frame, cooldown_text, (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "✅ Pronto para comando", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if gesture_name:
                gesture_display = gesture_controller.get_gesture_name(gesture_name)
                cv2.putText(frame, f"Gesto atual: {gesture_display}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            status_text = "Gestos ativos" if landmarks else "Mão não detectada"
            cv2.putText(frame, status_text, (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow("YouTube Gesture Control", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Programa finalizado")

if __name__ == "__main__":
    main()
