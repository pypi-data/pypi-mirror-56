"""
FeersumNLU Sentence Encoder: Word manifold (GloVe, word2vec, etc.) based sentence encoder.
"""

from typing import Dict, List, Set, Optional, Union  # noqa # pylint: disable=unused-import
import numpy as np
import logging

from feersum_nlu.models import sentence_encoder_base


class WordManifold(sentence_encoder_base.SentenceEncoderBase):
    """
    FeersumNLU Sentence Encoder: Word manifold (GloVe, word2vec, etc.) based sentence encoder.
    """

    def __init__(self,
                 vectors_file: str,
                 stop_words: Optional[Set[str]] = None,
                 spacies: Optional[List[str]] = None) -> None:
        """Init the word manifold using pre-trained vectors.

        :param vectors_file: The pre-trained vector file to load.
        :param stop_words: The set of words to ignore when encoding text.
        :param spacies: List of tokens to replace with spaces during tokenisation.
        """
        super().__init__(stop_words=stop_words, spacies=spacies)

        # The dictionary word vectors.
        vocab = {}  # type: Dict[str, np.array]

        # The dictionary of inverse word freq.
        vocab_fc = {}  # type: Dict[str, int]

        if stop_words is None:
            stop_words = set()

        # Zipf's law: The n'th most frequent word appears with a frequency of about 1/n of the most frequent word.
        # Note: The words in the vector files are stored with the most common words first!

        # Read the word vectors.
        try:
            logging.info(f"models.word_manifold.__init__: Loading model {vectors_file}...")

            with open(vectors_file, 'r') as f:
                word_count = 0  # type: int

                for line in f:
                    first_space = line.find(' ')
                    word = line[:first_space]

                    if word not in stop_words:
                        vector = np.fromstring(line[first_space:], dtype=np.float, sep=' ')
                        vocab[word] = vector

                        word_count += 1
                        vocab_fc[word] = word_count  # zipf's law

            logging.info("models.word_manifold.__init__: Loading model done!")
        except IOError:
            logging.error("models.word_manifold.__init__: Error loading model!")

        # Set embeddings dimension to arb word's vector dimension.
        self._vect_dim = next(iter(vocab.values())).shape[0] if (len(vocab) > 0) else 0

        self._vocab = vocab
        self._vocab_fc = vocab_fc

    def is_created(self) -> bool:
        """Return True if the encoder was instantiated properly."""
        return self._vect_dim > 0

    def get_vect_dim(self):
        """Return the encoded vector dimension."""
        return self._vect_dim

    # =========================================================
    # === Spell correct =======================================
    # =========================================================
    def _is_word_in_vocab(self, word: str) -> bool:
        """Return the subset of words that are in the vocabulary."""
        return word in self._vocab

    def _get_in_vocab_words(self, words: Union[Set[str], List[str]]):
        """Return the subset of words that are in the vocabulary."""
        return {w for w in words if w in self._vocab}

    def _get_out_of_vocab_words(self, words: Union[Set[str], List[str]]):
        """Return the subset of words that are NOT in the vocabulary."""
        return {w for w in words if w not in self._vocab}

    @staticmethod
    def _edits0(word) -> Set[str]:
        """Return the word itself."""
        return {word}

    @staticmethod
    def _splits(word: str):
        """Return a list of all possible (head, tail) pairs that comprise word."""
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    @staticmethod
    def _edits1(word: str) -> Set[str]:
        """Return all strings that are one edit away from word."""
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        pairs = WordManifold._splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in alphabet]

        return set(deletes + transposes + replaces + inserts)

    @staticmethod
    def _edits2(word: str) -> Set[str]:
        """"Return all strings that are two edits away from word."""
        return {e2 for e1 in WordManifold._edits1(word) for e2 in WordManifold._edits1(e1)}

    def spell_correct_word(self, word: str) -> str:
        """Find the spell correction for this word OR just return the input! Short words are assumed to be correct!"""
        if 3 <= len(word) <= 20:
            # Set candidates equal to the first non-empty set of in-vocab/valid words from edits0, edits1 or edits2
            # Note: I'm making use of Python's 'or' operation returns the result of the first non-empty set!
            candidates = (self._get_in_vocab_words(WordManifold._edits0(word)) or
                          self._get_in_vocab_words(WordManifold._edits1(word)) or
                          self._get_in_vocab_words(WordManifold._edits2(word)))

            if len(candidates) > 0:
                return min(candidates, key=self._vocab_fc.get)
            else:
                return word
        else:
            return word
    # =========================================================
    # =========================================================
    # =========================================================

    def _get_word_vect(self, word: str) -> Optional[np.array]:
        """Retrieve the word's stored vector.

        :param word: The word to retrieve the vector of.
        """
        word_vect = self._vocab.get(word.lower())

        return word_vect

    def add_word_similar_to(self, new_word: str, similar_word: str):
        """Add a word that is similar to an existing word and reference the existing word vector.

        :param new_word: The new word to add to the vocabulary.
        :param similar_word: The existing word to use the vector of.
        :return : The vector of new_word.
        """
        # Assign the vector to new_word even if it already exist in the vocab!
        vect = self._get_word_vect(similar_word.lower())
        fc = self._vocab_fc.get(similar_word.lower())

        if vect is not None and fc is not None:
            self._vocab[new_word.lower()] = vect
            # The new word is assumed to have the same probability of occurring as the existing word.
            self._vocab_fc[new_word.lower()] = fc

    def calc_word_similarity(self, word_a: str, word_b: str) -> float:
        """ Calculate the similarity of the two words.

        :param word_a:
        :param word_b:
        :return:
        """
        vect_a = self._get_word_vect(word_a)
        vect_b = self._get_word_vect(word_b)

        if vect_a is not None and vect_b is not None:
            nvect_a = self.get_nvect(vect_a)
            nvect_b = self.get_nvect(vect_b)
            # ToDo: What do the lengths of the vectors represent?
            # ToDo: Why not use the Euclidean distance??
            return np.dot(nvect_a, nvect_b)
        else:
            return 0.0

    def tokenize(self, text: str) -> List[str]:
        return super().tokenize(text)

    def calc_sentence_vector(self, text: str, spell_correct: bool) -> np.array:
        """Use the manifold theorem to generate a maxout sentence vector.

        :param text: The sentence text.
        :param spell_correct: If true then correct the spelling before calculating the sentence vector.
        """
        sent_vect = np.zeros(self._vect_dim)
        # w_total = 0.0

        tokens = self.tokenize(text)

        for word in tokens:
            word_vect = self._get_word_vect(word)
            # word_prob = self.get_word_probability(word)

            # if word not found and it is a number then replace with 'number' token.
            #   ToDo: Make this work for the other languages.
            if word_vect is None and word.isdigit():
                word = 'number'
                word_vect = self._get_word_vect(word)

            if word_vect is None and spell_correct:
                # Try to spell correct.
                closest_word = self.spell_correct_word(word)

                # print(word + "=>" + str(closest_word))

                if closest_word is not None:
                    word_vect = self._get_word_vect(closest_word)
                    # word_prob = self.get_word_probability(closest_word)
                else:
                    self._unknown_vocab_set.add(word)

            if word_vect is not None:
                # word_nvect = word_vect
                word_nvect = self.get_nvect(word_vect)

                # a = 0.00015
                # w = a/(a + word_prob)

                # sent_vect += word_nvect * w
                # w_total += w

                # Generate maxout sentence vector.
                # What is the significant of the length of the vector?
                # sent_vect = np.fmax(np.absolute(word_nvect * w), sent_vect)
                sent_vect = np.fmax(np.absolute(word_nvect), sent_vect)  # pylint: disable=E1111

        # u = self._get_nvect(self.get_word_vect('just'))
        # proj = np.dot(u, sent_vect)
        # sent_vect = sent_vect - u * proj

        # sent_vect_norm = np.linalg.norm(sent_vect)
        # if sent_vect_norm > 0.0:
        #    sent_vect = sent_vect / sent_vect_norm
        # if w_total > 0.0:
        #    sent_vect = sent_vect / w_total

        return sent_vect
