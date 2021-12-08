import numpy as np
import tensorflow as tf


class HandSignClassifier(object):
    def __init__(
            self,
            model_path='model/hand_sign_classifier.tflite',
            num_threads=1,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def get_index(self, landmark_list):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index

    def get_label(self, landmark_list):
        labels = ['open', 'close', 'finger', 'okay']
        index = self.get_index(landmark_list)
        return labels[index]
