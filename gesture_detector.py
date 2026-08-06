class GestureDetector:
    def __init__(self):
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20

        self.THUMB_CMC = 1
        self.INDEX_PIP = 6
        self.MIDDLE_PIP = 10
        self.RING_PIP = 14
        self.PINKY_PIP = 18

        self.WRIST = 0

    def detect_gesture(self, landmarks):
        """
        Detecta o gesto baseado nos landmarks da mão
        Retorna: string com o nome do gesto
        """
        if landmarks is None:
            return "NO_HAND"

        wrist = landmarks[self.WRIST]
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_cmc = landmarks[self.THUMB_CMC]
        index_tip = landmarks[self.INDEX_TIP]
        index_pip = landmarks[self.INDEX_PIP]
        middle_tip = landmarks[self.MIDDLE_TIP]
        middle_pip = landmarks[self.MIDDLE_PIP]
        ring_tip = landmarks[self.RING_TIP]
        ring_pip = landmarks[self.RING_PIP]
        pinky_tip = landmarks[self.PINKY_TIP]
        pinky_pip = landmarks[self.PINKY_PIP]

        fingers_up = []

        thumb_extended = abs(thumb_tip[0] - thumb_cmc[0]) > 0.05
        fingers_up.append(thumb_extended)

        fingers_up.append(index_tip[1] < index_pip[1])
        fingers_up.append(middle_tip[1] < middle_pip[1])
        fingers_up.append(ring_tip[1] < ring_pip[1])
        fingers_up.append(pinky_tip[1] < pinky_pip[1])

        count = sum(fingers_up)

        thumb_points_up = thumb_tip[1] < wrist[1] - 0.1
        thumb_points_down = thumb_tip[1] > wrist[1] + 0.1

        if count == 0:
            return "FIST"  # Punho fechado
        elif count == 2 and fingers_up[1] and fingers_up[2]:
            return "PEACE"  # Paz (V)
        elif count == 5:
            return "OPEN_HAND"  # Mão aberta
        elif count == 2 and fingers_up[0] and fingers_up[1]:
            return "PINCH"  # Pinça (polegar + indicador)
        elif count == 1 and fingers_up[0]:
            # Só o polegar levantado: decide a direção pela posição vertical real
            if thumb_points_up:
                return "THUMB_UP"  # Polegar para cima
            elif thumb_points_down:
                return "THUMB_DOWN"  # Polegar para baixo
            else:
                return "UNKNOWN_THUMB"
        else:
            return f"UNKNOWN_{count}"
