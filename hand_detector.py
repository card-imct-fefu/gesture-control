import copy
import itertools

import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self,
                 max_num_hands=1,
                 max_detection_confidence=0.7,
                 min_tracking_confidence=0.5):
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            static_image_mode=True,
            max_num_hands=max_num_hands,
            min_detection_confidence=max_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

    def find_marks(self, image, draw=False):
        def pre_process_landmark(landmark_list):
            temp_landmark_list = copy.deepcopy(landmark_list)

            # Convert to relative coordinates
            base_x, base_y = 0, 0
            for index, landmark_point in enumerate(temp_landmark_list):
                if index == 0:
                    base_x, base_y = landmark_point[0], landmark_point[1]

                temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
                temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

            # Convert to a one-dimensional list
            temp_landmark_list = list(
                itertools.chain.from_iterable(temp_landmark_list))

            # Normalization
            max_value = max(list(map(abs, temp_landmark_list)))

            def normalize_(n):
                return n / max_value

            temp_landmark_list = list(map(normalize_, temp_landmark_list))

            return temp_landmark_list

        imgRGB = cv2.cvtColor(image, cv2.cv2.COLOR_BGR2RGB)
        hands_processed = self.hands.process(imgRGB)
        marks = []

        if hands_processed.multi_hand_landmarks:
            for handLms in hands_processed.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    marks.append([cx, cy])
                if draw:
                    self.mpDraw.draw_landmarks(
                        image,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS)

            return pre_process_landmark(marks)
        return marks