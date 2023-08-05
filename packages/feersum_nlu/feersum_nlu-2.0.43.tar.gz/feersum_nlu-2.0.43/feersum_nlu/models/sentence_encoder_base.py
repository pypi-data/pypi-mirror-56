"""
FeersumNLU Sentence Encoder: Base class.
"""

from abc import ABC, abstractmethod
from typing import List, Set, Optional  # noqa # pylint: disable=unused-import
import numpy as np


class SentenceEncoderBase(ABC):
    """
    FeersumNLU Sentence Encoder: Base class.
    """

    def __init__(self,
                 stop_words: Optional[Set[str]] = None,
                 spacies: Optional[List[str]] = None) -> None:
        """

        :param stop_words: The set of words to ignore when encoding text.
        :param spacies: List of tokens to replace with spaces during tokenisation.
        """
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        self._stop_word_set = stop_words
        self._spacies_list = spacies

        # Model should maintain list of unknown words it encounters if possible!
        self._unknown_vocab_set = set()  # type: Set[str]

    @abstractmethod
    def is_created(self) -> bool:
        """Return True if the encoder was instantiated properly."""
        pass

    @abstractmethod
    def get_vect_dim(self) -> int:
        """Return the encoded vector dimension."""
        pass

    @abstractmethod
    def spell_correct_word(self, word: str) -> str:
        """Spell correct the word."""
        pass

    # @abstractmethod
    # def spell_correct_text(self, text: str) -> str:
    #     """Spell correct the text."""
    #     pass

    @abstractmethod
    def add_word_similar_to(self, new_word: str, similar_word: str):
        """Add a word that is similar to an existing word.

        :param new_word: The new word to add to the vocabulary.
        :param similar_word: The existing word to use the vector of.
        """
        pass

    @abstractmethod
    def calc_word_similarity(self, word_a: str, word_b: str) -> float:
        """ Calculate the similarity of the two words.

        :param word_a:
        :param word_b:
        :return:
        """
        pass

    # Default implementation of tokenize. Sentence encoders should specialise this as required.
    def tokenize(self, text: str) -> List[str]:
        """Replace substrings from _spacies_list with spaces and tokenise the string leaving out the stop words."""
        spacied_text = text

        if self._spacies_list is not None:
            for spacy in self._spacies_list:
                spacied_text = spacied_text.replace(spacy, " ")

        # spacied_tokens = nltk.word_tokenize(spacied_text)
        spacied_tokens = spacied_text.lower().split()

        tokens = []

        for spacied_token in spacied_tokens:
            # token = spacied_token.replace(" ", "")
            # if token!="" and token not in self._stop_word_set:
            if self._stop_word_set is None or spacied_token not in self._stop_word_set:
                tokens.append(spacied_token)

        return tokens

    @abstractmethod
    def calc_sentence_vector(self, text: str, spell_correct: bool) -> np.array:
        pass

    # ===================================
    # === Common class helper methods ===
    # ===================================
    @staticmethod
    def get_nvect(vect: np.array):
        norm = np.linalg.norm(vect)

        if norm != 0.0:
            return vect / norm
        else:
            return np.zeros(vect.shape)

    @staticmethod
    def calc_cosine_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the cosine distance between vect_a and vect_b. returns vect_a.vect_b/(|vect_a|*|vect_b|)
        -1.0 = dissimilar, 1.0 = similar. """
        vect_a_length = np.linalg.norm(vect_a)
        vect_b_length = np.linalg.norm(vect_b)

        if vect_a_length != 0.0 and vect_b_length != 0.0:
            score = np.dot(vect_a, vect_b) / (vect_a_length * vect_b_length)
        else:
            score = 0.0

        return score

    @staticmethod
    def calc_l1_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the L1 distance between vect_a and vect_b. returns sum_reduce(abs(vect_a - vect_b))
        0.0 = similar, larger = dissimilar. """
        # return np.linalg.norm(vect_a - vect_b, ord=1)  # SLOWER; 150% the time of below version.
        return np.sum(np.abs(vect_a - vect_b))  # FASTER

    @staticmethod
    def calc_l2_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the L1 distance between vect_a and vect_b. returns |vect_a - vect_b|
        0.0 = similar, larger = dissimilar. """
        diff = vect_a - vect_b
        return np.dot(diff, diff)

    def calc_common_words_sim(self,
                              input_text_a: str,
                              input_text_b: str,
                              stop_words=None) -> float:
        """ Return the sentence similarity based on common words.
        1.0 = similar, 0.0 = dissimilar. """
        f = 0.75  # Only consider the first n characters of words; acts like a simple stemmer for all languages
        ngrams_a = set()  # type: Set[str]
        ngrams_b = set()  # type: Set[str]

        input_tokens_a = self.tokenize(input_text_a)
        input_tokens_b = self.tokenize(input_text_b)

        for t in input_tokens_a:
            if len(t) > 3:  # Only consider words longer than 3 characters; ignore short stopper words.
                n = max(3, int(f * len(t)))
                ngrams_a.add(t[:min(n, len(t))])

        for t in input_tokens_b:
            if len(t) > 3:  # Only consider words longer than 3 characters; ignore short stopper words.
                n = max(3, int(f * len(t)))
                ngrams_b.add(t[:min(n, len(t))])

        length_a = 0
        common_a = 0

        for t in ngrams_a:
            if t not in stop_words:
                length_a += 1
                if t in ngrams_b:
                    common_a += 1

        length_b = 0
        common_b = 0

        for t in ngrams_b:
            if t not in stop_words:
                length_b += 1
                if t in ngrams_a:
                    common_b += 1

        if length_a == 0 or length_b == 0:
            return 0.0

        # return 0.5 * common_a / length_a + 0.5 * common_b / length_b
        # The below sim metric seems to be slightly more accurate on the Quora date at least.
        return (common_a + common_b) / (length_a + length_b)

    def get_unknown_vocab_size(self):
        """Get the number of words encountered that were not in the vocab."""
        return len(self._unknown_vocab_set)

    def get_unknown_vocab(self) -> Set[str]:
        """Get the list of words encountered that were not in the vocab."""
        return self._unknown_vocab_set

    def reset_unknown_vocab(self):
        """Reset the list of words encountered that were not in the vocab."""
        self._unknown_vocab_set = set()
