"""
    FeersumNLU Text Classifier: Nearest Neighbour search with L1 distance.
"""

import logging

from typing import Dict, Tuple, List, Set, NamedTuple, Optional, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.sentence_encoder_base import SentenceEncoderBase
from feersum_nlu.models import text_classifier_base

import numpy as np
import math
import sklearn.manifold as sklearn_manifold
from feersum_nlu.models.lid import lang_ident_nbayes

# === The expression type. sent_vec and lang_code are filled in during training!
# Python 3.5
_ExpressionT = NamedTuple('_ExpressionT',
                          [('text', str),
                           ('sent_vect', np.array),
                           ('label', str),
                           ('lang_code', str)])


# Python 3.6
# class _ExpressionT(NamedTuple):
#     text: str
#     label_id: int
#     sent_vect: np.array
#     label: str
# ===


def _classify_text_language(input_text: str, language_model_dict) -> str:
    """
    Pick the best scoring language from feersum_nlu.models.lid.lang_ident_nbayes(...)!

    Pick the best scoring language from feersum_nlu.models.lid.lang_ident_nbayes(...)! Child classes may specialise
    or override this method as required!

    :param input_text: The text to be classified by language.
    :return: The most likely language of the input_text.
    """

    result_list = lang_ident_nbayes(input_text)  # return a list of Tuple[lang_code, score]; sorted in descending score.

    # Pick the best scoring language from the ones that this model expects!
    if result_list is not None:
        for lang, score in result_list:
            if lang in language_model_dict:
                return lang

    return ""  # language not classified!


class TextClassifierNearestNeighbourL1(text_classifier_base.TextClassifierBase):
    """
    FeersumNLU Classifier: Nearest Neighbour search with L1 distance.
    """

    def __init__(self, language_model_dict: Optional[Dict[str, SentenceEncoderBase]]) -> None:
        super().__init__(language_model_dict=language_model_dict)
        self._next_label_idx = 0

        self._expressions = []  # type: List[_ExpressionT]

    def __getstate__(self):
        """Do not pickle the _language_model_dict with this object!"""
        # ToDo call base class' __getstate__
        state = self.__dict__.copy()
        del state['_language_model_dict']
        return state

    def __setstate__(self, state):
        """_language_model_dict not pickled with the object!"""
        # ToDo call base class' __setstate__
        self.__dict__.update(state)
        self._language_model_dict = None

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

        # ToDo: Batch the training samples by language and submit batches to the sentence encoder to improve performance
        if self._language_model_dict is None:
            logging.error("text_classifier_nn_l1.train_online - _language_model_dict is None!")
            return False

        # Train the model - Calculate the FAQ question vectors just once here.
        for training_sample in training_list:
            if len(self._language_model_dict) == 1:
                # Override the text language code if only one language model is present.
                lang_code = next(iter(self._language_model_dict))
            elif training_sample[2] == "":
                # Fill in the text language code if not supplied.
                lang_code = _classify_text_language(training_sample[0], self._language_model_dict)
            else:
                # Use the supplied language code. (*1)
                lang_code = training_sample[2]

            lang_model = self._language_model_dict.get(lang_code)

            # ToDo: A supplied (*1) lang_code that is not included in the model's lang dict will result in lang_model = None.
            #  Should this event be just logged OR should it be flagged back to user?
            if lang_model is not None:
                spell_correct = lang_code in {"eng", "afr"}

                text = training_sample[0]
                label = training_sample[1]

                # The model is trained by updating _expressions list. The list is the model!
                self._expressions.append(_ExpressionT(text,
                                                      lang_model.calc_sentence_vector(text, spell_correct),
                                                      label,
                                                      lang_code))

                # === Update the _labels set and the _label_to_idx mapping ===
                self._labels.add(label)
                if self._label_to_idx.get(label) is None:
                    self._label_to_idx[label] = self._next_label_idx
                    self._next_label_idx += 1

        return True

    def train(self,
              training_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]],
              testing_list: Union[List[Tuple[str, str, str]], List[Tuple[str, str, str, str]]]) -> bool:
        """
        Reset and train the classifier with expression-label pairs

        :param training_list: List of labelled samples (text, label, lang_code).
        :param testing_list: List of labelled samples (text, label, lang_code) to test accuracy & overfit during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._label_to_idx.clear()
        self._next_label_idx = 0
        self._labels.clear()

        self._expressions.clear()

        return self.train_online(training_list, testing_list, True)

    def classify(self, input_text: str, lang_code_hint: Optional[str],
                 weak_match_threshold: float,
                 top_n: int) -> Tuple[List[Tuple[str, float]], str]:
        """ Find the n best matches to the input text.

        :param input_text: The expression to look for in the expression set.
        :param lang_code_hint: A hint for the language of the input text.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return. At least one result is returned!
        :return: Sorted list of scored labels [(str, float)] plus the lang_code of the input text.
        """
        if self._language_model_dict is None:
            logging.error("text_classifier_nn_l1.classify - _language_model_dict is None!")
            return [], ""

        if len(self._language_model_dict) == 1:
            # Override the text language code if only one language model is present.
            input_lang_code = next(iter(self._language_model_dict))
        elif lang_code_hint is not None:
            input_lang_code = lang_code_hint
        else:
            # Fill in the text language code.
            input_lang_code = _classify_text_language(input_text, self._language_model_dict)

        lang_model = self._language_model_dict.get(input_lang_code)

        if lang_model is None:
            logging.error("text_classifier_nn_l1.classify - language model not found.")
            return [], input_lang_code

        spell_correct = input_lang_code in {"eng", "afr"}

        input_vect = lang_model.calc_sentence_vector(input_text, spell_correct)

        # 1) Calc softmax scores over ALL training utterances.
        # ToDo: Consider using hierarchical or fast_approx softmax if large model performance becomes a problem.
        softmax_temp = (1.0 / 250.0) * lang_model.get_vect_dim()  # ToDo: Set this as a model hyper param.
        scored_utterances = []  # type: List[Tuple[str, float]]
        best_match_probs = []  # type: List[Tuple[str, float]]
        # ToDo: Use more efficient KNN search data structure if many questions used in model!
        #   OR: Use locality sensitive hashing instead!!
        for expression in self._expressions:
            if (input_lang_code == expression.lang_code) and input_vect.any():
                dist = SentenceEncoderBase.calc_l1_dist(input_vect, expression.sent_vect)
                score = math.exp(-1.0 * dist / softmax_temp)
                scored_utterances.append((expression.label, score))

        num_scored_utterances = len(scored_utterances)

        if num_scored_utterances > 0:
            # 2) Find best matching scored labels.
            scored_utterances.sort(key=lambda scored_utterance: scored_utterance[1], reverse=True)
            best_match_label_set = set()  # type: Set[str]
            best_match_scores = []  # type: List[Tuple[str, float]]

            i = 0
            while i < num_scored_utterances:
                label, score = scored_utterances[i]

                if label not in best_match_label_set:
                    best_match_label_set.add(label)
                    best_match_scores.append((label, score))

                i += 1

            softmax_sum = 0.0

            for label, score in best_match_scores:
                softmax_sum += score

            # Note on softmax_temp:
            #  If softmax_sum is zero then none of the training samples were close enough to the input text to
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

        return best_match_probs, input_lang_code

    def run_tsne(self, n_components: int,
                 perplexity: float, learning_rate: float) -> List[Tuple[str, str, float, float, float]]:

        tsne_sample_list = []  # List[Tuple[str, str, float, float, float]]

        num_expressions = len(self._expressions)
        # print(f"classifier_nearest_neighbour.run_tsne : num_expressions={num_expressions}")

        # Ensure that num components is either 2 or 3.
        if (n_components != 2) and (n_components != 3):
            n_components = 2

        if num_expressions > 0:
            tsne = sklearn_manifold.TSNE(n_components=n_components,
                                         init='random',
                                         random_state=None,
                                         perplexity=perplexity,
                                         learning_rate=learning_rate)

            sent_vect_dim = len(self._expressions[0].sent_vect)
            # print(f"classifier_nearest_neighbour.run_tsne : sent_vect_dim={sent_vect_dim}")

            expr_x = np.zeros((num_expressions, sent_vect_dim))
            # expr_y = np.zeros(num_expressions)

            for idx, expression in enumerate(self._expressions):
                expr_x[idx] = expression.sent_vect
                # expr_y[idx] = expression.label_id

            tsne_x = tsne.fit_transform(expr_x)

            if n_components == 2:
                for idx, expression in enumerate(self._expressions):
                    tsne_sample_list.append((expression.text, expression.label,
                                             float(tsne_x[idx][0]), float(tsne_x[idx][1]), 0.0))
            elif n_components == 3:
                for idx, expression in enumerate(self._expressions):
                    tsne_sample_list.append((expression.text, expression.label,
                                             float(tsne_x[idx][0]), float(tsne_x[idx][1]), float(tsne_x[idx][2])))

        return tsne_sample_list
