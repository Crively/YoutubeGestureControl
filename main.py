import cv2
import numpy as np
import time 
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from gesture_controller import GestureController
from youtube_controller import YouTubeController


def main():
    hand_tracker = HandTracker()
    gesture_detector = GestureDetector()
    youtube_controller = YouTubeController()
    gesture_controller = GestureController(youtube_controller, cooldown_time=1.5)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    prev_landmarks = None

    print("🎬 YouTube Gesture Control Iniciado!")
    print("Pressione 'q' para sair")
    print("📋 Gestos disponíveis:")
    print("  ✊ Punho = Play/Pause")
    print("  👉 Deslizar direita = Avançar 5s")
    print("  👈 Deslizar esquerda = Voltar 5s")
    print("  👍 Polegar cima = Aumentar volume")
    print("  👎 Polegar baixo = Diminuir volume")
    print("  🖐️ Mão aberta = Tela Cheia")
    print("  🤏 Pinça = Legendas")
    print("  ✌️ Paz (V) = Mutar")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        frame = hand_tracker.find_hands(frame, draw=True)
        landmarks = hand_tracker.get_landmarks()

        if landmarks:
            gesture = gesture_detector.detect_gesture(landmarks)

            cv2.putText(frame, f"Gesto: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            gesture_controller.process_gesture(gesture, landmarks, prev_landmarks)
            
            prev_landmarks = landmarks
        else:
            prev_landmarks = None
            cv2.putText(frame, "Nenhuma mao detectada", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        current_time = time.time()
        cooldown_remaining = max(0, 1.5 - (current_time - gesture_controller.last_command_time))
        if cooldown_remaining > 0:
            cv2.putText(frame, f"Cooldown: {cooldown_remaining:.1f}s", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow("YouTube Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Programa finalizado!")


if __name__ == "__main__":
    main()
