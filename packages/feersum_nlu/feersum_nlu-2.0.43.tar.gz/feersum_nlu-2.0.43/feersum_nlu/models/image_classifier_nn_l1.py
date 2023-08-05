"""
FeersumNLU Classifier: Nearest Neighbour search with L1 distance; Uses Feersum vision_model.
"""

import logging

from typing import Tuple, List, Set, NamedTuple, Union, Optional  # noqa # pylint: disable=unused-import

from feersum_nlu.models.image_encoder_base import ImageEncoderBase
from feersum_nlu.models import image_classifier_base

import numpy as np
import math

# === The sample type. sent_vec and lang_code are filled in during training!
# Python 3.5
_SampleT = NamedTuple('_SampleT',
                      [('image', str),
                       ('image_vect', np.array),
                       ('label', str)])


# Python 3.6
# class _SampleT(NamedTuple):
#     image: str
#     image_vect: np.array
#     label: str
# ===


class ImageClassifierNearestNeighbourL1(image_classifier_base.ImageClassifierBase):
    """
    FeersumNLU Classifier: Nearest Neighbour search with L1 distance.
    """

    def __init__(self, vision_model: Optional[ImageEncoderBase]) -> None:
        super().__init__(vision_model=vision_model)

        self._next_label_idx = 0

        self._samples = []  # type: List[_SampleT]

    def __getstate__(self):
        """Do not pickle the _vision_model with this object!"""
        # ToDo: call base class' __getstate__
        state = self.__dict__.copy()  # ToDo: how much time is wasted in copying the vision model!?
        del state['_vision_model']
        return state

    def __setstate__(self, state):
        """_language_model_dict not pickled with the object!"""
        # ToDo: call base class' __setstate__
        self.__dict__.update(state)
        self._vision_model = None

    def train_online(self,
                     training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                     testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        # ToDo: Batch the training samples and submit batches to the sentence encoder to improve performance!

        if self._vision_model is None:
            logging.error("image_classifier_nn_l1.train_online - _vision_model is None!")
            return False

        # Train the model - Calculate the FAQ question vectors just once here.
        for training_sample in training_list:
            image = training_sample[0]
            label = training_sample[1]

            # The model is trained by updating _samples list. The list is the model!
            self._samples.append(_SampleT(image,
                                          self._vision_model.calc_image_vector(image),
                                          label))

            # === Update the _labels set and the _label_to_idx mapping ===
            self._labels.add(label)
            if self._label_to_idx.get(label) is None:
                self._label_to_idx[label] = self._next_label_idx
                self._next_label_idx += 1

        return True

    def train(self,
              training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              num_epochs: int = 1) -> bool:
        """
        Reset and train the classifier with image-label pairs

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._label_to_idx.clear()
        self._next_label_idx = 0
        self._labels.clear()

        self._samples.clear()

        return self.train_online(training_list, testing_list, True)

    def classify(self, input_image: str,
                 weak_match_threshold: float,
                 top_n: int) -> List[Tuple[str, float]]:
        """ Find the n best matches to the input image.

        :param input_image: The image to look for in the samples set. Image formatted as utf8 encoded base64 string.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)].
        """
        if self._vision_model is None:
            logging.error("image_classifier_nn_l1.classify - vision model not found.")
            return []

        input_vect = self._vision_model.calc_image_vector(input_image)

        # 1) Calc softmax scores over ALL training samples.
        # ToDo: Consider using hierarchical or fast_approx softmax if large model performance becomes a problem.
        softmax_temp = (1.0 / 250.0) * self._vision_model.get_vect_dim()  # ToDo: Set this as a model hyper param.
        scored_samples = []  # type: List[Tuple[str, float]]
        best_match_probs = []  # type: List[Tuple[str, float]]

        # ToDo: Use more efficient KNN search data structure if many questions used in model!
        #   OR: Use locality sensitive hashing instead!!
        for sample in self._samples:
            dist = ImageEncoderBase.calc_l1_dist(input_vect, sample.image_vect)

            score = math.exp(-1.0 * dist / softmax_temp)
            scored_samples.append((sample.label, score))

        num_scored_samples = len(scored_samples)

        if num_scored_samples > 0:
            # 2) Find best matching scored labels.
            scored_samples.sort(key=lambda scored_sample: scored_sample[1], reverse=True)
            best_match_label_set = set()  # type: Set[str]
            best_match_scores = []  # type: List[Tuple[str, float]]

            i = 0
            while i < num_scored_samples:
                label, score = scored_samples[i]

                if label not in best_match_label_set:
                    best_match_label_set.add(label)
                    best_match_scores.append((label, score))

                i += 1

            softmax_sum = 0.0

            for label, score in best_match_scores:
                softmax_sum += score

            # Note on softmax_temp:
            #  If softmax_sum is zero then none of the training samples were close enough to the input image to
            #  have score = math.exp(-1.0 * dist / softmax_temp) > 0.
            #  The problem could also be alleviated by increasing softmax_temp.

            if softmax_sum > 0.0:
                # 3) Calc probabilities and use weak_match_threshold as a probability threshold.
                for label, score in best_match_scores:
                    probability = score / softmax_sum

                    if probability > (1.0 - weak_match_threshold):
                        best_match_probs.append((label, probability))

                        if len(best_match_probs) >= top_n:
                            break  # from for-loop.

        return best_match_probs
