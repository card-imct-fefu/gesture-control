import cv2
import time

from hand_detector import HandDetector

hand_detector = HandDetector(max_num_hands=2)

cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0

while True:
    if cv2.waitKey(10) == 27:
        break
    success, img = cap.read()
    img = cv2.flip(img, 1)

    marks = hand_detector.find_marks(img, True)
    print(marks)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

cv2.destroyAllWindows()

