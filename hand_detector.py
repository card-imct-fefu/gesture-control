import mediapipe as mp
import cv2


class HandDetector:

    def __init__(self, max_num_hands=1,
                 max_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=max_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

    def find_marks(self, image, draw=False):
        imgRGB = cv2.cvtColor(image, cv2.cv2.COLOR_YCrCb2BGR)
        hands_processed = self.hands.process(imgRGB)
        marks = []

        if hands_processed.multi_hand_landmarks:
            for handLms in hands_processed.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    marks.append({'id': id, 'x': cx, 'y': cy})
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, handLms, self.mpHands.HAND_CONNECTIONS)
        return marks
