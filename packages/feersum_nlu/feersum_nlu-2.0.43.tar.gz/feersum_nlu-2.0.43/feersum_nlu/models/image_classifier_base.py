"""
FeersumNLU Image Classifier: Base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional, Set, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.image_encoder_base import ImageEncoderBase


class ImageClassifierBase(ABC):
    """
    FeersumNLU Image Classifier: Base class.
    """

    def __init__(self, vision_model: Optional[ImageEncoderBase] = None) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        self._labels = set()  # type: Set[str]
        # Label to idx mapping. Maintain during training.
        self._label_to_idx = {}  # type: Dict[str, int]

        self._vision_model = vision_model
        # REMEMBER to add new attributes to __getstate__ and __setstate__ !!!

    def __getstate__(self):
        state = {
            'uuid': self.uuid,
            '_labels': self._labels,
            '_label_to_idx': self._label_to_idx
        }
        # Don't save the vision model with the classifier. It is way too big!
        return state

    def __setstate__(self, state):
        """_vision_model not pickled with the object!"""
        self.uuid = state['uuid']
        self._labels = state['_labels']
        self._label_to_idx = state['_label_to_idx']
        self._vision_model = None

    def get_vision_model(self) -> Optional[ImageEncoderBase]:
        """ Return a reference to the vision model. """
        return self._vision_model

    def set_vision_model(self, vision_model: ImageEncoderBase) -> None:
        """Set or update the vision model. An update is required after unpickling!
        See refresh_model_vectors to also update the model's vectors if a new vision model was supplied."""
        self._vision_model = vision_model

    @abstractmethod
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
        pass

    @abstractmethod
    def train(self,
              training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              num_epochs: int) -> bool:
        """
        Reset and train the classifier with image-label pairs

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        pass

    def get_labels(self) -> List[str]:
        """
        Get the list of labels currently present in the model.

        :return: The list of labels currently present in the model.
        """
        return list(self._labels)

    def get_label_idx(self, label: str) -> Optional[int]:
        return self._label_to_idx.get(label)

    @abstractmethod
    def classify(self, input_image: str,
                 weak_match_threshold: float,
                 top_n: int) -> List[Tuple[str, float]]:
        """ Find the top_n class prediction.

        :param input_image: The image to classify. Image formatted as utf8 encoded base64 string.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)].
        """
        pass
