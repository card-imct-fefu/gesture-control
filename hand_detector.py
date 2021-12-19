import copy
import itertools

import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDrawingStyles = mp.solutions.drawing_styles


class HandDetector:

    @staticmethod
    def find_marks(hands, image, draw=False):
        def pre_process_landmark(landmark_list):
            temp_landmark_list = copy.deepcopy(landmark_list)

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

        img_rgb = cv2.cvtColor(image, cv2.cv2.COLOR_BGR2RGB)
        hands_processed = hands.process(img_rgb)
        marks = []

        if hands_processed.multi_hand_landmarks:
            for handLms in hands_processed.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    marks.append([cx, cy])
                if draw:
                    mpDraw.draw_landmarks(
                        image,
                        handLms,
                        mpHands.HAND_CONNECTIONS,
                        mpDrawingStyles.get_default_hand_landmarks_style(),
                        mpDrawingStyles.get_default_hand_connections_style())

            return pre_process_landmark(marks)
        return marks
