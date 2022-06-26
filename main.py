import cv2
import mediapipe as mp
import vgamepad as vg

from config import Config
from fps_counter import FpsCounter
from hand_detector import HandDetector
from model.hand_sign_classifier import HandSignClassifier


def crop_image(image, k):
    x, y, _ = image.shape
    offset_x, offset_y = int(x * k), int(y * k)
    return image[offset_y:y - offset_y, offset_x:x - offset_x]


gamepad = vg.VX360Gamepad()
config = Config("./config.json")

window_name = "main"
view_window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

cap = cv2.VideoCapture(config.get_video_capture_id())
cap.set(cv2.CAP_PROP_FPS, config.get_max_fps())

fps_counter = FpsCounter()

hand_sign_classifier = HandSignClassifier()
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

with mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():

        if cv2.waitKey(10) == 27:
            break
        success, img = cap.read()
        img = crop_image(img, config.get_crop_value())
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
                    f"{fps:03d} FPS, {hand_sign}",
                    (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        gamepad.update()
        cv2.imshow(window_name, img)

cv2.destroyAllWindows()
