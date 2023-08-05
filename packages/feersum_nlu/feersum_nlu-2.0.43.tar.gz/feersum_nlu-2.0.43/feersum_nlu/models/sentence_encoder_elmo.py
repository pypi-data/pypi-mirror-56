"""
FeersumNLU Sentence Encoder: Encode text with ELMO
"""

from typing import List, Set, Optional, Union  # noqa # pylint: disable=unused-import
import numpy as np
import logging

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import contractions

import tensorflow_hub as hub
import tensorflow as tf

from feersum_nlu.models import sentence_encoder_base


class SentenceEncoderElmo(sentence_encoder_base.SentenceEncoderBase):
    """
    FeersumNLU Sentence Encoder: Encode text with ELMO
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

        self.module_url = model_file  # "https://tfhub.dev/google/elmo/2"
        self.preprocess_text = False

        # reduce TF logging output
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        logging.info(f"models.sentence_encoder_elmo.__init__: Loading model {model_file}...")

        # Load the model.
        g = tf.Graph()

        try:
            with g.as_default():  # pylint: disable=E1129
                self._tf_input_text = tf.compat.v1.placeholder(tf.string)
                self._encoder_module = hub.Module(self.module_url, trainable=False)
                self._encoder = self._encoder_module(self._tf_input_text, signature="default", as_dict=True)
                init_op = tf.group([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])

            g.finalize()

            self._tf_session = tf.compat.v1.Session(graph=g)
            self._tf_session.run(init_op)

            logging.info("models.sentence_encoder_elmo.__init__: Loading model done.")
            self._is_created = True

        except (RuntimeError, ValueError):
            self._is_created = False
            logging.info("models.sentence_encoder_elmo.__init__: Loading model FAILED!")

        if self._is_created:
            # === Test model and get vector size ===
            encodings = self._tf_session.run(self._encoder, {self._tf_input_text: ["Test sentence with some words."]})
            self._vect_dim = encodings['default'].shape[1]
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
            text = SentenceEncoderElmo.remove_special_characters(text, remove_digits=False)

            # lower case
            text = text.lower()

            # expand contractions
            text = SentenceEncoderElmo.expand_contractions(text)

            # remove stopwords
            text = SentenceEncoderElmo.remove_stopwords(text, SentenceEncoderElmo.STOPWORDS)

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

    def elmo_default_context_vector(self, input_text: Union[List[str], str], spell_correct: bool) -> np.array:
        """

        :param input_text: List of strings to encode/embed
        :param spell_correct:
        :return: ['default'] is a fixed mean-pooling of all contextualised
        word representations of text, with shape [batch size, 1024]. The output dictionary also contains
        'word_emb', 'lstm_outputs1', 'lstm_outputs2' , 'elmo' and 'sequence_len'
        """

        if isinstance(input_text, str):
            text_list = [input_text]  # type: List[str]
        else:
            text_list = input_text

        embeddings = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['default']
        return embeddings

    def calc_sentence_vector(self, text: str, spell_correct: bool) -> np.array:
        encodings = self.elmo_default_context_vector(text, spell_correct=False)

        return encodings[0]  # Return only one sentence's encoding. This method's interface is a single sentence.

    def elmo_word_emb(self, text_list: List[str], spell_correct: bool) -> np.array:
        """ 1 of 4 trainable scalar weights for layer aggregation,the character-based word representation

        :param text_list: list of strings
        :param spell_correct:
        :return: the character-based word representations with shape [batch_size, max_length, 512].
        """

        embeddings = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['word_emb']

        return embeddings

    def elmo_lstm_1(self, text_list: List[str], spell_correct: bool) -> np.array:
        """1 of 4 trainable scalar weights for layer aggregation, the first LSTM hidden state

        :param text_list: list of strings
        :param spell_correct:
        :return: the first LSTM hidden state with shape [batch_size, max_length, 1024].
        """

        lstm_outputs = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['lstm_outputs1']
        return lstm_outputs

    def elmo_lstm_2(self, text_list: List[str], spell_correct: bool) -> np.array:
        """1 of 4 trainable scalar weights for layer aggregation,  the second LSTM hidden state

        :param text_list: list of strings
        :param spell_correct:
        :return: the second LSTM hidden state with shape [batch_size, max_length, 1024].
        """

        lstm_outputs = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['lstm_outputs2']
        return lstm_outputs

    def elmo_weighted_sum(self, text_list: List[str], spell_correct: bool) -> np.array:
        """1 of 4 trainable scalar weights for layer aggregation,the weighted sum of the 3 layers in ELMo

        :param text_list: list of strings
        :param spell_correct:
        :return:  the weighted sum of the 3 layers, where the weights are trainable. This tensor
         has shape [batch_size, max_length, 1024]
        """
        embeddings = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['elmo']
        return embeddings

    def elmo_seq_len(self, text_list: List[str], spell_correct: bool) -> np.array:
        """ keep track of the length of each text sample, when performing lazy tokenising (split on spaces)

        :param text_list: list of strings
        :param spell_correct:
        :return: the length of each text sample (split on spaces)
        """
        seq_lens = self._tf_session.run(self._encoder, {self._tf_input_text: text_list})['sequence_len']
        return seq_lens
