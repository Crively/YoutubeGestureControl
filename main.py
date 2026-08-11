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
    
    if not cap.isOpened():
        print("❌ Erro: Webcam não encontrada!")
        print("Verifique se a câmera está conectada e disponível.")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cv2.namedWindow("YouTube Gesture Control", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("YouTube Gesture Control", 800, 600)
    
    print("=" * 50)
    print("🎬 YouTube Gesture Control iniciado!")
    print("=" * 50)
    print("Gestos disponíveis:")
    print("  ✊ Punho fechado  -> Play/Pausa")
    print("  🖐️ Mão aberta    -> Tela cheia")
    print("  👍 Polegar p/ cima -> Aumentar volume")
    print("  👎 Polegar p/ baixo -> Diminuir volume")
    print("  🤏 Pinça         -> Legendas")
    print("  ✌️ Paz (V)       -> Mutar/Desmutar")
    print(f"\n⏱️ Cooldown: {gesture_controller.cooldown_time} segundos entre comandos")
    print("\n⚠️  ATENÇÃO: Mantenha o navegador com YouTube em foco!")
    print("\nPressione 'q' para sair")
    print("=" * 50)

    frame_count = 0
    gesture_detected_count = 0
    command_executed_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Erro ao capturar frame da webcam")
                break
            frame = cv2.flip(frame, 1)
            frame = hand_tracker.find_hands(frame, draw=True
            landmarks = hand_tracker.get_landmarks()
            
            current_time = time.time()
            gesture_name = None
            
            if landmarks:
                gesture_name = gesture_detector.detect_gesture(landmarks)
                frame = gesture_detector.draw_landmarks(frame, landmarks, gesture_name)
                
                if gesture_name:
                    gesture_detected_count += 1
                    command = gesture_controller.process_gesture(gesture_name, current_time)
                    if command:
                        command_executed_count += 1
                        print(f"✅ [{command_executed_count}] Comando: {command} (gesto: {gesture_name})")
                        youtube_controller.execute_command(command)
            
            h, w, _ = frame.shape
            
            hand_status = "✅ Mão detectada" if landmarks else "❌ Mão não detectada"
            cv2.putText(frame, hand_status, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                       (0, 255, 0) if landmarks else (0, 0, 255), 2)
            
            if gesture_controller.is_ready(current_time):
                cv2.putText(frame, "✅ Pronto para comando", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                remaining = gesture_controller.get_cooldown_remaining(current_time)
                cv2.putText(frame, f"⏳ Cooldown: {remaining:.1f}s", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            if gesture_name:
                gesture_display = gesture_controller.get_gesture_name(gesture_name)
                cv2.putText(frame, f"Gesto: {gesture_display}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            frame_count += 1
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - current_time) if frame_count > 30 else 0
            
            cv2.putText(frame, "Pressione 'q' para sair", (w - 200, h - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            cv2.imshow("YouTube Gesture Control", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                gesture_controller.last_command_time = 0
                print("🔄 Cooldown resetado!")
                
    except KeyboardInterrupt:
        print("\n⚠️ Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\n" + "=" * 50)
        print("📊 Estatísticas finais:")
        print(f"   Gestos detectados: {gesture_detected_count}")
        print(f"   Comandos executados: {command_executed_count}")
        print("=" * 50)
        print("👋 Programa finalizado com sucesso!")

if __name__ == "__main__":
    main()
