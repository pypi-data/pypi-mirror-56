"""
Feersum Vision Engine

"""

import logging
# import os

from typing import Dict, Tuple, List, Optional, Union  # noqa # pylint: disable=unused-import

from feersum_nlu import __version__ as feersum_vision_version

from feersum_nlu.models.image_encoder_base import ImageEncoderBase
from feersum_nlu.models.image_encoder_resnet import ImageEncoderResnet

from feersum_nlu.models.image_classifier_base import ImageClassifierBase
from feersum_nlu.models.image_duo_encoder_classifier_resnet import ImageDuoEncoderClassifierResnet

from feersum_nlu.models.image_reader_base import ImageReaderBase

from feersum_nlu import engine_utils


# === Accomodate unpickling, etc. of modules that have changed path ===#
# import sys
# from feersum_nlu.models import text_classifier_legacy

# Put the models in the sys paths expected by the objects pickled earlier.
# # ToDo: Check the migration status in the DB and if the below is still required.
# e.g. sys.modules['feersum_nlu.text_classifier'] = text_classifier_legacy
# === === #


# === === #
# data_path = os.path.expanduser("~/.nlu")

feers_img_encoder_dict = {"feers_resnet": ""}

feers_img_encoder_prod_list: List[str] = []

feers_img_encoder_long_name_dict = {"feers_resnet": "Resnet used as an image encoder."}

feers_img_encoder_type_dict = {"feers_resnet": "Resnet Image Encoder"}

# Small default language model.
feers_img_encoder_default = 'feers_resnet'

# === === #


def get_version() -> str:
    """ Return the version string defined in __init__.py """
    return str(feersum_vision_version)


class VisionEngine(object):
    """
    Feersum Vision Engine
    """

    def __init__(self) -> None:

        # Dictionaries of named instances of loaded machine learning models.
        self._vision_model_dict = {}  # type: Dict[str, ImageEncoderBase]

        self._image_clsfr_dict = {}  # type: Dict[str, ImageClassifierBase]

    # =========================================================================
    # === Image classifier functionality =======================================
    # =========================================================================
    # === Generic Image Classifier Interface (GTCI) ===
    def test_image_clsfr(self, name: str,
                         testing_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str]]],
                         weak_match_threshold: float,
                         top_n: int) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """
        Test the image classification with provided test set.

        :param name: The unique string identifier of the classifier
        :param testing_list: is a list of testing tuples (image, class_label)
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The 'n' in 'n-best'/top_n to consider when calculating the accuracy.
        :return: The image classifier accuracy, f1 score and confusion matrix and confusion matrix labels.
        """
        result_list = []  # type: List[Tuple[str, str, List[str], Optional[str]]]

        image_clsfr = self._image_clsfr_dict.get(name)

        if image_clsfr is not None and len(testing_list) > 0:
            confusion_matrix_labels = {'_nc': '_nc'}  # type: Dict[str, str]

            for testing_sample in testing_list:
                image = testing_sample[0]
                image_uuid = testing_sample[len(testing_sample) - 1] if len(testing_sample) == 3 \
                    else None  # type: Optional[str]

                true_label = testing_sample[1]  # the matrix row label
                true_label_id = str(image_clsfr.get_label_idx(true_label))

                predicted_results = self.retrieve_image_class(name=name,
                                                              input_image=image,
                                                              weak_match_threshold=weak_match_threshold,
                                                              top_n=top_n)
                # predicted_results = List[Tuple[str, float]]

                predicted_labels = [result[0] for result in predicted_results]
                predicted_label_ids = \
                    [str(image_clsfr.get_label_idx(predicted_label)) for predicted_label in predicted_labels]

                ########
                # Update the confusion matrix labels.
                confusion_matrix_labels[true_label_id] = true_label

                # Update the confusion matrix labels with the predicted results as well to get full coverage.
                for idx, predicted_label in enumerate(predicted_labels):
                    confusion_matrix_labels[predicted_label_ids[idx]] = predicted_label
                ########

                result_list.append((image, true_label_id, predicted_label_ids, image_uuid))

            # Tuple[float, float, Dict[str, Dict[str, int]]]
            accuracy, f1, confusion_matrix = engine_utils.analyse_clsfr_results(result_list)

            return accuracy, f1, confusion_matrix, confusion_matrix_labels
        else:
            return 0.0, 0.0, {}, {}

    def train_image_clsfr(self, name: str,
                          training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                          testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                          clsfr_algorithm: Optional[str],
                          num_epochs: Optional[int]) -> bool:
        """
        Reset and then train the image classification from example image.

        Reset and then train the image classification from example image. Note that the previously loaded or
        trained named instance is lost!

        :param name: The unique string identifier of the classifier
        :param training_list: is a list of training tuples (image, class_label)
        :param testing_list: List of tuples (image, class_label) used to test performance & over fitting.
        :param clsfr_algorithm: The name of the algorithm that should be used for the classification. Default is NaiveBayes.
        :param num_epochs: The number of epochs to train the model for.
        :return: True if training successful.
        """

        # === Model factory ===
        image_clsfr = None  # type: Optional[ImageClassifierBase]

        if num_epochs is None:
            num_epochs = 30

        if (clsfr_algorithm is None) or (clsfr_algorithm == "resnet152"):
            image_clsfr = ImageDuoEncoderClassifierResnet()
        else:
            logging.error(f"vision_engine.VisionEngine.train_image_clsfr(): {clsfr_algorithm} clsfr_algorithm not found!")
            return False
        # === ===

        if image_clsfr is not None:
            success = image_clsfr.train(training_list, testing_list, num_epochs)

            if success:
                self._image_clsfr_dict[name] = image_clsfr
                return True

        return False

    def train_image_clsfr_online(self, name: str,
                                 training_list: List[Tuple[str, str]],
                                 testing_list: List[Tuple[str, str]]) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param name: The instance name.
        :param training_list: The list of training samples List[Tuple[image, label]].
        :param testing_list: The list of testing samples List[Tuple[image, label]].
        :return: True if training was successful.
        """
        image_clsfr = self._image_clsfr_dict.get(name)

        if image_clsfr is not None:
            return image_clsfr.train_online(training_list, testing_list)
        else:
            return False

    def retrieve_image_class(self,
                             name: str,
                             input_image: str,
                             weak_match_threshold: float,
                             top_n: int) -> List[Tuple[str, float]]:
        """
        Classify the input image.

        :param name: Instance name.
        :param input_image: Base64 encoded image.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number of labels to return.
        :return: List of (label, score) sorted from high to low probability.
        """
        image_clsfr = self._image_clsfr_dict.get(name)

        if image_clsfr is not None:
            scored_label_list = image_clsfr.classify(input_image, weak_match_threshold, top_n)
            # scored_label_list = List[Tuple[label, score]]

            return scored_label_list
        else:
            return []

    def get_image_clsfr_labels(self, name: str) -> Optional[List[str]]:
        image_clsfr = self._image_clsfr_dict.get(name)

        if image_clsfr is not None:
            return image_clsfr.get_labels()
        else:
            return None

    def save_image_clsfr(self, name: str, use_data_folder=False) -> bool:
        """Save the image classifier."""
        blobname = name + '.image_clsfr_pickle'
        image_clsfr = self._image_clsfr_dict.get(name)

        if image_clsfr is not None:
            return engine_utils.save_blob(name=blobname,
                                          blob=image_clsfr,
                                          use_data_folder=use_data_folder)
        else:
            return False

    def load_image_clsfr(self, name: str,
                         use_data_folder=False) -> bool:
        """
        Load or reload the image classifier.
        """
        blobname = name + '.image_clsfr_pickle'

        obj = engine_utils.load_blob(name=blobname,
                                     use_data_folder=use_data_folder,
                                     cached_blob=self._image_clsfr_dict.get(name))

        if obj is not None:
            # ToDo: Check if the un-pickled object is of the right type. Do this for all model types!

            self._image_clsfr_dict[name] = obj
            return True
        else:
            # Model not available so delete from local cache and return failure.
            if self._image_clsfr_dict.get(name) is not None:
                del self._image_clsfr_dict[name]

            return False

    def trash_image_clsfr(self, name: str, trash_cache_only: bool = False) -> bool:
        """Unload from memory and trash the blob in storage system."""
        if not trash_cache_only:
            blobname = name + '.image_clsfr_pickle'
            engine_utils.trash_blob(name=blobname, use_data_folder=False)

        if self._image_clsfr_dict.get(name) is not None:
            del self._image_clsfr_dict[name]
            return True
        else:
            return False

    def vaporise_image_clsfr(self, name: str) -> bool:
        """Unload from memory and permanently delete the blob in storage system."""
        blobname = name + '.image_clsfr_pickle'
        engine_utils.vaporise_blob(name=blobname, use_data_folder=False)

        if self._image_clsfr_dict.get(name) is not None:
            del self._image_clsfr_dict[name]
            return True
        else:
            return False

    def get_image_classifier(self, name: str) -> Optional[ImageClassifierBase]:
        """Return a reference to the named ImageClassifierBase child instance."""
        return self._image_clsfr_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Image text reader functionality =====================================
    # =========================================================================
    def retrieve_image_text(self,
                            name: str,
                            input_image: str) -> List[Dict]:
        """
        Read the text in the input image.

        :param name: Instance name.
        :param input_image: Base64 encoded image.
        :return: List of {"text": "...", "lang_code": "..."}.
        """
        text_list = ImageReaderBase.read_text(input_image)
        return text_list

    # =========================================================================
    # === Vision Model ========================================================
    # =========================================================================
    def create_resnet_encoder(self, name: str,
                              model_url: str) -> bool:
        """Create named instance of ImageEncoderResnet encoder."""
        model = ImageEncoderResnet()

        if model.is_created():
            self._vision_model_dict[name] = model
            return True
        else:
            # The model didn't load properly.
            return False

    def create_feers_vision_model(self, name: str) -> bool:
        """Create named vision model from pre-defined feers lists. """
        model_path = feers_img_encoder_dict.get(name)

        if model_path is not None:
            encoder_type = feers_img_encoder_type_dict.get(name)

            if encoder_type == 'Resnet Image Encoder':
                return self.create_resnet_encoder(name, model_path)
            else:
                logging.error(f"create_feers_vision_model: {name} not found!")
                return False
        else:
            return False

    def save_vision_model(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.vision_model_pickle', self._vision_model_dict)

    def load_vision_model(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.load_model(name, use_data_folder, '.vision_model_pickle', self._vision_model_dict)

    def trash_vision_model(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.vision_model_pickle', self._vision_model_dict)

    def vaporise_vision_model(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.vision_model_pickle', self._vision_model_dict)

    def get_vision_model(self, name: str) -> Optional[ImageEncoderBase]:
        vision_model = self._vision_model_dict.get(name)

        # Try and load the vision model from the predefined feers list if not yet loaded.
        if vision_model is None:
            self.create_feers_vision_model(name)
            vision_model = self._vision_model_dict.get(name)

        return vision_model
