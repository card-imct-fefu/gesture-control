import cv2
import mediapipe as mp
import vgamepad as vg

from config import Config
from fps_counter import FpsCounter
from hand_detector import HandDetector
from model.hand_sign_classifier import HandSignClassifier

gamepad = vg.VX360Gamepad()

window_name = "main"
view_window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 30)

hand_sign_classifier = HandSignClassifier()
fps_counter = FpsCounter()
config = Config("./config.json")

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

with mpHands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():

        if cv2.waitKey(10) == 27:
            break
        success, img = cap.read()
        img = cv2.flip(img, 1)

        marks = HandDetector.find_marks(hands, img, True)
        hand_sign = None
        gamepad.reset()

        if marks:
            hand_sign = hand_sign_classifier.get_label(marks)
            button = config.get_button(hand_sign)

            if button:
                gamepad.press_button(button=button)

        fps = fps_counter.get()

        cv2.putText(img,
                    f"{fps} FPS, {hand_sign}",
                    (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        gamepad.update()
        cv2.imshow(window_name, img)

cv2.destroyAllWindows()
