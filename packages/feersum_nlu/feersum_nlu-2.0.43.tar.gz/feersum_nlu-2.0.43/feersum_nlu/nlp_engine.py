"""
Feersum Natural Language Processing Engine

"""

import random
import logging
import re
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse as urllib_parse

from typing import Dict, Tuple, List, Optional, Set, Union  # noqa # pylint: disable=unused-import

import dateparser

from feersum_nlu import nlp_engine_data
from feersum_nlu import __version__ as feersum_nlu_version

from feersum_nlu.models import lid
from feersum_nlu.models.sentence_encoder_base import SentenceEncoderBase
from feersum_nlu.models.sentence_encoder_usent import SentenceEncoderUSent
from feersum_nlu.models.sentence_encoder_elmo import SentenceEncoderElmo
from feersum_nlu.models.word_manifold import WordManifold

from feersum_nlu.models.faq_matcher import QuestionT
from feersum_nlu.models.faq_matcher import FAQMatcher
from feersum_nlu.models.intent_classifier import ExpressionT
from feersum_nlu.models.intent_classifier import IntentClassifier

from feersum_nlu.models.text_classifier_base import TextClassifierBase
from feersum_nlu.models.text_classifier_naive_bayes import TextClassifierNB
from feersum_nlu.models.text_classifier_svm import TextClassifierSVM
from feersum_nlu.models.text_classifier_nn_l1 import TextClassifierNearestNeighbourL1
from feersum_nlu.models.text_classifier_nn_cosine import TextClassifierNearestNeighbourCosine

from feersum_nlu.models.crf_extractor import CRFSample
from feersum_nlu.models.crf_extractor import CRFExtractor

from feersum_nlu.models.synonym_extractor import SynonymSample
from feersum_nlu.models.synonym_extractor import SynonymEntity  # noqa # pylint: disable=unused-import
from feersum_nlu.models.synonym_extractor import SynonymExtractor

from feersum_nlu.models.sentiment_analyser import SentimentAnalyser
from feersum_nlu.models.emotion_analyser import EmotionAnalyser
from feersum_nlu.models.person_name_extractor import PersonNameExtractor

from feersum_nlu import engine_utils

# === Accomodate unpickling, etc. of modules that have changed path ===#
import sys
from feersum_nlu.models import word_manifold
from feersum_nlu.models import faq_matcher
from feersum_nlu.models import intent_classifier
from feersum_nlu.models import sentiment_analyser

# Put the models in the sys paths expected by the objects pickled earlier.
# ToDo: Check the migration status in the DB and which of the below is still required!
# e.g. sys.modules['feersum_nlu.text_classifier'] = text_classifier_legacy
# sys.modules['feersum_nlu.text_classifier'] = text_classifier_legacy
# sys.modules['feersum_nlu.models.text_classifier'] = text_classifier_legacy
sys.modules['feersum_nlu.word_manifold'] = word_manifold
sys.modules['feersum_nlu.faq_matcher'] = faq_matcher
sys.modules['feersum_nlu.intent_classifier'] = intent_classifier
sys.modules['feersum_nlu.sentiment_analyser'] = sentiment_analyser

# === === #
feers_sent_encoder_dict = {"glove6B50D_trimmed": "glove.6B.50d.trimmed.txt",
                           "feers_wm_afr": "wiki.af.vec",
                           "feers_wm_eng": "glove.6B.200d.txt",
                           "feers_wm_nbl": "wiki.xh.vec",
                           # There is no nbl word embedding yet. Load the xhosa one!
                           "feers_wm_xho": "wiki.xh.vec",
                           "feers_wm_zul": "wiki.zu.vec",
                           "feers_wm_ssw": "wiki.ss.vec",
                           "feers_wm_nso": "wiki.nso.vec",
                           "feers_wm_sot": "wiki.st.vec",
                           "feers_wm_tsn": "wiki.tn.vec",
                           "feers_wm_ven": "wiki.ve.vec",
                           "feers_wm_tso": "wiki.ts.vec",
                           # ToDo: Move the usent and elmo models to the GCP bucket.
                           "feers_usent_eng": "https://tfhub.dev/google/universal-sentence-encoder-large/3?"
                                              "tf-hub-format=compressed",
                           "feers_elmo_eng": "https://tfhub.dev/google/elmo/2?"
                                             "tf-hub-format=compressed"}

feers_sent_encoder_prod_list: List[str] = ["glove6B50D_trimmed",
                                           "feers_wm_afr",
                                           "feers_wm_eng",
                                           "feers_wm_xho",
                                           "feers_wm_zul",
                                           "feers_wm_nso"]

# ToDo: Don't download directly from he hub.
# # Create a folder for the TF hub module.
# $ mkdir /tmp/moduleA
# # Download the module, and uncompress it to the destination folder. You might want to do this manually.
# $ curl -L "https://tfhub.dev/google/universal-sentence-encoder/2?tf-hub-format=compressed" | tar -zxvC /tmp/moduleA
# # Test to make sure it works.
# $ python
# > import tensorflow_hub as hub
# > hub.Module("/tmp/moduleA")

feers_sent_encoder_long_name_dict = {"glove6B50D_trimmed": "Small Stanford Glove Word Embedding for English",
                                     "feers_wm_afr": "FastText Word Manifold for Afrikaans",
                                     "feers_wm_eng": "Glove Word Manifold for English",
                                     "feers_wm_nbl": "FastText Word Manifold for isiXhosa (REUSED for isiNdebele)",
                                     "feers_wm_xho": "FastText Word Manifold for isiXhosa",
                                     "feers_wm_zul": "FastText Word Manifold for isiZulu",
                                     "feers_wm_ssw": "FastText Word Manifold for siSwati",
                                     "feers_wm_nso": "FastText Word Manifold for Sepedi",
                                     "feers_wm_sot": "FastText Word Manifold for Sesotho",
                                     "feers_wm_tsn": "FastText Word Manifold for Setswana",
                                     "feers_wm_ven": "FastText Word Manifold for Tshivenda",
                                     "feers_wm_tso": "FastText Word Manifold for Xitsonga",
                                     "feers_usent_eng": "Google's Usent encoder for English",
                                     "feers_elmo_eng": "Elmo encoder for English"}

feers_sent_encoder_type_dict = {"glove6B50D_trimmed": "Glove WordManifold",
                                "feers_wm_afr": "FastText WordManifold",
                                "feers_wm_eng": "Glove WordManifold",
                                "feers_wm_nbl": "FastText WordManifold",
                                "feers_wm_xho": "FastText WordManifold",
                                "feers_wm_zul": "FastText WordManifold",
                                "feers_wm_ssw": "FastText WordManifold",
                                "feers_wm_nso": "FastText WordManifold",
                                "feers_wm_sot": "FastText WordManifold",
                                "feers_wm_tsn": "FastText WordManifold",
                                "feers_wm_ven": "FastText WordManifold",
                                "feers_wm_tso": "FastText WordManifold",
                                "feers_usent_eng": "USent Sentence Encoder",
                                "feers_elmo_eng": "Elmo Sentence Encoder"}

# Small default language model.
feers_sent_encoder_default = 'glove6B50D_trimmed'


# === === #


def get_version() -> str:
    """ Return the version string defined in __init__.py """
    return str(feersum_nlu_version)


class NLPEngine(object):
    """
    Feersum Natural Language Processing Engine
    """

    def __init__(self,
                 use_duckling: bool = True,
                 duckling_url: str = 'https://qonda.qa.feersum.io') -> None:
        self._use_duckling = use_duckling
        self._duckling_url = duckling_url

        # Dictionaries of named instances of loaded machine learning models.
        self._language_model_dict = {}  # type: Dict[str, SentenceEncoderBase]

        self._text_clsfr_dict = {}  # type: Dict[str, TextClassifierBase]
        self._faq_dict = {}  # type: Dict[str, FAQMatcher]
        self._intent_clsfr_dict = {}  # type: Dict[str, IntentClassifier]
        self._crf_extr_dict = {}  # type: Dict[str, CRFExtractor]
        self._synonym_extr_dict = {}  # type: Dict[str, SynonymExtractor]

        # Create single 'generic' instances of some models that only needs one instance for now.
        self._sentiment_analyzer = SentimentAnalyser()

        emo_blob_folder_name = "emotion_analysis_experiment/pretrained"
        emo_blob_file_name = "export_emo_clas.pkl"
        emo_local_file_cache_path, emo_blob_file_name = \
            nlp_engine_data.get_blob_from_gcp_bucket(emo_blob_folder_name, emo_blob_file_name)
        self._emotion_analyser = EmotionAnalyser(emo_local_file_cache_path, emo_blob_file_name)

    def set_duckling_url(self, duckling_url: str = 'https://qonda.feersum.io'):
        self._duckling_url = duckling_url

    # =========================================================================
    # === Text classifier functionality =======================================
    # =========================================================================
    # === Generic Text Classifier Interface (GTCI) ===
    def test_text_clsfr(self, name: str,
                        testing_list: Union[List[Tuple[str, str, str, str]], List[Tuple[str, str, str]]],
                        weak_match_threshold: float,
                        top_n: int) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """
        Test the text classification with provided test set.

        :param name: The unique string identifier of the classifier
        :param testing_list: is a list of testing tuples (text, class_label, language_hint)
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The 'n' in 'n-best'/top_n to consider when calculating the accuracy.
        :return: The text classifier accuracy, f1 score and confusion matrix and confusion matrix labels.
        """
        result_list = []  # type: List[Tuple[str, str, List[str], Optional[str]]]

        text_clsfr = self._text_clsfr_dict.get(name)

        if text_clsfr is not None and len(testing_list) > 0:
            confusion_matrix_labels = {'_nc': '_nc'}  # type: Dict[str, str]

            for testing_sample in testing_list:
                text = testing_sample[0]
                text_uuid = testing_sample[len(testing_sample) - 1] if len(testing_sample) == 4 \
                    else None  # type: Optional[str]

                true_label = testing_sample[1]  # the matrix row label
                true_label_id = str(text_clsfr.get_label_idx(true_label))

                predicted_results, lang_code = self.retrieve_text_class(name=name,
                                                                        input_text=text,
                                                                        lang_code=None,  # No language hint when testing.
                                                                        weak_match_threshold=weak_match_threshold,
                                                                        top_n=top_n)
                # predicted_results = List[Tuple[str, float]]

                predicted_labels = [result[0] for result in predicted_results]
                predicted_label_ids = \
                    [str(text_clsfr.get_label_idx(predicted_label)) for predicted_label in predicted_labels]

                ########
                # Update the confusion matrix labels.
                confusion_matrix_labels[true_label_id] = true_label

                # Update the confusion matrix labels with the predicted results as well to get full coverage.
                for idx, predicted_label in enumerate(predicted_labels):
                    confusion_matrix_labels[predicted_label_ids[idx]] = predicted_label
                ########

                result_list.append((text, true_label_id, predicted_label_ids, text_uuid))

            # Tuple[float, float, Dict[str, Dict[str, int]]]
            accuracy, f1, confusion_matrix = engine_utils.analyse_clsfr_results(result_list)

            return accuracy, f1, confusion_matrix, confusion_matrix_labels
        else:
            return 0.0, 0.0, {}, {}

    def train_text_clsfr(self, name: str,
                         training_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
                         testing_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
                         clsfr_algorithm: Optional[str],
                         language_model_name_dict: Dict[str, str]) -> bool:
        """
        Reset and then train the text classification from example text.

        Reset and then train the text classification from example text. Note that the previously loaded or
        trained named instance is lost!

        :param name: The unique string identifier of the classifier
        :param training_list: is a list of training tuples (text, class_label)
        :param testing_list: List of tuples (text, class_label) used to test performance & over fitting.
        :param clsfr_algorithm: The name of the algorithm that should be used for the classification. Default is NaiveBayes.
        :param language_model_name_dict: The names of the language models to use for the lang codes in the associated model.
        :return: True if training successful.
        """

        language_model_dict = {}

        # Convert language model name dict to a dict of language model objects.
        for lang_code, model_name in language_model_name_dict.items():
            lang_model = self.get_language_model(model_name)  # type: Optional[SentenceEncoderBase]

            if lang_model is not None:
                language_model_dict[lang_code] = lang_model
            else:
                logging.error(f"nlp_engine.NLPEngine.train_text_clsfr(): {model_name} language model not found!")
                return False

        text_clsfr = None  # type: Optional[TextClassifierBase]

        # === Model factory ===
        if (clsfr_algorithm is None) or (clsfr_algorithm == "naive_bayes"):
            text_clsfr = TextClassifierNB(language_model_dict)
        elif clsfr_algorithm == "svm":
            text_clsfr = TextClassifierSVM(language_model_dict)
        elif len(language_model_dict) > 0:
            if clsfr_algorithm == "nearest_neighbour_l1":
                text_clsfr = TextClassifierNearestNeighbourL1(language_model_dict)
            elif clsfr_algorithm == "nearest_neighbour_cosine":
                text_clsfr = TextClassifierNearestNeighbourCosine(language_model_dict)
            else:
                logging.error(f"nlp_engine.NLPEngine.train_text_clsfr(): {clsfr_algorithm} clsfr_algorithm not found!")
                return False
        # === ===

        if text_clsfr is not None:
            success = text_clsfr.train(training_list, testing_list)

            if success:
                self._text_clsfr_dict[name] = text_clsfr
                return True

        return False

    def train_text_clsfr_online(self, name: str,
                                training_list: List[Tuple[str, str, str]],
                                testing_list: List[Tuple[str, str, str]]) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param name: The instance name.
        :param training_list: The list of training samples List[Tuple[text, label, lang_id]].
        :param testing_list: The list of testing samples List[Tuple[text, label, lang_id]].
        :return: True if training was successful.
        """
        text_clsfr = self._text_clsfr_dict.get(name)

        if text_clsfr is not None:
            return text_clsfr.train_online(training_list, testing_list)
        else:
            return False

    def retrieve_text_class(self,
                            name: str,
                            input_text: str, lang_code: Optional[str],
                            weak_match_threshold: float,
                            top_n: int) -> Tuple[List[Tuple[str, float]], Optional[str]]:
        """
        Classify the input text.

        :param name: Instance name.
        :param input_text: Expression from user to be matched against intents.
        :param lang_code: A hint for the language code of the input.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number of labels to return.
        :return: List of (label, score) sorted from high to low probability + lang_code of text.
        """
        text_clsfr = self._text_clsfr_dict.get(name)

        if text_clsfr is not None:
            scored_label_list, lang_code = text_clsfr.classify(input_text, lang_code,
                                                               weak_match_threshold,
                                                               top_n)
            # scored_label_list = List[Tuple[label, score]]

            return scored_label_list, lang_code
        else:
            return [], None

    def tsne_text_clsfr(self, name: str,
                        n_components: int, perplexity: float, learning_rate: float) -> \
            Optional[List[Tuple[str, str, float, float, float]]]:

        text_clsfr = self._text_clsfr_dict.get(name)

        if text_clsfr is not None:
            return text_clsfr.run_tsne(n_components, perplexity, learning_rate)
        else:
            return None

    def get_text_clsfr_labels(self, name: str) -> Optional[List[str]]:
        text_clsfr = self._text_clsfr_dict.get(name)

        if text_clsfr is not None:
            return text_clsfr.get_labels()
        else:
            return None

    def save_text_clsfr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.text_clsfr_pickle', self._text_clsfr_dict)

    def load_text_clsfr(self, name: str,
                        language_model_name_dict: Dict[str, str],
                        use_data_folder=False) -> bool:
        model_loaded = engine_utils.load_model(name, use_data_folder, '.text_clsfr_pickle', self._text_clsfr_dict)

        if model_loaded:
            # If model loaded then also add the requested language models.
            language_model_dict = {}

            for lang_code, language_model_name in language_model_name_dict.items():
                language_model = self.get_language_model(language_model_name)

                if language_model is not None:
                    language_model_dict[lang_code] = language_model
                else:
                    logging.error(f"nlp_engine.NLPEngine.load_text_clsfr(): {name} needs language model "
                                  f"{language_model_name}, but its not loaded!")

            if len(language_model_dict) == len(language_model_name_dict):
                self._text_clsfr_dict[name].set_language_model_dict(language_model_dict)
                return True
            else:
                # None all of the requested languages were available so unload model and return failure.
                engine_utils.trash_model(name, trash_cache_only=True,
                                         model_extension='.text_clsfr_pickle', model_dict=self._text_clsfr_dict)
                return False
        else:
            return False

    def trash_text_clsfr(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.text_clsfr_pickle', self._text_clsfr_dict)

    def vaporise_text_clsfr(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.text_clsfr_pickle', self._text_clsfr_dict)

    def get_text_classifier(self, name: str) -> Optional[TextClassifierBase]:
        return self._text_clsfr_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Language Model ======================================================
    # =========================================================================
    def create_word_manifold_encoder(self, name: str,
                                     vectors_file: str,
                                     max_vocab: int = 5000000,
                                     stop_words: Optional[Set[str]] = None,
                                     spacies: Optional[List[str]] = None) -> bool:
        """Create named instance of WordManifold encoder."""
        manifold = WordManifold(vectors_file=vectors_file,
                                stop_words=stop_words,
                                spacies=spacies)

        if manifold.is_created() > 0:
            self._language_model_dict[name] = manifold
            return True
        else:
            # The manifold probably didn't load properly.
            return False

    def create_usent_encoder(self, name: str,
                             model_url: str) -> bool:
        """Create named instance of SentenceEncoderUSent encoder."""
        model = SentenceEncoderUSent(model_url)

        if model.is_created():
            self._language_model_dict[name] = model
            return True
        else:
            # The model didn't load properly.
            return False

    def create_elmo_encoder(self, name: str,
                            model_url: str) -> bool:
        """Create named instance of SentenceEncoderElmo encoder."""
        model = SentenceEncoderElmo(model_url)

        if model.is_created():
            self._language_model_dict[name] = model
            return True
        else:
            # The model didn't load properly.
            return False

    def create_feers_language_model(self, name: str) -> bool:
        """Create named language model from pre-defined feers lists. """
        model_path = feers_sent_encoder_dict.get(name)

        if model_path is not None:
            encoder_type = feers_sent_encoder_type_dict.get(name)

            if (encoder_type == 'Glove WordManifold') or (encoder_type == 'FastText WordManifold'):
                local_file_cache_path, blob_file_name = \
                    nlp_engine_data.get_blob_from_gcp_bucket('glove_and_fasttext_ref', model_path)

                manifold_model_path = f"{local_file_cache_path}/{blob_file_name}"

                return self.create_word_manifold_encoder(name, manifold_model_path,
                                                         max_vocab=750000,
                                                         stop_words=None,
                                                         spacies=["&", "#", "@", "？", "~", "”", "“", ".", ",",
                                                                  "?",
                                                                  ";", ":",
                                                                  "!", "(", ")",
                                                                  "{", "}",
                                                                  "[", "]", '"', "'", "`", "’", "-", "–", "/",
                                                                  "\\",
                                                                  "…"])
            elif encoder_type == 'USent Sentence Encoder':
                return self.create_usent_encoder(name, model_path)
            elif encoder_type == 'Elmo Sentence Encoder':
                return self.create_elmo_encoder(name, model_path)
            else:
                logging.error(f"create_feers_language_model: {name} not found!")
                return False
        else:
            return False

    def save_language_model(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.language_model_pickle', self._language_model_dict)

    def load_language_model(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.load_model(name, use_data_folder, '.language_model_pickle', self._language_model_dict)

    def trash_language_model(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.language_model_pickle', self._language_model_dict)

    def vaporise_language_model(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.language_model_pickle', self._language_model_dict)

    def get_language_model(self, name: str) -> Optional[SentenceEncoderBase]:
        language_model = self._language_model_dict.get(name)

        # Try and load the language model from the predefined feers list if not yet loaded.
        if language_model is None:
            self.create_feers_language_model(name)
            language_model = self._language_model_dict.get(name)

        return language_model

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === FAQ matcher =========================================================
    # =========================================================================
    @staticmethod
    def load_faq_matcher_data(questions_filename: str,
                              q2a_filename: str,
                              answers_filename: str,
                              training_ratio: int,
                              testing_ratio: int,
                              min_group_size: int,
                              delim: str) -> Tuple[List[QuestionT], List[QuestionT]]:
        """ Loads the question data (in quora format) and prepares training and testing sets of questions.

        :param questions_filename: The quora format questions file.
        :param q2a_filename: The q2a mapping if available. Set to "" if not available.
        :param answers_filename: The answers file if available. Set to "" if not available.
        :param training_ratio: The number of training questions to use per answer.
        :param testing_ratio: The number of training questions to use per answer.
        :param min_group_size: The minimum sized question groups to use. Set to max training_ratio+testing_ratio to
        :param delim: The column delimeter used in the data file.
        """
        training_list, testing_list = FAQMatcher.load_faq_data(questions_filename,
                                                               q2a_filename,
                                                               answers_filename,
                                                               training_ratio,
                                                               testing_ratio,
                                                               min_group_size,
                                                               delim)
        return training_list, testing_list

    @staticmethod
    def cnvrt_faq_tuples_to_faq_questions(tuple_list: Union[List[Tuple[str, str, str, str]], List[Tuple[str, str, str]]],
                                          existing_questions: Optional[List[QuestionT]] = None) -> List[QuestionT]:
        """
        Convert a list of question,label,lang_code tuples into a list of QuestionTs USING existing
        model samples to allocate label IDs.

        :param tuple_list: List of data tuples (question,label,lang_code).
        :param existing_questions: List of existing questions.
        :return: List of QuestionT.
        """
        return FAQMatcher.cnvrt_tuples_to_questions(tuple_list, existing_questions)

    @staticmethod
    def split_faq_questions(question_list: List[QuestionT],
                            num_training_samples: int,
                            num_testing_samples: int) -> Tuple[List[QuestionT], List[QuestionT]]:
        """
        Split a list of questions into a training set and a testing set.

        :param question_list: The list of questions of all labels.
        :param num_training_samples:  The number of training samples of each label to return.
        :param num_testing_samples: The number of testing samples of each label to return.
        :return: A list of training questions and a list of testing questions.
        """
        training_list = []  # type: List[QuestionT]
        testing_list = []  # type: List[QuestionT]
        answer_id_count_dict = {}  # type: Dict[int, int]

        unsplit_question_list = list(question_list)
        random.shuffle(unsplit_question_list)

        for question in unsplit_question_list:
            answer_id = question.answer_id

            answer_count = answer_id_count_dict.get(answer_id, 0)

            if answer_count < num_training_samples:
                training_list.append(question)
                answer_id_count_dict[answer_id] = answer_count + 1
            elif answer_count < (num_training_samples + num_testing_samples):
                testing_list.append(question)
                answer_id_count_dict[answer_id] = answer_count + 1

        # print("questions per label: ", answer_id_count_dict.items())

        return training_list, testing_list

    def test_faq_matcher(self, name: str,
                         testing_list: List[QuestionT],
                         weak_match_threshold: float,
                         top_n: int) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """ Test the FAQ classifier with the provided test set

        :param name: Instance name.
        :param testing_list: List of tuples of questions and correctly classified answers_ids and answers.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The 'n' in 'n-best'/top_n to consider when calculating the accuracy.
        :return: The FAQ matcher accuracy, f1 score, confusion matrix and confusion matrix labels.
        """
        result_list = []  # type: List[Tuple[str, str, List[str], Optional[str]]]

        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None and len(testing_list) > 0:
            confusion_matrix_labels = {'_nc': '_nc'}

            for testing_sample in testing_list:
                text = testing_sample.text
                text_uuid = None  # type: Optional[str]

                true_label_id = str(testing_sample.answer_id)  # the matrix row label

                predicted_results, lang_code = faq_matcher.find_knn_matches(text,
                                                                            None,  # No language hint when testing.
                                                                            weak_match_threshold,
                                                                            top_n)

                predicted_label_ids = [str(result[1].answer_id) for result in predicted_results]

                ########
                # Update the confusion matrix labels.
                confusion_matrix_labels[true_label_id] = testing_sample.answer

                # Update the confusion matrix labels with the predicted results as well to get full coverage.
                for result in predicted_results:
                    confusion_matrix_labels[str(result[1].answer_id)] = result[1].answer
                ########

                result_list.append((text, true_label_id, predicted_label_ids, text_uuid))

            # Tuple[float, float, Dict[str, Dict[str, int]]]
            accuracy, f1, confusion_matrix = engine_utils.analyse_clsfr_results(result_list)

            return accuracy, f1, confusion_matrix, confusion_matrix_labels
        else:
            return 0.0, 0.0, {}, {}

    def train_faq_matcher(self, name: str,
                          training_list: List[QuestionT],
                          testing_list: List[QuestionT],
                          word_manifold_name_dict: Dict[str, str]) -> bool:
        """ Reset and train the FAQ classifier with question-answer pairs.

        Reset and train the FAQ classifier with question-answer pairs. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of tuples of questions, answer_ids and answers.
        :param testing_list: List of tuples of expressions used to test performance and over fitting during training.
        :param word_manifold_name_dict: Which named instances of WordManifold to use.
        :return: Boolean indicating whether or not the training was successful.
        """
        word_manifold_dict = {}  # type: Dict[str, WordManifold]

        # Convert manifold name dict to a dict of manifold objects.
        for lang_code, manifold_name in word_manifold_name_dict.items():
            language_model = self.get_language_model(manifold_name)

            if (language_model is not None) and (type(language_model) == WordManifold):
                word_manifold_dict[lang_code] = language_model  # type: ignore
            else:
                logging.error(f"nlp_engine.NLPEngine.train_faq_matcher(): {manifold_name} word manifold not found!")
                return False

        if len(word_manifold_dict) > 0:
            faq_matcher = FAQMatcher(word_manifold_dict)

            success = faq_matcher.train(training_list, testing_list)

            if success:
                self._faq_dict[name] = faq_matcher
                return True

        return False

    def train_and_cross_validate_faq_matcher(self, name: str,
                                             training_list: List[QuestionT],
                                             testing_list: List[QuestionT],
                                             word_manifold_name_dict: Dict[str, str],
                                             weak_match_threshold: float = 1.0,
                                             k: int = 5,
                                             n_experiments: int = 30) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """ Reset and train the faq matcher with question-answer pairs.

        Reset and train the faq matcher with question-answer pairs. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of tuples of questions used to train the model.
        :param testing_list: List of tuples of questions used to test performance and over fitting during training.
        :param word_manifold_name_dict: Which named instances of WordManifold to use.
        :param weak_match_threshold: The weak match threshold to use during cross validation testing.
        :param k: The samples are randomised, then every k'th samples of each class is put in the validation set.
        :param n_experiments: The number of validation experiments.
        :return: The validation accuracy, f1 score, confusion matrix and confusion matrix labels.
        """
        word_manifold_dict = {}  # type: Dict[str, WordManifold]

        # Convert manifold name dict to a dict of manifold objects.
        for lang_code, manifold_name in word_manifold_name_dict.items():
            language_model = self.get_language_model(manifold_name)

            if (language_model is not None) and (type(language_model) == WordManifold):
                word_manifold_dict[lang_code] = language_model  # type: ignore
            # else:
            #     print("Error:", manifold_name, "is not loaded!")

        if len(word_manifold_dict) > 0:
            faq_matcher = FAQMatcher(word_manifold_dict)

            # =================================================
            # === Do the cross validation training and testing.
            cross_accuracy_sum = 0.0
            cross_f1_sum = 0.0
            cross_confusion_dict = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
            cross_confusion_labels = {}  # type: Dict[str, str]
            cross_count = 0

            for i in range(n_experiments):
                random.shuffle(training_list)

                cross_training_list = []  # type: List[QuestionT]
                cross_testing_list = []  # type: List[QuestionT]

                clsfr_label_counts = {}  # type: Dict[str, int]

                for question in training_list:
                    label_count = clsfr_label_counts.get(question.answer, 0)
                    clsfr_label_counts[question.answer] = label_count + 1  # Increment the count.

                    if (label_count % k) == 0:
                        cross_testing_list.append(question)
                    else:
                        cross_training_list.append(question)

                success = faq_matcher.train(cross_training_list, [])

                # print(f"    success = {success}")

                if success:
                    self._faq_dict[name] = faq_matcher
                    accuracy, f1, confusion_dict, confusion_labels = \
                        self.test_faq_matcher(name,
                                              cross_testing_list,
                                              weak_match_threshold, 1)

                    # print("Training -", cross_training_list)
                    # print("Testing -", cross_testing_list)

                    # === Update the cross confusion matrix ===
                    for label_a, dict_b in confusion_dict.items():
                        cross_dict_b = cross_confusion_dict.get(label_a, {})

                        for label_b, samples in dict_b.items():
                            cross_samples = cross_dict_b.get(label_b, [])

                            for sample in samples:
                                if sample not in cross_samples:
                                    cross_samples.append(sample)

                            cross_dict_b[label_b] = cross_samples

                        cross_confusion_dict[label_a] = cross_dict_b
                    # === ===

                    cross_confusion_labels = confusion_labels
                    cross_accuracy_sum += accuracy
                    cross_f1_sum += f1
                    cross_count += 1

                    # print(f"    cross_count = {cross_count}")
                    # print(f"    train(): cross_accuracy = {accuracy}")
                    # print(f"    train(): cross_f1 = {f1}")
                    # print(f"    train(): confusion_dict = {confusion_dict}")
                    # print(f"    train(): confusion_labels = {confusion_labels}")
                    # print(f"    train(): cross_accuracy_avrg = {cross_accuracy_sum / cross_count}")
                    # print(f"    train(): cross_f1_avrg = {cross_f1_sum / cross_count}")
                    # print(f"    train(): cross_confusion_dict = {cross_confusion_dict}")
                    # print(f"    train(): cross_confusion_labels = {cross_confusion_labels}")
                    # print()
            # =================================================

            # Final train cycle with ALL training samples.
            success = faq_matcher.train(training_list, testing_list)

            if (cross_count > 0) and success:
                self._faq_dict[name] = faq_matcher
                cross_accuracy = cross_accuracy_sum / cross_count
                cross_f1 = cross_f1_sum / cross_count
                return cross_accuracy, cross_f1, cross_confusion_dict, cross_confusion_labels

        return 0.0, 0.0, {}, {}

    def train_faq_matcher_online(self, name: str,
                                 training_list: List[QuestionT],
                                 testing_list: List[QuestionT]) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param name: The instance name.
        :param training_list: The list of training samples List[Tuple[text, label, lang_id]].
        :param testing_list: The list of testing samples List[Tuple[text, label, lang_id]].
        :return: True if training was successful.
        """
        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            return faq_matcher.train_online(training_list, testing_list)
        else:
            return False

    def get_model_faq_matcher_questions(self, name: str) -> Optional[List[QuestionT]]:
        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            return faq_matcher.get_model_questions()
        else:
            return None

    def retrieve_faqs(self,
                      name: str,
                      input_text: str, lang_code: Optional[str],
                      weak_match_threshold: float,
                      top_n: int) -> Tuple[List[Tuple[str, int, str, float, str]], Optional[str]]:
        """ Retrieve a list of matching FAQs.

        :param name: Instance name.
        :param input_text: Question asked by user to be matched against FAQ.
        :param lang_code: A hint for the language code of the input.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number of labels to return.
        :return: List of probable question and answer_id,answer_text pairs sorted from high to low probability and
            tagged with language of matched question. The language code of the input text is also returned.
            Note: If only one manifold is used then the input language is assumed to be of that language!!
        """
        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            retrieved_matches = []  # type: List[Tuple[str, int, str, float, str]]

            best_matches, lang_code = faq_matcher.find_knn_matches(input_text, lang_code,
                                                                   weak_match_threshold,
                                                                   top_n)

            # Reformat the result list to not have the question vector.
            for score, question in best_matches:
                retrieved_matches.append((question.text, question.answer_id,
                                          question.answer, score, question.lang_code))

            return retrieved_matches, lang_code
        else:
            return [], None

    def tsne_faq_matcher(self, name: str,
                         n_components: int, perplexity: float, learning_rate: float) -> \
            Optional[List[Tuple[str, str, float, float, float]]]:

        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            return faq_matcher.run_tsne(n_components, perplexity, learning_rate)
        else:
            return None

    def get_faq_matcher_word_manifold_dict(self, name: str) -> Optional[Dict[str, WordManifold]]:
        """Returns the associated word manifold instances."""
        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            return faq_matcher.get_word_manifold_dict()
        else:
            return None

    def get_faq_matcher_labels(self, name: str) -> Optional[List[str]]:
        faq_matcher = self._faq_dict.get(name)

        if faq_matcher is not None:
            return faq_matcher.get_labels()
        else:
            return None

    def save_faq_matcher(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.faq_matcher_pickle', self._faq_dict)

    def load_faq_matcher(self, name: str,
                         word_manifold_name_dict: Dict[str, str],
                         use_data_folder=False) -> bool:
        model_loaded = engine_utils.load_model(name, use_data_folder, '.faq_matcher_pickle', self._faq_dict)

        if model_loaded:
            # If model loaded then also add the requested language models.
            word_manifold_dict = {}  # type: Dict[str, WordManifold]

            for lang_code, manifold_name in word_manifold_name_dict.items():
                language_model = self.get_language_model(manifold_name)

                if (language_model is not None) and (type(language_model) == WordManifold):
                    word_manifold_dict[lang_code] = language_model  # type: ignore
                else:
                    logging.error(f"nlp_engine.NLPEngine.load_faq_matcher(): {name} needs word manifold "
                                  f"{manifold_name}, but its not loaded!")

            if len(word_manifold_dict) > 0:
                self._faq_dict[name].set_word_manifold_dict(word_manifold_dict)
                return True
            else:
                # None of the languages available so unload model and return failure.
                engine_utils.trash_model(name, trash_cache_only=True,
                                         model_extension='.faq_matcher_pickle', model_dict=self._faq_dict)
                return False
        else:
            return False

    def trash_faq_matcher(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.faq_matcher_pickle', self._faq_dict)

    def vaporise_faq_matcher(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.faq_matcher_pickle', self._faq_dict)

    def get_faq_matcher(self, name: str) -> Optional[FAQMatcher]:
        return self._faq_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Intent classifier ===================================================
    # =========================================================================
    @staticmethod
    def load_intent_splitsco_file_r1(file_name: str) -> List[Tuple[str, str, str]]:
        """ Load splits.ai intent file that is part of their NLU benchmark. """
        expression_tuples = IntentClassifier.load_splitsco_file_r1(file_name)
        return expression_tuples

    @staticmethod
    def load_intent_splitsco_file_r2(file_name: str) -> List[Tuple[str, str, str]]:
        """ Load splits.ai intent file that is part of their NLU benchmark. """
        expression_tuples = IntentClassifier.load_splitsco_file_r2(file_name)
        return expression_tuples

    @staticmethod
    def cnvrt_intent_tuples_to_expressions(tuple_list: Union[List[Tuple[str, str, str, str]], List[Tuple[str, str, str]]],
                                           existing_expressions: Optional[List[ExpressionT]] = None) -> \
            List[ExpressionT]:
        """
        Convert a list of expression,label,lang_code tuples into a list of ExpressionTs USING existing
        model samples to allocate label IDs.

        :param tuple_list: List of data tuples (expression,label,lang_code).
        :param existing_expressions: List of existing expressions.
        :return: List of ExpressionTs.
        """
        return IntentClassifier.cnvrt_tuples_to_expressions(tuple_list, existing_expressions)

    @staticmethod
    def split_intent_expressions(expression_list: List[ExpressionT],
                                 num_training_samples: int,
                                 num_testing_samples: int) -> Tuple[List[ExpressionT], List[ExpressionT]]:
        """
        Split a list of expressions (of multiple labelled intents) into a training set and a testing set.

        :param expression_list: The list of expressions of all labels.
        :param num_training_samples:  The number of training samples of each label to return.
        :param num_testing_samples: The number of testing samples of each label to return.
        :return: A list of training expressions and a list of testing expressions.
        """
        training_list = []  # type: List[ExpressionT]
        testing_list = []  # type: List[ExpressionT]
        intent_count_dict = {}  # type: Dict[str, int]

        unsplit_expression_list = list(expression_list)
        random.shuffle(unsplit_expression_list)

        for expression in unsplit_expression_list:
            intent_label = expression.intent_label

            intent_count = intent_count_dict.get(intent_label, 0)

            if intent_count < num_training_samples:
                training_list.append(expression)
                intent_count_dict[intent_label] = intent_count + 1
            elif intent_count < (num_training_samples + num_testing_samples):
                testing_list.append(expression)
                intent_count_dict[intent_label] = intent_count + 1

        # print("Expressions per label: ", intent_count_dict.items())

        return training_list, testing_list

    @staticmethod
    def save_intent_expressions(list_name: str,
                                path: str,
                                expression_list: List[ExpressionT]) -> bool:
        """
        Save a .tsv file with the expression, label and label_id of each sample.

        :param list_name: name of file to write. The path and .tsv extension is added to the name given.
        :param path: Path to save file at.
        :param expression_list: The list of expressions to save.
        :return: Boolean indicating success or failure of the save operation.
        """
        if path is None or path == "":
            path = "."

        filename = path + '/' + list_name + '.tsv'

        try:
            handle = open(filename, 'w')

            handle.write("text \t label \t label_id \n")

            for expression in expression_list:
                text = '{0}\t{1}\t{2}\n'.format(expression.text.replace('\n', '').replace('\t', ' '),
                                                expression.intent_label.replace('\n', '').replace('\t', ' '),
                                                expression.intent_id)
                # print(text)
                handle.write(text)

            handle.close()

            return True
        except IOError:
            # print("save_intent_expressions error!")
            pass

        return False

    def test_intent_clsfr(self, name: str,
                          testing_list: List[ExpressionT],
                          weak_match_threshold: float,
                          top_n: int) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """
        Test the intent classifier with the provided test set

        :param name: Instance name.
        :param testing_list: List of tuples of expressions and correctly classified labels.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The 'n' in 'n-best'/top_n to consider when calculating the accuracy.
        :return: The intent classifier's accuracy, f1 score, confusion matrix and confusion matrix labels.
        """
        result_list = []  # type: List[Tuple[str, str, List[str], Optional[str]]]

        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None and len(testing_list) > 0:
            confusion_matrix_labels = {'_nc': '_nc'}  # type: Dict[str, str]

            for testing_sample in testing_list:
                text = testing_sample.text
                text_uuid = None  # type: Optional[str]

                true_label_id = str(testing_sample.intent_id)  # the matrix row label

                predicted_results, lang_code = intent_clsfr.find_knn_matches(testing_sample.text,
                                                                             None,  # No language hint when testing.
                                                                             weak_match_threshold,
                                                                             top_n)

                predicted_label_ids = [str(result[1].intent_id) for result in predicted_results]

                ########
                # Update the confusion matrix labels.
                confusion_matrix_labels[true_label_id] = testing_sample.intent_label

                # Update the confusion matrix labels with the predicted results as well to get full coverage.
                for result in predicted_results:
                    confusion_matrix_labels[str(result[1].intent_id)] = result[1].intent_label
                ########

                result_list.append((text, true_label_id, predicted_label_ids, text_uuid))

            # Tuple[float, float, Dict[str, Dict[str, int]]]
            accuracy, f1, confusion_matrix = engine_utils.analyse_clsfr_results(result_list)

            return accuracy, f1, confusion_matrix, confusion_matrix_labels
        else:
            return 0.0, 0.0, {}, {}

    def train_intent_clsfr(self, name: str,
                           training_list: List[ExpressionT],
                           testing_list: List[ExpressionT],
                           word_manifold_name_dict: Dict[str, str]) -> bool:
        """ Reset and train the Intent classifier with expression-label pairs.

        Reset and train the intent classifier with expression-label pairs. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of tuples of expressions used to train the model.
        :param testing_list: List of tuples of expressions used to test performance and over fitting during training.
        :param word_manifold_name_dict: Which named instances of WordManifold to use.
        :return: Boolean indicating whether or not the training was successful.
        """
        word_manifold_dict = {}  # type: Dict[str, WordManifold]

        # Convert manifold name dict to a dict of manifold objects.
        for lang_code, manifold_name in word_manifold_name_dict.items():
            language_model = self.get_language_model(manifold_name)

            if (language_model is not None) and (type(language_model) == WordManifold):
                word_manifold_dict[lang_code] = language_model  # type: ignore
            # else:
            #     print("Error:", manifold_name, "is not loaded!")

        if len(word_manifold_dict) > 0:
            intent_clsfr = IntentClassifier(word_manifold_dict)

            success = intent_clsfr.train(training_list, testing_list)

            if success:
                self._intent_clsfr_dict[name] = intent_clsfr
                return True

        return False

    def train_and_cross_validate_intent_clsfr(self, name: str,
                                              training_list: List[ExpressionT],
                                              testing_list: List[ExpressionT],
                                              word_manifold_name_dict: Dict[str, str],
                                              weak_match_threshold: float = 1.0,
                                              k: int = 5,
                                              n_experiments: int = 30) -> \
            Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]], Dict[str, str]]:
        """ Reset and train the Intent classifier with expression-label pairs.

        Reset and train the intent classifier with expression-label pairs. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of tuples of expressions used to train the model.
        :param testing_list: List of tuples of expressions used to test performance and over fitting during training.
        :param word_manifold_name_dict: Which named instances of WordManifold to use.
        :param weak_match_threshold: The weak match threshold to use during cross validation testing.
        :param k: The samples are randomised, then every k'th samples of each class is put in the validation set.
        :param n_experiments: The number of validation experiments.
        :return: The validation accuracy, f1 score, confusion matrix and confusion matrix labels.
        """
        word_manifold_dict = {}  # type: Dict[str, WordManifold]

        # Convert manifold name dict to a dict of manifold objects.
        for lang_code, manifold_name in word_manifold_name_dict.items():
            language_model = self.get_language_model(manifold_name)

            if (language_model is not None) and (type(language_model) == WordManifold):
                word_manifold_dict[lang_code] = language_model  # type: ignore
            # else:
            #     print("Error:", manifold_name, "is not loaded!")

        if len(word_manifold_dict) > 0:
            intent_clsfr = IntentClassifier(word_manifold_dict)

            # =================================================
            # === Do the cross validation training and testing.
            cross_accuracy_sum = 0.0
            cross_f1_sum = 0.0
            cross_confusion_dict = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
            cross_confusion_labels = {}  # type: Dict[str, str]
            cross_count = 0

            for i in range(n_experiments):
                random.shuffle(training_list)

                intent_clsfr_cross_training_list = []  # type: List[ExpressionT]
                intent_clsfr_cross_testing_list = []  # type: List[ExpressionT]

                clsfr_label_counts = {}  # type: Dict[str, int]

                for expression in training_list:
                    label_count = clsfr_label_counts.get(expression.intent_label, 0)
                    clsfr_label_counts[expression.intent_label] = label_count + 1  # Increment the count.

                    if (label_count % k) == 0:
                        intent_clsfr_cross_testing_list.append(expression)
                    else:
                        intent_clsfr_cross_training_list.append(expression)

                success = intent_clsfr.train(intent_clsfr_cross_training_list, [])

                # print(f"    success = {success}")

                if success:
                    self._intent_clsfr_dict[name] = intent_clsfr
                    accuracy, f1, confusion_dict, confusion_labels = \
                        self.test_intent_clsfr(name,
                                               intent_clsfr_cross_testing_list,
                                               weak_match_threshold, 1)

                    # print("Training -", intent_clsfr_cross_training_list)
                    # print("Testing -", intent_clsfr_cross_testing_list)

                    # === Update the cross confusion matrix ===
                    for label_a, dict_b in confusion_dict.items():
                        cross_dict_b = cross_confusion_dict.get(label_a, {})

                        for label_b, samples in dict_b.items():
                            cross_samples = cross_dict_b.get(label_b, [])

                            for sample in samples:
                                if sample not in cross_samples:
                                    cross_samples.append(sample)

                            cross_dict_b[label_b] = cross_samples

                        cross_confusion_dict[label_a] = cross_dict_b
                    # === ===

                    cross_confusion_labels = confusion_labels
                    cross_accuracy_sum += accuracy
                    cross_f1_sum += f1
                    cross_count += 1

                    # print(f"    cross_count = {cross_count}")
                    # print(f"    train(): cross_accuracy = {accuracy}")
                    # print(f"    train(): cross_f1 = {f1}")
                    # print(f"    train(): confusion_dict = {confusion_dict}")
                    # print(f"    train(): confusion_labels = {confusion_labels}")
                    # print(f"    train(): cross_accuracy_avrg = {cross_accuracy_sum / cross_count}")
                    # print(f"    train(): cross_f1_avrg = {cross_f1_sum / cross_count}")
                    # print(f"    train(): cross_confusion_dict = {cross_confusion_dict}")
                    # print(f"    train(): cross_confusion_labels = {cross_confusion_labels}")
                    # print()
            # =================================================

            # Final train cycle with ALL training samples.
            success = intent_clsfr.train(training_list, testing_list)

            if (cross_count > 0) and success:
                self._intent_clsfr_dict[name] = intent_clsfr
                cross_accuracy = cross_accuracy_sum / cross_count
                cross_f1 = cross_f1_sum / cross_count
                return cross_accuracy, cross_f1, cross_confusion_dict, cross_confusion_labels

        return 0.0, 0.0, {}, {}

    def train_intent_clsfr_online(self, name: str,
                                  training_list: List[ExpressionT],
                                  testing_list: List[ExpressionT]) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param name: The instance name.
        :param training_list: The list of training samples List[Tuple[text, label, lang_id]].
        :param testing_list: The list of testing samples List[Tuple[text, label, lang_id]].
        :return: True if training was successful.
        """
        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            return intent_clsfr.train_online(training_list, testing_list)
        else:
            return False

    def get_model_intent_clsfr_expressions(self, name: str) -> Optional[List[ExpressionT]]:
        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            return intent_clsfr.get_model_expressions()
        else:
            return None

    def retrieve_intents(self,
                         name: str,
                         input_text: str, lang_code: Optional[str],
                         weak_match_threshold: float,
                         top_n: int) -> Tuple[List[Tuple[str, int, str, float, str]], Optional[str]]:
        """ Retrieve a list of matching intent expressions.

        :param name: Instance name.
        :param input_text: Expression from user to be matched against intents.
        :param lang_code: A hint for the language code of the input.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number of labels to return.
        :return: List of probable expressions (text, intent_id, intent_label, score, lang_code) sorted from high to low score
        """
        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            retrieved_matches = []  # type: List[Tuple[str, int, str, float, str]]

            nn_matches, lang_code = intent_clsfr.find_knn_matches(input_text, lang_code,
                                                                  weak_match_threshold,
                                                                  top_n)
            # nn_matches = List[ExpressionT]

            # Reformat the result list to not have the expression vector.
            for score, expression in nn_matches:
                retrieved_matches.append((expression.text, expression.intent_id,
                                          expression.intent_label, score, expression.lang_code))

            return retrieved_matches, lang_code
        else:
            return [], None

    def tsne_intent_clsfr(self, name: str,
                          n_components: int, perplexity: float, learning_rate: float) -> \
            Optional[List[Tuple[str, str, float, float, float]]]:

        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            return intent_clsfr.run_tsne(n_components, perplexity, learning_rate)
        else:
            return None

    def get_intent_classifier_word_manifold_dict(self, name: str) -> Optional[Dict[str, WordManifold]]:
        """Returns the associated word manifold instances."""
        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            return intent_clsfr.get_word_manifold_dict()
        else:
            return None

    def get_intent_clsfr_labels(self, name: str) -> Optional[List[str]]:
        intent_clsfr = self._intent_clsfr_dict.get(name)

        if intent_clsfr is not None:
            return intent_clsfr.get_labels()
        else:
            return None

    def save_intent_clsfr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.intent_clsfr_pickle', self._intent_clsfr_dict)

    def load_intent_clsfr(self, name: str,
                          word_manifold_name_dict: Dict[str, str],
                          use_data_folder=False) -> bool:
        model_loaded = engine_utils.load_model(name, use_data_folder, '.intent_clsfr_pickle', self._intent_clsfr_dict)

        if model_loaded:
            # If model loaded then also add the requested language models.
            word_manifold_dict = {}  # type: Dict[str, WordManifold]

            for lang_code, manifold_name in word_manifold_name_dict.items():
                language_model = self.get_language_model(manifold_name)

                if (language_model is not None) and (type(language_model) == WordManifold):
                    word_manifold_dict[lang_code] = language_model  # type: ignore
                else:
                    logging.error(f"nlp_engine.NLPEngine.load_intent_clsfr(): {name} needs word manifold "
                                  f"{manifold_name}, but its not loaded!")

            if len(word_manifold_dict) > 0:
                self._intent_clsfr_dict[name].set_word_manifold_dict(word_manifold_dict)
                return True
            else:
                # None of the languages available so unload model and return failure.
                engine_utils.trash_model(name, trash_cache_only=True,
                                         model_extension='.intent_clsfr_pickle', model_dict=self._intent_clsfr_dict)
                return False
        else:
            return False

    def trash_intent_clsfr(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.intent_clsfr_pickle', self._intent_clsfr_dict)

    def vaporise_intent_clsfr(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.intent_clsfr_pickle', self._intent_clsfr_dict)

    def get_intent_classifier(self, name: str) -> Optional[IntentClassifier]:
        return self._intent_clsfr_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # ==================================================================
    # === CRF Entity ===================================================
    # ==================================================================
    @staticmethod
    def cnvrt_json_to_crf_samples(json_list: List[Dict]) -> List[CRFSample]:
        """
        Convert json samples to CRF samples.

        :param json_list: [{'text': '...', 'entity_list': [{'start': 0, 'end': 1, 'entity': 'object', 'value': 'car'}]
        :return: List of CRF samples.
        """
        return CRFExtractor.cnvrt_json_to_crf_samples(json_list)

    @staticmethod
    def split_crf_expressions(sample_list: List[CRFSample],
                              fraction_training: float) -> Tuple[List[CRFSample], List[CRFSample]]:
        """
        Split a list of CRF samples into a training set and a testing set.

        :param sample_list: The list of samples of all labels.
        :param fraction_training: The fraction of the samples to use as training samples.
        :return: A list of training samples and a list of testing samples.
        """
        shuffled_sample_list = list(sample_list)
        random.shuffle(shuffled_sample_list)

        num_training_samples = round(len(shuffled_sample_list) * fraction_training)

        return shuffled_sample_list[:num_training_samples], shuffled_sample_list[num_training_samples:]

    def test_crf_extr(self, name: str,
                      sample_list: List[CRFSample],
                      weak_match_threshold: float) -> Tuple[float, float,
                                                            Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                                                            Dict[str, str]]:
        """
        Test the crf extractor with the provided test set

        :param name: Instance name.
        :param sample_list: List of CRF Samples.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :return: The crf extractors 'accuracy, f1 score.
        """
        crf_extr = self._crf_extr_dict.get(name)

        if crf_extr is not None and len(sample_list) > 0:
            accuracy_sum = 0.0
            sample_count = 0
            result_list = []  # type: List[Tuple[str, str, List[str], Optional[str]]]

            for sample in sample_list:
                pred_entity_list, pred_lang_code = crf_extr.predict(sample.text, None)
                accuracy_sum += crf_extr.score_prediction(pred_entity_list=pred_entity_list,
                                                          true_entity_list=sample.entity_list,
                                                          text=sample.text)
                sample_count += 1

                # More analysis ...
                for entity in sample.entity_list:
                    entity_value = sample.text[entity.index: (entity.index + entity.len)]

                    # Find the entity amongst the predicted entities.
                    for pred_entity in pred_entity_list:
                        if (entity.entity == pred_entity.entity) and (entity_value == pred_entity.value):
                            # Found!
                            result_list.append((sample.text, entity.entity, [pred_entity.entity], None))
                            break

            # accuracy = accuracy_sum / sample_count
            accuracy, f1, confusion_matrix = engine_utils.analyse_clsfr_results(result_list)

            crf_labels = crf_extr.get_labels()

            if crf_labels is not None:
                confusion_matrix_labels = {label: label for label in crf_labels}
                return accuracy, f1, confusion_matrix, confusion_matrix_labels
            else:
                return 0.0, 0.0, {}, {}
        else:
            return 0.0, 0.0, {}, {}

    def train_crf_extr(self, name: str,
                       training_list: List[CRFSample],
                       testing_list: List[CRFSample]) -> bool:
        """ Reset and train the crf extractor with the crf samples.

        Reset and train the crf extractor with the crf samples. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of samples to train the model.
        :param testing_list: List of samples used to test performance and over fitting during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        crf_extr = CRFExtractor()

        success = crf_extr.train(training_list, testing_list)

        if success:
            self._crf_extr_dict[name] = crf_extr
            return True
        else:
            return False

    def train_and_cross_validate_crf_extr(self, name: str,
                                          training_list: List[ExpressionT],
                                          testing_list: List[ExpressionT],
                                          weak_match_threshold: float = 1.0,
                                          k: int = 5,
                                          n_experiments: int = 30) -> Tuple[float, float]:
        # """ Reset and train the Intent classifier with expression-label pairs.
        #
        # Reset and train the intent classifier with expression-label pairs. Note that the previously loaded or
        # trained named instance is lost!
        #
        # :param name: Instance name.
        # :param training_list: List of tuples of expressions used to train the model.
        # :param testing_list: List of tuples of expressions used to test performance and over fitting during training.
        # :param weak_match_threshold: The weak match threshold to use during cross validation testing.
        # :param k: The samples are randomised, then every k'th samples of each class is put in the validation set.
        # :param n_experiments: The number of validation experiments.
        # :return: The validation accuracy, f1 score.
        # """
        # if ... :
        #     intent_clsfr = IntentClassifier(...)
        #
        #     # =================================================
        #     # === Do the cross validation training and testing.
        #     cross_accuracy_sum = 0.0
        #     cross_f1_sum = 0.0
        #     cross_confusion_dict = {}  # type: Dict[str, Dict[str, List[str]]]
        #     cross_confusion_labels = {}  # type: Dict[str, str]
        #     cross_count = 0
        #
        #     for i in range(n_experiments):
        #         random.shuffle(training_list)
        #
        #         intent_clsfr_cross_training_list = []  # type: List[ExpressionT]
        #         intent_clsfr_cross_testing_list = []  # type: List[ExpressionT]
        #
        #         clsfr_label_counts = {}  # type: Dict[str, int]
        #
        #         for expression in training_list:
        #             label_count = clsfr_label_counts.get(expression.intent_label, 0)
        #             clsfr_label_counts[expression.intent_label] = label_count + 1  # Increment the count.
        #
        #             if (label_count % k) == 0:
        #                 intent_clsfr_cross_testing_list.append(expression)
        #             else:
        #                 intent_clsfr_cross_training_list.append(expression)
        #
        #         success = intent_clsfr.train(intent_clsfr_cross_training_list, [])
        #
        #         # print(f"    success = {success}")
        #
        #         if success:
        #             self._intent_clsfr_dict[name] = intent_clsfr
        #             accuracy, f1, confusion_dict, confusion_labels = \
        #                 self.test_intent_clsfr(name,
        #                                        intent_clsfr_cross_testing_list,
        #                                        weak_match_threshold, 1)
        #
        #             # print("Training -", intent_clsfr_cross_training_list)
        #             # print("Testing -", intent_clsfr_cross_testing_list)
        #
        #             # === Update the cross confusion matrix ===
        #             for label_a, dict_b in confusion_dict.items():
        #                 cross_dict_b = cross_confusion_dict.get(label_a, {})
        #
        #                 for label_b, samples in dict_b.items():
        #                     cross_samples = cross_dict_b.get(label_b, [])
        #
        #                     for sample in samples:
        #                         if sample not in cross_samples:
        #                             cross_samples.append(sample)
        #
        #                     cross_dict_b[label_b] = cross_samples
        #
        #                 cross_confusion_dict[label_a] = cross_dict_b
        #             # === ===
        #
        #             cross_confusion_labels = confusion_labels
        #             cross_accuracy_sum += accuracy
        #             cross_f1_sum += f1
        #             cross_count += 1
        #
        #             # print(f"    cross_count = {cross_count}")
        #             # print(f"    train(): cross_accuracy = {accuracy}")
        #             # print(f"    train(): cross_f1 = {f1}")
        #             # print(f"    train(): confusion_dict = {confusion_dict}")
        #             # print(f"    train(): confusion_labels = {confusion_labels}")
        #             # print(f"    train(): cross_accuracy_avrg = {cross_accuracy_sum / cross_count}")
        #             # print(f"    train(): cross_f1_avrg = {cross_f1_sum / cross_count}")
        #             # print(f"    train(): cross_confusion_dict = {cross_confusion_dict}")
        #             # print(f"    train(): cross_confusion_labels = {cross_confusion_labels}")
        #             # print()
        #     # =================================================
        #
        #     # Final train cycle with ALL training samples.
        #     success = intent_clsfr.train(training_list, testing_list)
        #
        #     if (cross_count > 0) and success:
        #         self._intent_clsfr_dict[name] = intent_clsfr
        #         cross_accuracy = cross_accuracy_sum / cross_count
        #         cross_f1 = cross_f1_sum / cross_count
        #         return cross_accuracy, cross_f1, cross_confusion_dict, cross_confusion_labels

        # ToDo: Figure out how to do cross-validation testing on entities.
        return 0.0, 0.0

    def retrieve_crf_entities(self,
                              name: str,
                              input_text: str, lang_code: Optional[str],
                              weak_match_threshold: float) -> Tuple[List[Dict], Optional[str]]:
        """ Tag the words in the sentence with entity labels.

        :param name: Instance name.
        :param input_text: Utterance with entities to be extracted.
        :param lang_code: A hint for the language code of the input.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :return: List of extracted entities i.e. [{"entity": "location", "index": 31, "len": 8}, ...]
        """
        crf_extr = self._crf_extr_dict.get(name)

        if crf_extr is not None:
            extracted_entities, lang_code = crf_extr.predict(input_text, lang_code)

            extracted_entities_json = []  # type: List[Dict]

            for entity in extracted_entities:
                extracted_entities_json.append({"entity": entity.entity,
                                                "value": entity.value,
                                                "index": entity.index,
                                                "len": entity.len})

            return extracted_entities_json, lang_code
        else:
            return [], None

    def get_crf_extr_labels(self, name: str) -> Optional[List[str]]:
        crf_extr = self._crf_extr_dict.get(name)

        if crf_extr is not None:
            return crf_extr.get_labels()
        else:
            return None

    def save_crf_extr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.crf_extr_pickle', self._crf_extr_dict)

    def load_crf_extr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.load_model(name, use_data_folder, '.crf_extr_pickle', self._crf_extr_dict)

    def trash_crf_extr(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.crf_extr_pickle', self._crf_extr_dict)

    def vaporise_crf_extr(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.crf_extr_pickle', self._crf_extr_dict)

    def get_crf_extr(self, name: str) -> Optional[CRFExtractor]:
        return self._crf_extr_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # ==================================================================
    # === Synonym Entity ===================================================
    # ==================================================================
    @staticmethod
    def cnvrt_json_to_synonym_samples(json_list: List[Dict]) -> List[SynonymSample]:
        """
        Convert json samples to Synonym samples.

        :param json_list: [{'text': '...', 'entity_list': [{'start': 0, 'end': 1, 'entity': 'object', 'value': 'car'}]
        :return: List of Synonym samples.
        """
        return SynonymExtractor.cnvrt_json_to_synonym_samples(json_list)

    @staticmethod
    def split_synonym_expressions(sample_list: List[SynonymSample],
                                  fraction_training: float) -> Tuple[List[SynonymSample], List[SynonymSample]]:
        """
        Split a list of synonym samples into a training set and a testing set.

        :param sample_list: The list of samples of all labels.
        :param fraction_training: The fraction of the samples to use as training samples.
        :return: A list of training samples and a list of testing samples.
        """
        shuffled_sample_list = list(sample_list)
        random.shuffle(shuffled_sample_list)

        num_training_samples = round(len(shuffled_sample_list) * fraction_training)

        return shuffled_sample_list[:num_training_samples], shuffled_sample_list[num_training_samples:]

    def test_synonym_extr(self, name: str,
                          testing_list: List[SynonymSample],
                          weak_match_threshold: float) -> Tuple[float, float]:
        """
        Test the synonym extractor with the provided test set

        :param name: Instance name.
        :param testing_list: List of Synonym Samples.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :return: The synonym extractors 'accuracy, f1 score.
        """
        synonym_extr = self._synonym_extr_dict.get(name)

        if synonym_extr is not None and len(testing_list) > 0:
            for sample in testing_list:
                # print("sample =", sample)

                # truth = sample.entity_list
                # prediction, lang_code = synonym_extr.predict(sample.text, None)

                # ToDo: Figure out how to do testing on entities.
                pass

            return 0.0, 0.0
        else:
            return 0.0, 0.0

    def train_synonym_extr(self, name: str,
                           training_list: List[SynonymSample],
                           testing_list: List[SynonymSample]) -> bool:
        """ Reset and train the synonym extractor with the synonym samples.

        Reset and train the synonym extractor with the synonym samples. Note that the previously loaded or
        trained named instance is lost!

        :param name: Instance name.
        :param training_list: List of samples to train the model.
        :param testing_list: List of samples used to test performance and over fitting during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        synonym_extr = SynonymExtractor()

        success = synonym_extr.train(training_list, testing_list)

        if success:
            self._synonym_extr_dict[name] = synonym_extr
            return True
        else:
            return False

    def train_and_cross_validate_synonym_extr(self, name: str,
                                              training_list: List[ExpressionT],
                                              testing_list: List[ExpressionT],
                                              weak_match_threshold: float = 1.0,
                                              k: int = 5,
                                              n_experiments: int = 30) -> Tuple[float, float]:

        # ToDo: Figure out how to do cross-validation testing on entities.
        return 0.0, 0.0

    def retrieve_synonym_entities(self,
                                  name: str,
                                  input_text: str, lang_code: Optional[str],
                                  weak_match_threshold: float) -> Tuple[List[Dict], Optional[str]]:
        """ Tag the words in the sentence with entity labels.

        :param name: Instance name.
        :param input_text: Utterance with entities to be extracted.
        :param lang_code: A hint for the language code of the input.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :return: List of extracted entities i.e. [{"entity": "location", "index": 31, "len": 8}, ...]
        """
        synonym_extr = self._synonym_extr_dict.get(name)

        if synonym_extr is not None:
            extracted_entities, lang_code = synonym_extr.predict(input_text, lang_code)

            extracted_entities_json = []  # type: List[Dict]

            for entity in extracted_entities:
                extracted_entities_json.append({"entity": entity.entity,
                                                "value": entity.value,
                                                "index": entity.index,
                                                "len": entity.len})

            return extracted_entities_json, lang_code
        else:
            return [], None

    def get_synonym_extr_labels(self, name: str) -> Optional[List[str]]:
        synonym_extr = self._synonym_extr_dict.get(name)

        if synonym_extr is not None:
            return synonym_extr.get_labels()
        else:
            return None

    def save_synonym_extr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.save_model(name, use_data_folder, '.synonym_extr_pickle', self._synonym_extr_dict)

    def load_synonym_extr(self, name: str, use_data_folder=False) -> bool:
        return engine_utils.load_model(name, use_data_folder, '.synonym_extr_pickle', self._synonym_extr_dict)

    def trash_synonym_extr(self, name: str, trash_cache_only: bool = False) -> bool:
        return engine_utils.trash_model(name, trash_cache_only, '.synonym_extr_pickle', self._synonym_extr_dict)

    def vaporise_synonym_extr(self, name: str) -> bool:
        return engine_utils.vaporise_model(name, '.synonym_extr_pickle', self._synonym_extr_dict)

    def get_synonym_extr(self, name: str) -> Optional[SynonymExtractor]:
        return self._synonym_extr_dict.get(name)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Retrieve/Parse date =================================================
    # =========================================================================
    @staticmethod
    def _format_dcklng_datetime(dttext: str) -> str:
        """Format the duckling date_time string from iso 8601 format to something more pretty."""
        return dttext[:10] + ' ' + dttext[11:19]

    @staticmethod
    def _grain_to_days(grain: str) -> float:
        """Convert the grain string to the floating point number of days it represents."""
        if grain == 'second':
            return 1.0 / (24.0 * 60.0 * 60.0)
        if grain == 'minute':
            return 1.0 / (24.0 * 60.0)
        if grain == 'hour':
            return 1.0 / 24.0
        if grain == 'day':
            return 1.0
        if grain == 'week':
            return 7.0
        if grain == 'month':
            return 30.44
        if grain == 'year':
            return 365.24
        raise Exception('Unknown time grain!')
        # return 0.0

    def retrieve_date(self, input_text: str, context: str) -> List[Tuple[str, str]]:
        """ Retrieve a date from the text.

        :param input_text: Document/Sentence to classify.
        :param context: Some background/prior text to the query that might be useful.
                        * Values 'past'/'future' selects whether ambiguous dates are resolved into the future or into
                        the past.
        :return: List of probable date values with the time 'grain' that represent uncertainty in the date&time value.
        """

        retrieved_date_list = []
        retrieved_date_list_cleaned = []

        if self._use_duckling is False:
            prefer_dates_list = []
            if context == 'past' or context == 'current' or context == 'future':
                prefer_dates_list.append(context)
            else:
                prefer_dates_list.append('future')
                prefer_dates_list.append('current')
                prefer_dates_list.append('past')

            for preferred_date in prefer_dates_list:
                # === DMY date ===
                datep_dmy = dateparser.date.DateDataParser(settings={'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'last',
                                                                     'PREFER_DATES_FROM': preferred_date})
                # languages=['en', 'pt', 'es'])

                datep_dmy_data = datep_dmy.get_date_data(input_text)

                if datep_dmy_data['date_obj']:
                    dp_str = str(datep_dmy_data['date_obj'])

                    if datep_dmy_data['period'] == 'day':
                        # Attempt to guess a grain finer than a day.
                        if dp_str[11:13] != '00':
                            datep_dmy_data['period'] = 'hour'
                        if dp_str[14:16] != '00':
                            datep_dmy_data['period'] = 'minute'
                        if dp_str[17:19] != '00':
                            datep_dmy_data['period'] = 'second'

                    retrieved_date_list.append((dp_str, datep_dmy_data['period']))

                # === YMD date - see above ===
                datep_ymd = dateparser.date.DateDataParser(settings={'DATE_ORDER': 'YMD', 'PREFER_DAY_OF_MONTH': 'last',
                                                                     'PREFER_DATES_FROM': preferred_date})
                # languages=['en', 'pt', 'es'])

                datep_ymd_data = datep_ymd.get_date_data(input_text)

                if datep_ymd_data['date_obj']:
                    dp_str = str(datep_ymd_data['date_obj'])

                    if datep_ymd_data['period'] == 'day':
                        # Attempt to guess a grain finer than a day.
                        if dp_str[11:13] != '00':
                            datep_ymd_data['period'] = 'hour'
                        if dp_str[14:16] != '00':
                            datep_ymd_data['period'] = 'minute'
                        if dp_str[17:19] != '00':
                            datep_ymd_data['period'] = 'second'

                    retrieved_date_list.append((dp_str, datep_ymd_data['period']))
        else:
            entity_list = self.retrieve_duckling_entities(input_text=input_text,
                                                          context="",
                                                          reference_time=None)

            for entity in entity_list:
                if entity['dim'] == 'time':
                    retrieved_date_list.append(
                        (NLPEngine._format_dcklng_datetime(entity['value']), entity['grain']))

        # Cleanup the list of dates...
        # Prefer smaller granularity entries where dates and times match and remove exact duplicates.
        for index_a, date_a in enumerate(retrieved_date_list):
            a_is_best = True

            for date_b in retrieved_date_list[index_a + 1:]:
                if date_b[0] == date_a[0] and \
                        (NLPEngine._grain_to_days(date_b[1]) <= NLPEngine._grain_to_days(date_a[1])):
                    a_is_best = False
                    break

            if a_is_best:
                retrieved_date_list_cleaned.append(date_a)

        retrieved_date_list_cleaned.sort(key=lambda date_item: date_item[0], reverse=False)

        return retrieved_date_list_cleaned

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Duckling Entities ===================================================
    # =========================================================================
    @staticmethod
    def duckling_strip_timezone(input: str):
        return input[:min(len(input), 23)]

    def retrieve_duckling_entities(self, input_text: str,
                                   context: str,
                                   reference_time: Optional[str]) -> List[Dict]:
        """ Retrieve duckling entities from the text.

        :param input_text: Document/Sentence to classify.
        :param context: Some background/prior text to the query that might be useful.
        :param reference_time: The parser's reference time. If empty string then reference time is the current time.
        :return: List of entity dicts.
        """
        entity_list = []  # type: List[Dict]

        if self._use_duckling is True:
            try:
                parse_list = []  # type: List[Union[Dict]]

                try:
                    # "text", "lang", "dims", "tz", "locale", "reftime", "latent"
                    data = {'text': input_text + " " + context,
                            'locale': 'en_GB',
                            'lang': 'EN'}

                    # if reference_time is not None:
                    #     data['reftime'] = reference_time

                    response = requests.post(self._duckling_url + '/parse',
                                             data=data, timeout=2.0,
                                             auth=HTTPBasicAuth('duckling', 'kWEn64Mqhg6mpDTv'))

                    if response.status_code != 200:
                        logging.error(f"NLPEngine.retrieve_duckling_entities: response.status_code={response.status_code}!")

                    parse_list = response.json()

                except requests.Timeout as e:
                    logging.error(f"NLPEngine.retrieve_duckling_entities: requests.Timeout {e}!")
                except requests.RequestException as e:
                    logging.error(f"NLPEngine.retrieve_duckling_entities: requests.RequestException {e}!")

                # parse_list = self._dcklng.parse(input_text + " " + context,
                #                                 language=Language.ENGLISH,
                #                                 reference_time=dcklng_ref_time)

                ###########################
                # # duckling number
                # {'end': 1,
                #  'start': 0,
                #  'dim': 'number',
                #  'value': {'type': 'value', 'value': 6.0},
                #  'body': '6 eggs'}
                #
                # # feersum number
                # {
                #     'dim': 'number',
                #     'body': '6', 'type':
                #     'value', 'value': 6.0
                # }
                #
                ###########################
                # # duckling duration
                # {'end': 8,
                #  'dim': 'duration',
                #  'value': {'normalized': {'value': 15897600.0, 'unit': 'second'},
                #            'value': 6.0,
                #            'unit': 'month',
                #            'month': 6},
                #  'body': '6 months',
                #  'start': 0}
                #
                # # feersum_duration
                # {
                #     'dim': 'duration',
                #     'body': '6 months',
                #     'type': None,
                #     'value': 6.0,
                #     'unit': 'month'
                # }
                #
                #
                ###########################
                # # duckling distance
                # {'end': 1,
                #  'dim': 'distance',
                #  'latent': True,
                #  'body': '6',
                #  'start': 0,
                #  'value': {'type': 'value', 'value': 6.0}}
                #
                # # feersum distance
                # {
                #     'dim': 'distance',
                #     'body': '6 km',
                #     'type': 'value',
                #     'value': 6.0,
                #     'unit': 'kilometre'
                # }
                #
                #
                ###########################
                # # duckling volume
                # {'end': 1,
                #  'dim': 'volume',
                #  'latent': True,
                #  'body': '6',
                #  'start': 0,
                #  'value': {'type': 'value', 'value': 6.0}}
                #
                # # feersum volume
                # {
                #     'dim': 'volume',
                #     'body': '6 litres',
                #     'type': 'value',
                #     'value': 6.0,
                #     'unit': 'litre'
                # }
                #
                #
                ###########################
                # # duckling temperature
                # {'end': 1,
                #  'dim': 'temperature',
                #  'latent': True,
                #  'body': '6',
                #  'start': 0,
                #  'value': {'type': 'value', 'value': 6.0}}
                #
                # # feersum temperature
                # {
                #     'dim': 'temperature',
                #     'body': '6 degrees celcius.',
                #     'type': 'value',
                #     'value': 6.0,
                #     'unit': 'celsius'
                # }
                #
                #

                ###########################
                # # duckling time value
                # {
                #     'dim': 'time',
                #     'body': 'The day after tomorrow',
                #     'value':
                #         {
                #             'type': 'value',
                #             'value': '2019-04-27T00:00:00.000+02:00',
                #             'grain': 'day',
                #             'values': [{'type': 'value', 'value': '2019-04-27T00:00:00.000+02:00', 'grain': 'day'}]
                #          },
                #     'start': 0,
                #     'end': 22
                # }
                #
                # # feersum time value
                # {
                #     'dim': 'time',
                #     'body': 'The day after tomorrow',
                #     'type': 'value',
                #     'value': '2019-04-27T00:00:00.000+02:00',
                #     'grain': 'day'
                # }
                #
                #
                ###########################
                # # duckling time interval
                # {
                #     'dim': 'time',
                #     'body': 'on tomorrow between 6pm and 11:00 pm',
                #     'value':
                #         {
                #             'type': 'interval',
                #             'from': {'value': '2019-04-26T18:00:00.000+02:00', 'grain': 'minute'},
                #             'to': {'value': '2019-04-26T23:01:00.000+02:00', 'grain': 'minute'},
                #             'values':
                #                 [
                #                     {
                #                         'type': 'interval',
                #                         'from': {'value': '2019-04-26T18:00:00.000+02:00', 'grain': 'minute'},
                #                         'to': {'value': '2019-04-26T23:01:00.000+02:00', 'grain': 'minute'}
                #                     }
                #                 ]
                #         },
                #     'start': 17,
                #     'end': 53
                # }
                #
                # # feersum time interval
                # {
                #     'dim': 'time',
                #     'body': 'on tomorrow between 6pm and 11:00 pm',
                #     'type': 'interval',
                #     'value': '2019-04-26T18:00:00.000+02:00',
                #     'grain': 'minute',
                #     'from_value': '2019-04-26T18:00:00.000+02:00',
                #     'from_grain': 'minute',
                #     'to_value': '2019-04-26T23:01:00.000+02:00',
                #     'to_grain': 'minute'
                # }
                #

                for new_entity in parse_list:
                    new_entity_good = True

                    # The updated list of entities - keeps the entities better than new_entity and also new_entity if
                    # no other ones better than new_entity.
                    good_entity_list = []  # type: List[Dict]

                    # Check to see if an entity overlapping new_entity already exists.
                    # The longest of the overlapping entities are assumed to be the best one to use!
                    for i, entity in enumerate(entity_list):
                        if new_entity['start'] < entity['end'] and new_entity['end'] > entity['start']:
                            # === existing entity DOES overlap with new one.
                            new_entity_length = new_entity['end'] - new_entity['start']
                            entity_length = entity['end'] - entity['start']

                            if entity_length >= new_entity_length:
                                # existing entity probably better than new one.
                                good_entity_list.append(entity)
                                new_entity_good = False
                        else:
                            # === existing entity DOES NOT overlap with new one.
                            good_entity_list.append(entity)

                    if new_entity_good:
                        good_entity_list.append(dict(new_entity))

                    entity_list = good_entity_list

                # Modify the entities to be a bit easier to use.
                for i, entity in enumerate(entity_list):
                    # print("Duckling entity =", entity)

                    feersum_entity = {'dim': entity['dim'],
                                      'body': entity['body']}

                    value_dict = entity['value']
                    feersum_entity['type'] = value_dict.get('type')

                    if entity.get('dim') == 'time':
                        if value_dict.get('type') == 'interval':
                            from_dict = value_dict.get('from')
                            to_dict = value_dict.get('to')

                            # Add fallback value, grain and unit info.
                            if from_dict is not None:
                                feersum_entity['value'] = self.duckling_strip_timezone(from_dict['value'])
                                if from_dict.get('unit'):
                                    feersum_entity['unit'] = from_dict['unit']
                                if from_dict.get('grain'):
                                    feersum_entity['grain'] = from_dict['grain']
                            elif to_dict is not None:
                                feersum_entity['value'] = self.duckling_strip_timezone(to_dict['value'])
                                if to_dict.get('unit'):
                                    feersum_entity['unit'] = to_dict['unit']
                                if to_dict.get('grain'):
                                    feersum_entity['grain'] = to_dict['grain']

                            # Add from value, grain and unit info if available.
                            if from_dict is not None:
                                feersum_entity['from_value'] = self.duckling_strip_timezone(from_dict['value'])
                                if from_dict.get('unit'):
                                    feersum_entity['from_unit'] = from_dict['unit']
                                if from_dict.get('grain'):
                                    feersum_entity['from_grain'] = from_dict['grain']

                            # Add to value, grain and unit info if available.
                            if to_dict is not None:
                                feersum_entity['to_value'] = self.duckling_strip_timezone(to_dict['value'])
                                if to_dict.get('unit'):
                                    feersum_entity['to_unit'] = to_dict['unit']
                                if to_dict.get('grain'):
                                    feersum_entity['to_grain'] = to_dict['grain']
                        elif value_dict.get('type') == 'value':
                            feersum_entity['value'] = self.duckling_strip_timezone(value_dict['value'])
                            if value_dict.get('unit'):
                                feersum_entity['unit'] = value_dict['unit']
                            if value_dict.get('grain'):
                                feersum_entity['grain'] = value_dict['grain']
                    elif entity.get('dim') == 'duration':
                        feersum_entity['value'] = self.duckling_strip_timezone(value_dict['value'])
                        if value_dict.get('unit'):
                            feersum_entity['unit'] = value_dict['unit']
                        if value_dict.get('grain'):
                            feersum_entity['grain'] = value_dict['grain']
                    else:  # Handle all the other general cases that have a value and unit.
                        feersum_entity['value'] = self.duckling_strip_timezone(value_dict['value'])
                        if value_dict.get('unit'):
                            feersum_entity['unit'] = value_dict['unit']

                    entity_list[i] = dict(feersum_entity)

                    # print("Feersum entity =", feersum_entity)
                    # print()
            except ValueError:
                # print("NLPEngine.retrieve_duckling_entities ValueError! PROBABLY due to the reference time format!")
                pass

        return entity_list

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === RegEx Entities ======================================================
    # =========================================================================
    @staticmethod
    def retrieve_regex_entities(input_text: str,
                                regex_pattern: str,
                                context: str) -> List[Dict]:
        """ Retrieve regex entities from the text. See http://www.regexpal.com

        :param input_text: Document/Sentence to classify.
        :param regex_pattern: The regular expression to use to extract entities
               i.e. r"(?P<license>[A-Z]{3}[ ]?[0-9]{3}[ ]?(GP|NW|MP))"
        :param context: Some background/prior text to the query that might be useful.
        :return: List of entity dicts.
        """
        entity_list = []  # type: List[Dict]

        match_iter = re.finditer(regex_pattern,
                                 input_text,
                                 flags=re.IGNORECASE)

        for match in match_iter:
            entity = {}

            # Add key,value pairs that of non None values!
            for key, value in match.groupdict().items():
                if value is not None:
                    entity[key] = value

            entity["_all_groups"] = match.group(0)

            entity_list.append(entity)

        return entity_list

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Similar Entities ======================================================
    # =========================================================================
    def retrieve_similar_entities(self, input_text: str,
                                  input_entities: Set[str],
                                  threshold: float,
                                  word_manifold_name: str,
                                  spell_correct: bool,
                                  context: str) -> List[Dict]:
        """ Retrieve entities from the text similar to input_entities.

        :param input_text: Document/Sentence to classify.
        :param input_entities: The set of words to test against.
        :param threshold: The similarity threshold.
        :param word_manifold_name: The word manifold instance to use.
        :param spell_correct: Whether or not to spell correct the input text.
        :param context: Some background/prior text to the query that might be useful.
        :return: List of entity dicts.
        """
        entity_list = []  # type: List[Dict]

        input_text_lower = input_text.lower()

        # 1) Find exact 'input_entity in input_text' type matches - supports multi-word entities like person names.
        for input_entity in input_entities:
            input_entity_lower = input_entity.lower()

            # Find if word in input text starts with input_entity OR if the input text perhaps starts with the input entity.
            if str(" " + input_entity_lower) in input_text_lower or input_text_lower.startswith(input_entity_lower):
                entity_list.append({"entity": input_entity_lower, "similarity": 1.0})

        language_model = self.get_language_model(word_manifold_name)

        # 2) Find words in the input text that is similar to those in the input entities -  DOESN'T support multi-words ents!
        if (language_model is not None) and (type(language_model) == WordManifold):
            input_tokens = language_model.tokenize(input_text)

            for input_token in input_tokens:
                already_extracted = False

                # See if input token is a duplicate of an earlier extracted token.
                for entity in entity_list:
                    if entity.get('entity') == input_token.lower():
                        already_extracted = True
                        break

                if already_extracted:
                    continue  # This token is already in entity_list so continue to next input token.

                if spell_correct:
                    input_token = language_model.spell_correct_word(input_token)

                if input_token is not None:
                    # Find the closest dist between this input_token and all input_entities.
                    best_sim = None

                    for input_entity in input_entities:
                        input_sim = language_model.calc_word_similarity(input_token, input_entity)

                        if input_sim > threshold:
                            if best_sim is None or input_sim > best_sim:
                                best_sim = input_sim

                    if best_sim is not None:
                        entity_list.append({"entity": input_token.lower(), "similarity": best_sim})

                        # entity_list.sort(key=lambda matched_entity: matched_entity["similarity"], reverse=True)

        return entity_list

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Person name Entities ================================================
    # =========================================================================
    def retrieve_person_name_entities(self, input_text: str) -> List[str]:
        """ Retrieve any person names in the input text.

        :param input_text: users response to "what is your name ?"
        :return: name
        """
        name = PersonNameExtractor(input_text).retrieve_person_name_entities()

        # print(input_text)
        # print(name)

        if name is not None:
            return [name]
        else:
            return []

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Sentiment analyser ==================================================
    # =========================================================================
    def retrieve_sentiment(self,
                           input_text: str,
                           lang_code: Optional[str]) -> \
            Tuple[float, Optional[List[Dict[str, Union[float, int]]]]]:
        """ Retrieve the global sentiment of the input text.

        :param input_text: Document/Sentence to analyse.
        :param lang_code: A hint for the language code of the input.
        :return: The sentiment value between -1(negative sentiment) and +1(positive sentiment) as well as an optional list
        of sentiment dicts for parts of the input text i.e. [{value, index, len}].
        """
        return self._sentiment_analyzer.get_vader_sentiment(input_text)

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Emotion analyser ==================================================
    # =========================================================================
    def retrieve_emotion(self,
                         input_text: str,
                         lang_code: Optional[str]) -> Tuple[List[Tuple[str, float]], Optional[str]]:
        """ Retrieve the global emotion of the input text.

        :param input_text: Document/Sentence to analyse.
        :param lang_code: A hint for the language code of the input.
        :return: A probability sorted list of emotion classes.
        """
        results = self._emotion_analyser.classify(input_text)
        # print('**', results)
        return results, lang_code

    # =========================================================================
    # =========================================================================
    # =========================================================================

    # =========================================================================
    # === Language recognition from text/dialog ===============================
    # =========================================================================
    @staticmethod
    def get_lid_labels(name: str) -> Optional[List[str]]:
        return lid.get_labels()

    @staticmethod
    def retrieve_language(name: str,
                          input_text: str) -> List[Tuple[str, float]]:  # (lang_code, score)
        """ Retrieve the language the input text is written in.

        :param name: The LID model name.
        :param input_text: Document/Sentence to analyse.
        :return: A list of probable ISO-639-1 language codes sorted from high to low probability.
        """
        result_list = []  # type: List[Tuple[str, float]]

        if input_text is not None and len(input_text) > 0:
            # Just one pre-trained model supported at the moment.
            result_list = lid.lang_ident_nbayes(input_text=input_text)

        return result_list

    @staticmethod
    def retrieve_language_hlt(input_text: str) -> List[Tuple[str, float]]:  # (lang_code, score)
        """ Retrieve the language the input text is written in. Call out to HLT's lang ID.

        :param input_text: Document/Sentence to analyse.
        :return: A list of probable ISO-639-1 language codes sorted from high to low probability.
        """
        result_list = []  # type: List[Tuple[str, float]]

        if input_text is not None and len(input_text) > 0:
            # print("urllib.parse.quote", urllib_parse.quote(input_text))

            hlt_to_iso_map = {"hausa": "hau",
                              "afrikaans": "afr",
                              "english": "eng",
                              "isindebele": "nbl",
                              "isixhosa": "xho",
                              "isizulu": "zul",
                              "sepedi": "nso",
                              "sesotho": "sot",
                              "setswana": "tsn",
                              "siswati": "ssw",
                              "tshivenda": "ven",
                              "xitsonga": "tso"}

            try:
                r = requests.get("http://hlt.meraka.csir.co.za/cgi-bin/lid/lid.cgi?%27" +
                                 urllib_parse.quote(input_text) + "%27",
                                 timeout=0.2)

                iso_lang_code = hlt_to_iso_map.get(r.content.decode('utf-8').strip().lower())

                if iso_lang_code is None:
                    iso_lang_code = "eng"

                result_list.append((iso_lang_code, 1.0))
            except requests.exceptions.RequestException:
                pass

        return result_list
    # =========================================================================
    # =========================================================================
    # =========================================================================
