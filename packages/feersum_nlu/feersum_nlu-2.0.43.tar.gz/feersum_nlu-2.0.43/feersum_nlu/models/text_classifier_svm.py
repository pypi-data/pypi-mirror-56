"""
FeersumNLU Classifier: SVM
"""

from typing import Dict, Tuple, List, Optional, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.sentence_encoder_base import SentenceEncoderBase
from feersum_nlu.models import text_classifier_base

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV

import numpy as np


# from itertools import chain
# from collections import defaultdict
# from sklearn.feature_extraction.text import _make_int_array
# import numpy as np
# import scipy.sparse as sp
#
# class OnlineCountVectorizer(CountVectorizer):
#     """Scikit-learn CountVectorizer with online learning
#     """
#     def partial_refit(self, raw_documents):
#         """Update existing vocabulary dictionary with all oov (out of vocabulary) tokens in the raw documents.
#          Parameters
#          ----------
#          raw_documents : iterable
#              An iterable which yields either str, unicode or file objects.
#          Returns
#          -------
#          self: OnlineCountVectorizer
#          """
#         self.partial_refit_transform(raw_documents)
#         return self
#
#     def partial_refit_transform(self, raw_documents):
#         """Update the exiting vocabulary dictionary and return term-document matrix.
#         This is equivalent to partial_refit followed by transform, but more efficiently
#         implemented.
#         Parameters
#         ----------
#         raw_documents : iterable
#             An iterable which yields either str, unicode or file objects.
#         Returns
#         -------
#         X : array, [n_samples, n_features]
#             Document-term matrix.
#         """
#         analyzer = self.build_analyzer()
#         analyzed_documents = [analyzer(doc) for doc in raw_documents]
#         new_tokens = set(chain.from_iterable(analyzed_documents))
#         oov_tokens = new_tokens.difference(set(self.vocabulary_.keys()))
#
#         if oov_tokens:
#             logger.info("adding {} tokens".format(len(oov_tokens)))
#             max_index = max(self.vocabulary_.values())
#             oov_vocabulary = dict(zip(oov_tokens, list(range(max_index + 1, max_index + 1 + len(oov_tokens), 1))))
#             self.vocabulary_.update(oov_vocabulary)
#
#         _, X = self._count_analyzed_vocab(analyzed_documents, True)
#         return X
#
#     def _count_analyzed_vocab(self, analyzed_documents, fixed_vocab):
#         """Create sparse feature matrix, and vocabulary where fixed_vocab=False.
#         For consistency this is a slightly edited version of feature_extraction.text._count_vocab with the document
#         analysis factored out.
#         """
#         if fixed_vocab:
#             vocabulary = self.vocabulary_
#         else:
#             # Add a new value when a new vocabulary item is seen
#             vocabulary = defaultdict()
#             vocabulary.default_factory = vocabulary.__len__
#
#         j_indices = []
#         indptr = _make_int_array()
#         values = _make_int_array()
#         indptr.append(0)
#         for analyzed_doc in analyzed_documents:
#             feature_counter = {}
#             for feature in analyzed_doc:
#                 try:
#                     feature_idx = vocabulary[feature]
#                     if feature_idx not in feature_counter:
#                         feature_counter[feature_idx] = 1
#                     else:
#                         feature_counter[feature_idx] += 1
#                 except KeyError:
#                     # Ignore out-of-vocabulary items for fixed_vocab=True
#                     continue
#
#             j_indices.extend(feature_counter.keys())
#             values.extend(feature_counter.values())
#             indptr.append(len(j_indices))
#
#         j_indices = np.asarray(j_indices, dtype=np.intc)
#         indptr = np.frombuffer(indptr, dtype=np.intc)
#         values = np.frombuffer(values, dtype=np.intc)
#
#         X = sp.csr_matrix((values, j_indices, indptr),
#                           shape=(len(indptr) - 1, len(vocabulary)),
#                           dtype=self.dtype)
#         X.sort_indices()
#         return vocabulary, X


class TextClassifierSVM(text_classifier_base.TextClassifierBase):
    """
    FeersumNLU Classifier: SVM.
    """

    def __init__(self, language_model_dict: Optional[Dict[str, SentenceEncoderBase]]) -> None:
        super().__init__(language_model_dict=language_model_dict)
        self._next_label_idx = 0

        # self._word_ngram_vectorizer = CountVectorizer(analyzer='word', ngram_range=word_ngrams, max_features=500000,
        #                                               lowercase=True)
        # self._char_ngram_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=char_ngrams, max_features=500000,
        #                                               lowercase=True)
        #
        # if (word_ngrams != (0, 0)) and (char_ngrams != (0, 0)):
        #     self._union_vectorizer = FeatureUnion([('words', self._word_ngram_vectorizer),
        #                                            ('chars', self._char_ngram_vectorizer)])
        # elif word_ngrams != (0, 0):
        #     self._union_vectorizer = FeatureUnion([('words', self._word_ngram_vectorizer)])
        # else:
        #     self._union_vectorizer = FeatureUnion([('chars', self._char_ngram_vectorizer)])

        self._word_ngram_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2), max_features=500000,
                                                      lowercase=True)
        self._char_2gram_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(2, 2), max_features=500000,
                                                      lowercase=True)
        self._char_4gram_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(4, 4), max_features=500000,
                                                      lowercase=True)
        self._char_6gram_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(6, 6), max_features=500000,
                                                      lowercase=True)

        self._union_vectorizer = FeatureUnion([
            ('w', self._word_ngram_vectorizer),
            ('c2', self._char_2gram_vectorizer),
            ('c4', self._char_4gram_vectorizer),
            ('c6', self._char_6gram_vectorizer),
        ])

        self._clsfr = None  # type: Optional[SGDClassifier]

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
        # Online training not supported yet.
        return False

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

        if len(training_list) > 0:
            text_inputs = []  # type: List[str]
            labels = []  # type: List[str]
            class_size_dict = {}  # type: Dict[str, int]

            for training_sample in training_list:
                text_inputs.append(training_sample[0])
                labels.append(training_sample[1])
                class_size_dict[training_sample[1]] = class_size_dict.get(training_sample[1], 0)

            min_class_size = min(class_size_dict.values())

            feature_counts = self._union_vectorizer.fit_transform(text_inputs)

            cross_validation_folds = 3

            if min_class_size >= cross_validation_folds:
                # Do grid search with cross validation if the smallest class has enough samples for cross validation.
                estimator = SGDClassifier(max_iter=1000000, n_iter_no_change=20, tol=1e-6, verbose=0)
                parameters = {'loss': ['log', 'modified_huber'], 'alpha': [0.001, 0.01, 0.1]}
                grid_search_cv = GridSearchCV(estimator=estimator, param_grid=parameters, cv=cross_validation_folds)
                grid_search_cv.fit(feature_counts, labels)
                # print("best_params_ =", grid_search_cv.best_params_)
                self._clsfr = grid_search_cv.best_estimator_
            else:
                self._clsfr = SGDClassifier(loss='log', alpha=0.01,
                                            max_iter=1000000, n_iter_no_change=20, tol=1e-6, verbose=0)
                self._clsfr.fit(feature_counts, labels)

            # === Update the _labels set and the _label_to_idx mapping ===
            for training_sample in training_list:
                label = training_sample[1]

                self._labels.add(label)
                if self._label_to_idx.get(label) is None:
                    self._label_to_idx[label] = self._next_label_idx
                    self._next_label_idx += 1

            return True
        else:
            return False

    def get_informative_features(self, top_n: int) -> Dict[str, List[Tuple[str, float]]]:
        """
        Get the list of most informative features per class.

        :param top_n: The number of top features per class to list.
        :return: A dictionary of features per class.
        """
        informative_feature_dict = {}  # type: Dict[str, List[Tuple[str, float]]]

        if self._clsfr is not None:
            feature_names = self._union_vectorizer.get_feature_names()
            class_labels = self._clsfr.classes_

            # Note: _clsfr.coef_ behaves different when only two classes!
            if len(class_labels) > 2:
                for i, class_label in enumerate(class_labels):
                    argsorted_feature_indexes = np.argsort(self._clsfr.coef_[i])
                    top_n_feature_indexes = argsorted_feature_indexes[-min(top_n, len(argsorted_feature_indexes)):]
                    informative_feature_dict[class_label] = []
                    for j in top_n_feature_indexes:
                        informative_feature_dict[class_label].append((feature_names[j], self._clsfr.coef_[i][j]))
            else:
                i, class_label = 0, 'success'
                argsorted_feature_indexes = np.argsort(self._clsfr.coef_[i])
                top_n_feature_indexes = argsorted_feature_indexes[-min(top_n, len(argsorted_feature_indexes)):]
                informative_feature_dict[class_label] = []
                for j in top_n_feature_indexes:
                    informative_feature_dict[class_label].append((feature_names[j], self._clsfr.coef_[i][j]))

        return informative_feature_dict

    def classify(self, input_text: str, lang_code_hint: Optional[str],
                 weak_match_threshold: float,
                 top_n: int) -> Tuple[List[Tuple[str, float]], str]:
        """ Find the n best matches to the input text.

        :param input_text: The expression to look for in the expression set.
        :param lang_code_hint: A hint for the language of the input text.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)] plus the lang_code of the input text.
        """
        # if len(self._language_model_dict) == 1:
        #     # Override the text language code if only one language model is present.
        #     input_lang_code = next(iter(self._language_model_dict))
        # elif lang_code_hint is not None:
        #     input_lang_code = lang_code_hint
        # else:
        #     # Fill in the text language code.
        #     input_lang_code = self._classify_text_language(input_text)
        input_lang_code = str(lang_code_hint)

        if self._clsfr is not None:
            feature_counts = self._union_vectorizer.transform([input_text])
            y_proba_list = self._clsfr.predict_proba(feature_counts)

            scored_labels = []  # type: List[Tuple[str, float]]

            for i, class_label in enumerate(self._clsfr.classes_):
                prob = y_proba_list[0, i]  # type: float

                if prob >= (1.0 - weak_match_threshold):
                    scored_labels.append((class_label, prob))

            scored_labels.sort(key=lambda scored_label: scored_label[1], reverse=True)

            return scored_labels[:min(top_n, len(scored_labels))], input_lang_code
        else:
            return [], input_lang_code

    def run_tsne(self, n_components: int,
                 perplexity: float, learning_rate: float) -> List[Tuple[str, str, float, float, float]]:

        tsne_sample_list = []  # type: List[Tuple[str, str, float, float, float]]

        return tsne_sample_list
