"""
FeersumNLU Text Classifier: Base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional, Set, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.sentence_encoder_base import SentenceEncoderBase


class TextClassifierBase(ABC):
    """
    FeersumNLU Classifier: Base class.
    """

    def __init__(self, language_model_dict: Optional[Dict[str, SentenceEncoderBase]] = None) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        self._labels = set()  # type: Set[str]
        # Label to idx mapping. Maintain during training.
        self._label_to_idx = {}  # type: Dict[str, int]

        self._language_model_dict = language_model_dict

    def __getstate__(self):
        """Do not pickle the _language_model_dict with this object!"""
        state = self.__dict__.copy()
        del state['_language_model_dict']
        return state

    def __setstate__(self, state):
        """_language_model_dict not pickled with the object!"""
        self.__dict__.update(state)
        self._language_model_dict = None

    def get_language_model_dict(self) -> Optional[Optional[Dict[str, SentenceEncoderBase]]]:
        """ Return a reference to the language model dict. """
        return self._language_model_dict

    def set_language_model_dict(self, language_model_dict: Dict[str, SentenceEncoderBase]) -> None:
        """Set or update the language model dict. An update is required after unpickling!
        See refresh_model_vectors to also update the model's sentence vectors if a new language model was supplied."""
        self._language_model_dict = language_model_dict

    @abstractmethod
    def train_online(self,
                     training_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
                     testing_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of labelled samples (text, label, lang_code)
        :param testing_list: List of labelled samples (text, label, lang_code) to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        pass

    @abstractmethod
    def train(self,
              training_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
              testing_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]]) -> bool:
        """
        Reset and train the classifier with expression-label pairs

        :param training_list: List of labelled samples (text, label, lang_code).
        :param testing_list: List of labelled samples (text, label, lang_code) to test accuracy & overfit during training.
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
    def classify(self, input_text: str, lang_code_hint: Optional[str],
                 weak_match_threshold: float,
                 top_n: int) -> Tuple[List[Tuple[str, float]], str]:
        """ Find the n best matches to the input text.

        :param input_text: The expression to classify.
        :param lang_code_hint: A hint for the language of the input text.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)] plus the lang_code of the input text.
        """
        pass

    @abstractmethod
    def run_tsne(self, n_components: int,
                 perplexity: float, learning_rate: float) -> List[Tuple[str, str, float, float, float]]:
        """
        Generate a non-linear TSNE projection and return the lower dimensional vectors.

        :param n_components: The number of dimensions (2 or 3) to project down to.
        :param perplexity: The perplexity to use during the optimisation process.
        :param learning_rate: The learning rate to use during the optimisation process.
        :return: A list of lower dimensional samples (text, label, x, y, z).
        """
        pass
