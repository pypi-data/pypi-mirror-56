"""
Feersum_nlu PersonNameExtractor class.
"""

from typing import List, Optional  # noqa # pylint: disable=unused-import
import re
import nltk


class PersonNameExtractor(object):
    """ Perform sentiment analysis on text

    """

    def __init__(self, input_text) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.

        self.input_text = input_text

    # ---------- Utility Functions --------------

    def _check_valid_chars(self, text) -> Optional[str]:
        """Check that name contains only valid characters

        :return: name
        """

        pattern = re.compile(r"[.A-Za-z]+((\s)?((\'|\-)?([A-Za-z.])*))*$")

        text = ' '.join(text.split())  # replace multiple whitespaces with single whitespace

        check = pattern.fullmatch(text)

        if check is not None:
            return check.group()
        else:
            print("That is not a valid name. It contains unwanted characters")
            return None

    # ----------------------------------------------------#

    def _check_consecutive_chars(self, text="") -> Optional[str]:
        """Check that name has fewer than 4 consecutive vowels/consonants

        :param text: users response to "what is your name ?"
        :return: name
        """
        name = ""
        for word in text.split():
            if re.search(r'[^aeiou]{4}', word.lower()):
                # print("Too many consecutive consonants")
                return None
            elif re.search(r'[aeiou]{4}', word.lower()):
                # print("Too many consecutive vowels")
                return None
            else:
                name = name + word + " "

        return name.rstrip().title()
    # ----------------------------------------------------#

    def _check_titles(self, text) -> Optional[str]:
        """Checks if the text has a title as part of the name
        """

        title_checks = ["mr", "mrs", "ms", "dr", "mx"]

        result = text.lower()

        for check in title_checks:
            if re.search(r"\b" + re.escape(check) + r"\b", result):
                result = check + result.split(check)[1]

        return result

    # ----------------------------------------------------#

    def _preprocess_text(self, text="") -> str:
        """Perform basic preprocessing steps

        :param input_text: users response to "what is your name ?"
        :return: preprocessed text
        """

        checks = ["i'm", "i am", "im", "call me", "my", "name", "is", "named", "called", "not", "dont", "but"]

        if text != "":
            result = text.lower()
        else:
            result = self.input_text.lower()

        for check in checks:
            if re.search(r"\b" + re.escape(check) + r"\b", result):
                result = result.replace(check, "")

        if result is not None:
            result = self._check_valid_chars(result)

        if result is not None:
            result = self._check_consecutive_chars(result)

        if result is not None:
            result = self._check_titles(result)

        return result
    # ----------------------------------------------------#

    def _single_word(self, text="") -> Optional[str]:
        """ Tries to handle single word responses to "What is your name"

        :param word: the response to "What is your name" or something similar
        :return: the name, if valid or None if not
        """
        LEN_LIMIT = 20
        SINGLE_WORD_EXCEPTIONS = ["no", "nah", "nope", "why", "expletive"]

        if text != "":
            result = text.lower()
        else:
            result = self.input_text

        name = self._check_valid_chars(result.replace(".", ""))

        # check validity - length of name
        if name is not None:
            if len(name) > LEN_LIMIT:
                # print("That name has too many characters")
                return None

            if len(name) < 2:
                # print("That name has too few characters")
                return None

            if name.lower() in SINGLE_WORD_EXCEPTIONS:
                # print("Sorry {} is not a valid name. ".format(name))
                return None

                # consecutive vowels/consonants
            name = self._preprocess_text(name)

            return name.replace(".", "").title()

        return None
    # ---------------------------------------------------- #

    def _two_words(self, text="") -> Optional[str]:
        """ Tries to handle a two word space delimited responses to "What is your name"

        :param words: the response to "What is your name" or something similar
        :return: the name, if valid or None if not
        """

        LEN_LIMIT = 20
        SINGLE_WORD_EXCEPTIONS = ["no", "nah", "nope", "why", "expletive"]
        names = []

        if text != "":
            result = text.lower()
        else:
            result = self.input_text

        for word in result.split():
            # word = self._check_valid_chars(self.input_text.replace(".", ""))
            if word is not None:
                if len(word) > LEN_LIMIT:
                    # print("That name has too many characters")
                    return None

                if len(word) < 2:
                    # print("That name has too few characters")
                    return None

                if word.lower() in SINGLE_WORD_EXCEPTIONS:
                    # print("Sorry {} is not a valid name. ".format(word))
                    return None

            names.append(word.replace(".", "").title())

        return " ".join([name for name in names])
    # -------------------------------------------------- #

    def _extract_entity_names(self, tree: nltk.tree.Tree) -> List[str]:
        """ recursively extract persons name from requested input

        :param tree: POS tree
        :return: list of entities, containing the name of the user
        """

        entity_names = []

        if hasattr(tree, 'label'):
            # Houston, do we have a named entity ?

            if tree.label() == 'NE':
                # Match consecutive NNPs rather than just use them all
                # child could be a subtree or a leaf
                entity_names.append(' '.join([child[0] for child in tree if child[1] == "NNP"]))

            else:
                for child in tree:
                    if type(child) == nltk.tree.Tree:
                        entity_names.extend(self._extract_entity_names(child))
                    else:
                        continue
                    if len(child) > 1 and child[1] == "NNP":
                        entity_names.append(' '.join([child[0] for child in tree if child[1] == "NNP"]))

        return entity_names

    # ----------------------------------------------------#
    def retrieve_person_name_entities(self) -> Optional[str]:
        """

        :param input_text: users response to "what is your name ?"
        :return: name
        """
        # 1 - Preprocess the text
        clean_text = self._preprocess_text()

        if clean_text is not None:
            word_count = len(clean_text.split())
        else:
            # print("OTHER-1", clean_text)
            return None

            # 2 - Check if one word

        #         print("Retrieve - clean text -> {} - wordcount -> {} ".format(clean_text, word_count))
        if word_count == 1:
            # print("ONE WORD", clean_text)
            return self._single_word(clean_text)

        # 3 - Check if two words
        elif word_count == 2:
            # print("TWO WORDS", clean_text)
            return self._two_words(clean_text)

        else:
            # tokenized_words = [nltk.word_tokenize(words) for words in clean_text]
            tokenized_words = [nltk.word_tokenize(clean_text.title())]
            tagged_words = [nltk.pos_tag(words) for words in tokenized_words]
            chunked_words = nltk.ne_chunk_sents(tagged_words, binary=True)

            entity_names = []

            for i, tree in enumerate(chunked_words):
                entity_names.extend(self._extract_entity_names(tree))
                # print("Entity - ", clean_text, tree)
                if entity_names:
                    # print("NLTK", clean_text, entity_names)
                    return entity_names[0].title()
            # print("OTHER-2", clean_text)
            return None
#
# extractor = PersonNameExtractor("My name is Clark Kent").retrieve_person_name_entities()
# print("Extracted Name : ",extractor)
