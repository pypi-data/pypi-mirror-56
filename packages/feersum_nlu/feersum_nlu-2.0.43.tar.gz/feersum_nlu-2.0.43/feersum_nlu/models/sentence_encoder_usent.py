"""
FeersumNLU Sentence Encoder: USent (Universal Sentence) Encoder.
"""

from typing import List, Set, Optional  # noqa # pylint: disable=unused-import
import numpy as np
import logging

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import contractions

import tensorflow_hub as hub
import tensorflow as tf

from feersum_nlu.models import sentence_encoder_base


class SentenceEncoderUSent(sentence_encoder_base.SentenceEncoderBase):
    """
    FeersumNLU Sentence Encoder: USent (Universal Sentence) Encoder.
    """

    def __init__(self,
                 model_file: str,
                 stop_words: Optional[Set[str]] = None,
                 spacies: Optional[List[str]] = None) -> None:
        """Init the USent encoder using pre-trained model file.

        :param model_file: The pre-trained model's path and name.
        :param stop_words: The set of words to ignore when encoding text.
        :param spacies: List of tokens to replace with spaces during tokenisation.
        """
        super().__init__(stop_words=stop_words, spacies=spacies)

        self.module_url = model_file
        self.preprocess_text = False

        # reduce TF logging output
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        logging.info(f"models.sentence_encoder_usent.__init__: Loading model {model_file}...")

        # Load the model.
        g = tf.Graph()

        try:
            with g.as_default():  # pylint: disable=E1129
                self._tf_input_text = tf.compat.v1.placeholder(tf.string)
                self._encoder_module = hub.Module(self.module_url, trainable=False)
                self._encoder = self._encoder_module(self._tf_input_text)
                init_op = tf.group([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])

            g.finalize()

            self._tf_session = tf.compat.v1.Session(graph=g)
            self._tf_session.run(init_op)

            logging.info("models.sentence_encoder_usent.__init__: Loading model done.")
            self._is_created = True

        except (RuntimeError, ValueError):
            self._is_created = False
            logging.info("models.sentence_encoder_usent.__init__: Loading model FAILED!")

        if self._is_created:
            # === Test model and get vector size ===
            encodings = self._tf_session.run(self._encoder, {self._tf_input_text: ["Test sentence with some words."]})
            self._vect_dim = encodings.shape[1]
            # === ===

    # ToDo: How to handle this for other languages?!
    STOPWORDS = set(stopwords.words('english'))

    def is_created(self) -> bool:
        """Return True if the encoder was instantiated properly."""
        return self._is_created

    @staticmethod
    def expand_contractions(text):
        # ToDo: How to handle this for other languages?!
        return contractions.fix(text)

    @staticmethod
    def remove_special_characters(text, remove_digits=False):
        pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
        text = re.sub(pattern, '', text)
        return text

    @staticmethod
    def remove_stopwords(text, stopwords):
        # ToDo: This is broken for word contractions! Consider renaming the method to
        # indicate that contractions MUST first be expanded.
        tokenized_text = word_tokenize(text)
        text = " ".join([token for token in tokenized_text if token not in stopwords])
        return text

    @staticmethod
    def text_processor(texts: List[str]) -> List[str]:
        """
        Pre-process text to expand contractions, remove extra whitespace, unwanted chars and stopwords, etc.

        :param texts: Text or list of texts to be preprocessed.
        :return processed_texts: Preprocessed text.
        """
        processed_texts = []
        for text in texts:
            # remove extra whitespace
            text = text.strip()

            # remove unwanted characters
            text = SentenceEncoderUSent.remove_special_characters(text, remove_digits=False)

            # lower case
            text = text.lower()

            # expand contractions
            text = SentenceEncoderUSent.expand_contractions(text)

            # remove stopwords
            text = SentenceEncoderUSent.remove_stopwords(text, SentenceEncoderUSent.STOPWORDS)

            processed_texts.append(text)

        return processed_texts

    def get_vect_dim(self) -> int:
        """Return the encoded vector dimension."""
        return self._vect_dim

    def spell_correct_word(self, word: str) -> str:
        """Spell correct the word."""
        # ToDo: Spell correction.
        return word

    def add_word_similar_to(self, new_word: str, similar_word: str):
        """Add a word that is similar to an existing word.

        :param new_word: The new word to add to the vocabulary.
        :param similar_word: The existing word to use the vector of.
        """
        # ToDo: Data structure to hold tokens and their in vocab tokens to replace them with..
        pass

    def calc_word_similarity(self, word_a: str, word_b: str) -> float:
        """ Calculate the similarity of the two words.

        :param word_a:
        :param word_b:
        :return:
        """
        return 0.0

    def tokenize(self, text: str) -> List[str]:
        # return super().tokenize(text)
        return word_tokenize(text)  # Use NLTK's tokeniser like the model's text pre-processing.

    def calc_sentence_vector(self, text: str, spell_correct: bool) -> np.array:
        # is the class instance set up with text preprocessing or not
        if self.preprocess_text:
            processed_query = self.text_processor([text])
        else:
            processed_query = [text]

        # ToDo: Spell correction.

        encodings = self._tf_session.run(self._encoder,
                                         feed_dict={self._tf_input_text: processed_query})

        return encodings[0]
