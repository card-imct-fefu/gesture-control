import cv2
import vgamepad as vg

from fps_counter import FpsCounter
from hand_detector import HandDetector
from model.hand_sign_classifier import HandSignClassifier
from config import Config

gamepad = vg.VX360Gamepad()
cap = cv2.VideoCapture(0)

hand_detector = HandDetector(max_num_hands=1)
hand_sign_classifier = HandSignClassifier()
fps_counter = FpsCounter()
config = Config("./config.json")


while True:
    if cv2.waitKey(10) == 27:
        break
    success, img = cap.read()
    img = cv2.flip(img, 1)

    marks = hand_detector.find_marks(img, True)
    hand_sign = None
    gamepad.reset()

    if marks:
        cv2.waitKey(50)

        hand_sign = hand_sign_classifier.get_label(marks)
        button = config.get_button(hand_sign)

        if button:
            gamepad.press_button(button=button)

    fps = fps_counter.get()

    cv2.putText(img,
                f"{fps} FPS, {hand_sign}",
                (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    gamepad.update()
    cv2.imshow("Image", img)

cv2.destroyAllWindows()
