"""
FeersumNLU Image Regressor: Base class.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.image_encoder_base import ImageEncoderBase


class ImageRegressorBase(ABC):
    """
    FeersumNLU Image Regressor: Base class.
    """

    def __init__(self, vision_model: Optional[ImageEncoderBase] = None) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.

        self._vision_model = vision_model
        # REMEMBER to add new attributes to __getstate__ and __setstate__ !!!

    def __getstate__(self):
        state = {
            'uuid': self.uuid,

        }
        # Don't save the vision model with the regressor. It is way too big!
        return state

    def __setstate__(self, state):
        """_vision_model not pickled with the object!"""
        self.uuid = state['uuid']

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
                     training_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
                     testing_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of samples with values (image, float). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of samples with values (image, float) to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        pass

    @abstractmethod
    def train(self,
              training_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
              testing_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
              num_epochs: int) -> bool:
        """
        Reset and train the regressor with image-value pairs

        :param training_list: List of samples with values (image, float). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of samples with values (image, float) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        pass

    @abstractmethod
    def estimate(self, input_image: str) -> float:
        """ Run the regression model.

        :param input_image: The input image to the estimator model. Image formatted as utf8 encoded base64 string.
        :return: The model estimate.
        """
        pass
