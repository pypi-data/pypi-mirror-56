"""
Feersum_nlu FAQMatcher class.
"""

import json
import csv
from itertools import islice
import logging

from typing import Dict, Tuple, List, Set, NamedTuple, Optional, Union  # noqa # pylint: disable=unused-import

from feersum_nlu.models.word_manifold import WordManifold
from feersum_nlu.models.lid import lang_ident_nbayes

import numpy as np
import math
import sklearn.manifold as sklearn_manifold
import time

# === The question type - sent_vec and lang_code are filled in during training!
# Python 3.5
QuestionT = NamedTuple('QuestionT',
                       [('text', str), ('answer_id', int),
                        ('sent_vect', np.array),
                        ('answer', str),
                        ('lang_code', str)])


# Python 3.6
# class QuestionT(NamedTuple):
#     text: str
#     answer_id: int
#     sent_vect: np.array
#     answer: str
# ===

class FAQMatcher(object):
    """
    Feersum_nlu FAQMatcher class.
    """

    def __init__(self, manifold_dict: Optional[Dict[str, WordManifold]]) -> None:
        # The question training data is also the model for this model type!
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.

        self._faq_questions = []  # type: List[QuestionT]
        self._faq_labels = set()  # type: Set[str]

        self._manifold_dict = manifold_dict

    def __getstate__(self):
        """Do not pickle the _manifold_dict with this object!"""
        state = self.__dict__.copy()
        del state['_manifold_dict']
        return state

    def __setstate__(self, state):
        """_manifold_dict not pickled with the object!"""
        self.__dict__.update(state)
        self._manifold_dict = None

    def _classify_text_language(self, input_text: str) -> str:
        lang_ident = ""

        result_list = lang_ident_nbayes(input_text)

        if result_list is not None:
            # Pick the best scoring language from the ones that the FAQ expects!
            for lang, score in result_list:
                if (self._manifold_dict is None) or (lang in self._manifold_dict):
                    lang_ident = lang
                    break  # break after best score found in language dict!

        return lang_ident

    def set_word_manifold_dict(self, manifold_dict: Dict[str, WordManifold]) -> None:
        """Set or update the word manifold_dict. An update is required after unpickling!
        See refresh_model_vectors to also update the model's sentence vectors if a new word manifold was supplied."""
        self._manifold_dict = manifold_dict

    def get_model_questions(self) -> List[QuestionT]:
        return self._faq_questions

    def train_online(self,
                     training_list: List[QuestionT],
                     testing_list: List[QuestionT],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of questions.
        :param testing_list: List of questions to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        if self._manifold_dict is None:
            logging.error("intent_classifier.train_online - _manifold_dict is None!")
            return False

        lang_count_dict = {}  # type: Dict[str, int]

        # Train the model - Calculate the FAQ question vectors just once here.
        for i, training_sample in enumerate(training_list):
            if len(self._manifold_dict) == 1:
                # Override the text language code if only one manifold is present.
                lang_code = next(iter(self._manifold_dict))
            elif training_sample.lang_code == "":
                # Fill in the text language code if not supplied.
                lang_code = self._classify_text_language(training_sample.text)
            else:
                # Use the supplied language code.
                lang_code = training_sample.lang_code

            # Keep track of how many samples there are per language.
            count = lang_count_dict.get(lang_code)
            if count is None:
                count = 0
            lang_count_dict[lang_code] = count + 1

            manifold = self._manifold_dict.get(lang_code)

            if manifold is not None:
                spell_correct = lang_code in {"eng", "afr"}

                # The model is trained by updating _questions list. The list is the model!
                self._faq_questions.append(QuestionT(training_sample.text,
                                                     training_sample.answer_id,
                                                     manifold.calc_sentence_vector(training_sample.text,
                                                                                   spell_correct),
                                                     training_sample.answer,
                                                     lang_code))

                self._faq_labels.add(training_sample.answer)

            # if report_progress:
            #     progress = int((i * 100.0) / len(training_list))
            #
            #     # if progress > 0:
            #     #     current_time = time.time()
            #     #     # print("PROGRESS:", progress, "% ", "TTC:",
            #     #     #       round((current_time - start_time) * (100 - progress) / progress, 2), "s")

        return True

    def train(self,
              training_list: List[QuestionT],
              testing_list: List[QuestionT]) -> bool:
        """ Reset and train the FAQ classifier with question-answer pairs

        :param training_list: List of questions.
        :param testing_list: List of questions to test accuracy & overfit during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._faq_questions.clear()
        self._faq_labels.clear()

        return self.train_online(training_list, testing_list, True)

    def get_labels(self) -> Optional[List[str]]:
        if len(self._faq_labels) > 0:
            return list(self._faq_labels)
        else:
            return None

    def find_knn_matches(self, input_text: str, lang_code_hint: Optional[str],
                         weak_match_threshold: float,
                         top_n: int) -> Tuple[List[Tuple[float, QuestionT]], str]:
        """ Find the n best matches to the input text.

        :param input_text: The question to look for in the question set.
        :param lang_code_hint: A hint for the language of the input text.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number of sorted matches to return.
        :return: Sorted list of scored questions (score, QuestionT) and the language code of the input.
        """
        if self._manifold_dict is None:
            logging.error("faq_matcher.find_knn_matches - _manifold_dict is None!")
            return [], ""

        if len(self._manifold_dict) == 1:
            # Override the text language code if only one manifold is present.
            input_lang_code = next(iter(self._manifold_dict))
        elif lang_code_hint is not None:
            input_lang_code = lang_code_hint
        else:
            # Fill in the text language code.
            input_lang_code = self._classify_text_language(input_text)

        manifold = self._manifold_dict.get(input_lang_code)

        if manifold is None:
            logging.error("faq_matcher.find_knn_matches - language manifold not found.")
            return [], input_lang_code

        spell_correct = input_lang_code in {"eng", "afr"}

        input_vect = manifold.calc_sentence_vector(input_text, spell_correct)

        # 1) Calc softmax scores over ALL training utterances.
        # ToDo: Consider using hierarchical or fast_approx softmax if large model performance becomes a problem.
        softmax_temp = 1.0 / 5.0  # ToDo: Set this as a model hyper param.
        scored_questions = []  # type: List[Tuple[float, QuestionT]]
        best_match_probs = []  # type: List[Tuple[float, QuestionT]]

        # ToDo: Use more efficient KNN search data structure if many questions used in model!
        #   OR: Use locality sensitive hashing instead!!
        for question in self._faq_questions:
            if input_lang_code in {'afr', 'eng'}:
                # === Use the word embedding language model ...
                if (input_lang_code == question.lang_code) and input_vect.any():
                    # dist = WordManifold.calc_l2_dist(input_vect, question.sent_vect)
                    dist = WordManifold.calc_l1_dist(input_vect, question.sent_vect)

                    score = math.exp(-1.0 * dist / softmax_temp)
                    scored_questions.append((score, question))
            else:
                # === Use common word scoring ...
                # stop_words = {"&", "#", "@", "？", "~", "”", "“", ".", ",", "?", ";", ":", "!", "(", ")",
                #               "{", "}",
                #               "[", "]", '"', "'", "`", "’", "-", "–", "/", "\\", "…"}  # type: Set[str]
                stop_words = set()  # type: Set[str]
                dist = 1.0 - manifold.calc_common_words_sim(input_text,
                                                            question.text,
                                                            stop_words)

                score = math.exp(-1.0 * dist / (softmax_temp / 4.0))  # Adapt temp for common word dist.
                scored_questions.append((score, question))

        num_scored_questions = len(scored_questions)

        if num_scored_questions > 0:
            # 2) Find best matching scored labels.
            scored_questions.sort(key=lambda scored_question: scored_question[0], reverse=True)
            best_match_answer_ids = []  # type: List[int]
            best_match_questions = []  # type: List[Tuple[float, QuestionT]]

            i = 0
            while i < num_scored_questions:
                score, question = scored_questions[i]

                if question.answer_id not in best_match_answer_ids:
                    best_match_answer_ids.append(question.answer_id)
                    best_match_questions.append((score, question))

                i += 1

            softmax_sum = 0.0

            for score, question in best_match_questions:
                softmax_sum += score

            if softmax_sum > 0.0:
                # 3) Calc probabilities and use weak_match_threshold as a probability threshold.
                for score, question in best_match_questions:
                    probability = score / softmax_sum

                    if probability > (1.0 - weak_match_threshold):
                        best_match_probs.append((probability, question))

        return best_match_probs[:min(top_n, len(best_match_probs))], input_lang_code

    def run_tsne(self,
                 n_components: int, perplexity: float, learning_rate: float) -> List[Tuple[str, str, float, float, float]]:

        # print(f"faq_matcher.run_tsne : n_components={n_components} "
        #       f"perplexity={perplexity} learning_rate={learning_rate}")

        tsne_sample_list = []  # List[Tuple[str, str, float, float, float]]

        num_questions = len(self._faq_questions)
        # print(f"faq_matcher.run_tsne : num_questions={num_questions}")

        # Ensure that num components is either 2 or 3.
        if (n_components != 2) and (n_components != 3):
            n_components = 2

        if num_questions > 0:
            tsne = sklearn_manifold.TSNE(n_components=n_components,
                                         init='random',
                                         random_state=None,
                                         perplexity=perplexity,
                                         learning_rate=learning_rate)

            sent_vect_dim = len(self._faq_questions[0].sent_vect)
            # print(f"faq_matcher.run_tsne : sent_vect_dim={sent_vect_dim}")

            expr_x = np.zeros((num_questions, sent_vect_dim))
            # expr_y = np.zeros(num_questions)

            for idx, question in enumerate(self._faq_questions):
                # print(idx, len(expr_x[idx]), len(question.sent_vect), flush=True)
                expr_x[idx] = question.sent_vect
                # expr_y[idx] = question.intent_id

            start_time = time.time()
            print(f"faq_matcher.run_tsne : tsne.fit_transform - Started ...")
            tsne_x = tsne.fit_transform(expr_x)
            end_time = time.time()
            print(f"faq_matcher.run_tsne : tsne.fit_transform - Done in {round(end_time-start_time, 2)} seconds.")

            if n_components == 2:
                for idx, question in enumerate(self._faq_questions):
                    tsne_sample_list.append((question.text, question.answer,
                                             float(tsne_x[idx][0]), float(tsne_x[idx][1]), 0.0))
            elif n_components == 3:
                for idx, question in enumerate(self._faq_questions):
                    tsne_sample_list.append((question.text, question.answer,
                                             float(tsne_x[idx][0]), float(tsne_x[idx][1]), float(tsne_x[idx][2])))

        return tsne_sample_list

    def get_word_manifold_dict(self) -> Optional[Dict[str, WordManifold]]:
        """ Return a reference to the internal word manifold_dict. """
        return self._manifold_dict

    @staticmethod
    def show_stats(question_list: List[QuestionT]):
        group_size_dict = {}  # type: Dict[int, int]

        for q in question_list:
            group_size = group_size_dict.get(q.answer_id)

            if group_size is not None:
                group_size_dict[q.answer_id] = group_size + 1
            else:
                group_size_dict[q.answer_id] = 1

        size_count_dict = {}  # type: Dict[int, int]

        for _, size in group_size_dict.items():
            count = size_count_dict.get(size)

            if count is not None:
                size_count_dict[size] = count + 1
            else:
                size_count_dict[size] = 1

        # print(size_count_dict)

    @staticmethod
    def cnvrt_tuples_to_questions(tuple_list: Union[List[Tuple[str, str, str, str]], List[Tuple[str, str, str]]],
                                  existing_questions: Optional[List[QuestionT]] = None) -> List[QuestionT]:
        """
        Convert a list of question,label,lang_code tuples into a list of QuestionTs USING existing
        model samples to allocate label IDs.

        :param tuple_list: List of data tuples (question,label,lang_code).
        :param existing_questions: List of existing questions.
        :return: List of questions.
        """
        id_set = set()
        label_id_dict = {}  # type: Dict[str, int]
        new_answer_id = 0

        if existing_questions is not None:
            # Setup id_set of existing answer IDs AND label_id_dict map from label to ID.
            for question in existing_questions:
                label_id_dict[question.answer] = question.answer_id
                id_set.add(question.answer_id)
                new_answer_id = max(question.answer_id + 1, new_answer_id)

        # Allocate an answer ID for each new label ACROSS ALL LANGUAGES.
        for sample in tuple_list:
            if label_id_dict.get(sample[1]) is None:
                while new_answer_id in id_set:
                    new_answer_id += 1

                label_id_dict[sample[1]] = new_answer_id
                id_set.add(new_answer_id)
                new_answer_id += 1

        question_list = []  # type: List[QuestionT]

        # Use the answer IDs to build the list of QuestionTs.
        for sample in tuple_list:
            answer_id = label_id_dict[sample[1]]
            question_list.append(QuestionT(sample[0], answer_id, None, sample[1], sample[2]))

        return question_list

    @staticmethod
    def load_faq_data(questions_file_name: str,
                      q2a_map_file_name: str,
                      answers_file_name: str,
                      training_ratio: int,
                      testing_ratio: int,
                      min_group_size: int,
                      delim: str) -> Tuple[List[QuestionT], List[QuestionT]]:
        """ Loads the question data (in quora format) and prepares training and testing sets of questions.

        :param questions_file_name: The quora format questions file.
        :param q2a_map_file_name: The q2a mapping if available. Set to "" if not available.
        :param answers_file_name: The answers file if available. Set to "" if not available.
        :param training_ratio: The number of training questions to use per answer.
        :param testing_ratio: The number of training questions to use per answer.
        :param min_group_size: The minimum sized question groups to use. Set to max training_ratio+testing_ratio to
        consistently have the same training and testing groups.
        :param delim: The column delimeter used in the data file.
        """
        question_dict = {}  # type: Dict[int, QuestionT]
        group_dict = {}  # type: Dict[int, Set[int]]

        q2a_dict = {}  # type: Dict[int, int]
        answer_dict = {}  # type: Dict[int, str]

        # Read the questions file AND group questions marked as similar.
        with open(questions_file_name, newline='') as csvfile:
            last_row_id = "bof"
            new_gid = 0

            csvdoc = csv.reader(csvfile, delimiter=delim, quotechar='"')
            for row in islice(csvdoc, 1, None):
                try:
                    row_id = row[0]
                    last_row_id = row_id

                    q1_id = int(row[1])
                    q1_text = row[3]

                    q2_id = int(row[2])
                    q2_text = row[4]

                    is_same_question = row[5] == "1"

                    q1_gid = -1
                    q2_gid = -1

                    if question_dict.get(q1_id) is not None:
                        # assert(q1 == question_dict[q1_id].text)
                        q1_gid = question_dict[q1_id].answer_id

                    if question_dict.get(q2_id) is not None:
                        # assert(q2 == question_dict[q2_id].text)
                        q2_gid = question_dict[q2_id].answer_id

                    # Update with a connected component analysis.
                    # 1) Update question group IDs and merge groups if required.
                    if is_same_question:
                        if q1_gid == -1 and q2_gid == -1:  # two unseen questions
                            q1_gid = new_gid
                            q2_gid = new_gid
                            new_gid += 1

                        elif q1_gid == -1:  # one unseen question q1
                            q1_gid = q2_gid

                        elif q2_gid == -1:  # one unseen question q2
                            q2_gid = q1_gid

                        else:  # both questions already assigned to groups so merge the two groups.
                            if q1_gid != q2_gid:
                                group_dict[q1_gid].update(group_dict[q2_gid])

                                # change all questions that was in second group to first group.
                                for q_id in group_dict[q2_gid]:
                                    question_dict[q_id] = QuestionT(question_dict[q_id].text,
                                                                    q1_gid,
                                                                    question_dict[q_id].sent_vect,
                                                                    question_dict[q_id].answer,
                                                                    question_dict[q_id].lang_code)

                                group_dict.pop(q2_gid)  # key q2_gid is expected to be in dict.
                                q2_gid = q1_gid
                    else:
                        if q1_gid == -1:  # unseen question
                            q1_gid = new_gid
                            new_gid += 1

                        if q2_gid == -1:  # unseen question
                            q2_gid = new_gid
                            new_gid += 1

                    # 2) Add/re-add questions to question dict and update group_dict.
                    question_dict[q1_id] = QuestionT(q1_text, q1_gid, None, "", "eng")
                    question_dict[q2_id] = QuestionT(q2_text, q2_gid, None, "", "eng")

                    if group_dict.get(q1_gid) is None:
                        group_dict[q1_gid] = set()  # Set[int]

                    if group_dict.get(q2_gid) is None:
                        group_dict[q2_gid] = set()  # Set[int]

                    group_dict[q1_gid].add(q1_id)
                    group_dict[q2_gid].add(q2_id)

                except (IndexError, ValueError):
                    print("Index or Value Error: Last row id was " + str(last_row_id))
                    print(row)
                    return [], []

        # Read q2a file to on output update the questions' self assigned group IDs to the provided answer IDs.
        if q2a_map_file_name != "":
            with open(q2a_map_file_name, newline='') as csvfile:
                csvdoc = csv.reader(csvfile, delimiter=delim, quotechar='"')

                last_qid = 0

                for row in islice(csvdoc, 1, None):
                    try:
                        qid = int(row[0])
                        last_qid = qid

                        answer_id = int(row[1])
                        q2a_dict[qid] = answer_id

                    except (IndexError, ValueError):
                        print("Index or Value Error: Last qid was " + str(last_qid))
                        print(row)
                        return [], []

        # Read answers file.
        if answers_file_name != "":
            with open(answers_file_name, newline='') as csvfile:
                csvdoc = csv.reader(csvfile, delimiter=delim, quotechar='"')

                last_answer_id = 0

                for row in islice(csvdoc, 1, None):
                    try:
                        answer_id = int(row[0])
                        last_answer_id = answer_id

                        answer_dict[answer_id] = row[1]

                    except IndexError:
                        print("Index Error: Last answer_id was " + str(last_answer_id))
                        print(row)
                        return [], []

        # Genescore training and testing lists...
        training_list = []  # type: List[QuestionT]
        testing_list = []  # type: List[QuestionT]

        if training_ratio > 0:
            # Iterate over all groups (i.e. question sets) and append to training_list and testing_list...
            for _, question_set in group_dict.items():
                if len(question_set) >= min_group_size:
                    for qid in islice(question_set, 0, training_ratio):
                        answer_id = question_dict[qid].answer_id

                        # Remap self assigned group ID to the provided answer ID.
                        q2a_answer_id = q2a_dict.get(qid)
                        if q2a_answer_id is not None:
                            answer_id = q2a_answer_id

                        answer_text = answer_dict.get(answer_id)

                        if answer_text is None:
                            answer_text = str(answer_id)

                        training_list.append(
                            QuestionT(question_dict[qid].text, answer_id, question_dict[qid].sent_vect,
                                      answer_text, "eng"))

                    for qid in islice(question_set, training_ratio, training_ratio + testing_ratio):
                        answer_id = question_dict[qid].answer_id

                        # Remap self assigned group ID to the provided answer ID.
                        q2a_answer_id = q2a_dict.get(qid)
                        if q2a_answer_id is not None:
                            answer_id = q2a_answer_id

                        # Add the answer_id as the answer text if no answer text supplied.
                        answer_text = answer_dict.get(answer_id)
                        if answer_text is None:
                            answer_text = str(answer_id)

                        testing_list.append(
                            QuestionT(question_dict[qid].text, answer_id, question_dict[qid].sent_vect,
                                      answer_text, "eng"))
        else:
            # Iterate over all groups (i.e. question sets) and append to training_list...
            for _, question_set in group_dict.items():
                for qid in question_set:  # islice(question_set, 0, 1):
                    answer_id = question_dict[qid].answer_id

                    # Remap self assigned group ID to the provided answer ID.
                    q2a_answer_id = q2a_dict.get(qid)
                    if q2a_answer_id is not None:
                        answer_id = q2a_answer_id

                    # Add the answer_id as the answer text if no answer text supplied.
                    answer_text = answer_dict.get(answer_id)
                    if answer_text is None:
                        answer_text = str(answer_id)

                    training_list.append(QuestionT(question_dict[qid].text, answer_id, question_dict[qid].sent_vect,
                                                   answer_text, "eng"))

        # print("Training list stats - size_vs_count:")
        # FAQMatcher.show_stats(training_list)
        # print()
        #
        # print("Testing list stats - size_vs_count:")
        # FAQMatcher.show_stats(testing_list)
        # print()

        return training_list, testing_list

    @staticmethod
    def load_splitsco_file_r1(file_name: str) -> List[Tuple[str, str, str]]:
        """ Load splits.ai intent file that is part of their NLU benchmark. """
        expression_tuples = []  # type: List[Tuple[str, str, str]]

        with open(file_name) as json_file:
            json_dict = json.load(json_file)

            intent_domains = json_dict.get("domains")
            if intent_domains is not None:
                # print("len(intent_domains) =", len(intent_domains))

                for intent_domain in intent_domains:
                    intents = intent_domain.get("intents")
                    # print("len(intents) =", len(intents))

                    for intent in intents:
                        name = intent.get("name")
                        queries = intent.get("queries")

                        if name is not None and queries is not None:
                            # print("name =", name, "len(queries) =", len(queries))

                            for querie in queries:
                                text = querie.get("text")
                                if text is not None:
                                    # print("expression =", text, "intent_label =", name)
                                    expression_tuples.append((text, name, ""))

        return expression_tuples

    @staticmethod
    def load_splitsco_file_r2(file_name: str) -> List[Tuple[str, str, str]]:
        """ Load splits.ai intent file that is part of their NLU benchmark. """
        expression_tuples = []  # type: List[Tuple[str, str, str]]

        with open(file_name) as json_file:
            json_dict = json.load(json_file)

            for intent_label, expressions in json_dict.items():
                # print("intent_label:", intent_label)

                for expression_json in expressions:
                    expression_snippets = expression_json.get("data")
                    # Each snippet is a dict and has a piece of the expression within 'text' item.

                    if expression_snippets is not None:
                        expression_text = ""

                        for snippet in expression_snippets:
                            snippet_text = snippet.get("text")

                            if snippet_text is not None:
                                expression_text = expression_text + snippet_text

                        if expression_text != "":
                            expression_tuples.append((expression_text, intent_label, ""))

        return expression_tuples
