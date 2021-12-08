import cv2

from fps_counter import FpsCounter
from hand_detector import HandDetector
from model.hand_sign_classifier import HandSignClassifier

hand_detector = HandDetector(max_num_hands=1)
hand_sign_classifier = HandSignClassifier()

fps_counter = FpsCounter()

cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0

while True:
    if cv2.waitKey(10) == 27:
        break
    success, img = cap.read()
    img = cv2.flip(img, 1)

    marks = hand_detector.find_marks(img, True)
    if marks:
        cv2.waitKey(10)

        hand_sign = hand_sign_classifier.get_label(marks)
        fps = fps_counter.get()

        cv2.putText(img,
                    f"{fps} FPS, {hand_sign}",
                    (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

cv2.destroyAllWindows()
