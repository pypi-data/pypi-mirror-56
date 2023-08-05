"""
Feersum_nlu Synonym Extractor.
"""

from typing import Tuple, List, Optional, Dict, Set, Any  # noqa # pylint: disable=unused-import
import re
import logging


class SynonymEntity(object):
    def __init__(self,
                 _entity: str,
                 _ignore_word_boundaries: Optional[bool],
                 _ignore_case: Optional[bool],
                 _value: Optional[str],
                 _index: Optional[int],
                 _len: Optional[int],
                 _syn_set: Optional[List[str]]):  # Either has a _syn_set OR a single entity synonym value @ (ent,index,len).
        self.entity = _entity
        self.ignore_word_boundaries = _ignore_word_boundaries
        self.ignore_case = _ignore_case
        self.value = _value
        self.index = _index
        self.len = _len
        self.syn_set = _syn_set

    def __repr__(self) -> str:
        return f"{self.entity} {self.ignore_word_boundaries} {self.ignore_case} " \
               f"{self.value} {self.index} {self.len} {self.syn_set}"

    def __str__(self) -> str:
        return f"{self.entity} {self.ignore_word_boundaries} {self.ignore_case} " \
               f"{self.value} {self.index} {self.len} {self.syn_set}"


class SynonymSample(object):
    def __init__(self,
                 _text: Optional[str],
                 _entity_list: List[SynonymEntity]) -> None:
        self.text = _text
        self.entity_list = _entity_list


class SynonymExtractor(object):
    """
    Feersum_nlu SynonymExtractor class.
    """

    def __init__(self) -> None:
        self.uuid = ""  # Unique version identifier.

        # Map of entity class to list of synonyms.
        self._entity_syn_set_map = {}  # type: Dict[str, List[str]]
        self._entity_ignore_word_boundaries_map = {}  # type: Dict[str, bool]
        self._entity_ignore_case_map = {}  # type: Dict[str, bool]

        self._pattern_obj_cache_ignore_case = {}  # type: Dict[str, Any]
        self._pattern_obj_cache_honour_case = {}  # type: Dict[str, Any]

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        # Add the attributes to the model that may not exist yet.
        if not hasattr(self, '_entity_ignore_word_boundaries_map'):
            self._entity_ignore_word_boundaries_map = {}
        if not hasattr(self, '_entity_ignore_case_map'):
            self._entity_ignore_case_map = {}
        if not hasattr(self, '_pattern_obj_cache_ignore_case'):
            self._pattern_obj_cache_ignore_case = {}
        if not hasattr(self, '_pattern_obj_cache_honour_case'):
            self._pattern_obj_cache_honour_case = {}

    @staticmethod
    def cnvrt_json_to_synonym_samples(json_samples: List[Dict]) -> List[SynonymSample]:
        """
        Convert json samples to Synonym samples.

        :param json_samples: [{'text': '...', 'entity_list': [{'index': 0, 'len': 1, 'entity': 'object'}]
        :return: List of Synonym samples.
        """
        synonym_samples = []  # type: List[SynonymSample]

        for json_sample in json_samples:
            json_text = json_sample.get('text')
            json_entity_list = json_sample.get('entity_list')

            has_text = True if isinstance(json_text, str) else False

            if isinstance(json_entity_list, list):
                valid_entity_list = []  # type: List[SynonymEntity]

                for json_entity in json_entity_list:
                    if isinstance(json_entity, dict):
                        entity = json_entity.get('entity')
                        ignore_word_boundaries = json_entity.get('ignore_word_boundaries')
                        ignore_case = json_entity.get('ignore_case')

                        if isinstance(entity, str):
                            syn_set = json_entity.get('syn_set')

                            if isinstance(syn_set, list):
                                # The entity has a syn_set which can be used directly to train possible synonyms.
                                valid_entity_list.append(SynonymEntity(_entity=entity,
                                                                       _ignore_word_boundaries=ignore_word_boundaries,
                                                                       _ignore_case=ignore_case,
                                                                       _value=None,
                                                                       _index=None, _len=None,
                                                                       _syn_set=syn_set))
                            elif has_text:
                                # The sample has a text utterance so entities can be specified as (entity,index,len)
                                index = json_entity.get('index')
                                entity_len = json_entity.get('len')

                                if isinstance(index, int) and isinstance(entity_len, int):
                                    valid_entity_list.append(SynonymEntity(_entity=entity,
                                                                           _ignore_word_boundaries=ignore_word_boundaries,
                                                                           _ignore_case=ignore_case,
                                                                           _value=None,
                                                                           _index=index, _len=entity_len,
                                                                           _syn_set=None))

                if len(valid_entity_list) > 0:
                    synonym_samples.append(SynonymSample(_text=json_text, _entity_list=valid_entity_list))

        return synonym_samples

    def train(self,
              training_samples: List[SynonymSample],
              testing_samples: List[SynonymSample]) -> bool:
        """ Reset and train the Synonym extractor with word labelled docs.

        :param training_samples: List of training samples.
        :param testing_samples: List of testing samples to test accuracy & overfit during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._entity_syn_set_map.clear()

        self._pattern_obj_cache_ignore_case.clear()
        self._pattern_obj_cache_honour_case.clear()

        training_successful = True

        # Iterate over all entities in ALL training samples.
        for training_sample in training_samples:
            for training_entity in training_sample.entity_list:
                entity_syn_set: Set[str]

                # If entity already exists in model then start syn_set with what is currently in model.
                entity_syn_set = set(self._entity_syn_set_map.get(training_entity.entity, []))

                # Add new synonyms from current training_entity:
                if training_entity.syn_set is not None:
                    # training entity has a list of synonyms.
                    syn_value_set = training_entity.syn_set

                    for syn_value in syn_value_set:
                        try:
                            re.compile(syn_value)
                            is_valid_regex = True
                        except re.error as e:
                            is_valid_regex = False
                            training_successful = False
                            logging.error(f"models.synonym_extractor.train: syn_value {syn_value} "
                                          f"resulted in re.error: {e}!")

                        if is_valid_regex:
                            entity_syn_set.add(syn_value)
                else:
                    # training_entity contains a single example reference of the entity in the text to add to entity's synset
                    if training_entity.index is not None and training_entity.len is not None and \
                            training_sample.text is not None and \
                            (training_entity.index + training_entity.len) <= len(training_sample.text):
                        syn_value = training_sample.text[training_entity.index: training_entity.index + training_entity.len]
                        entity_syn_set.add(re.escape(syn_value))

                # Update the model.
                self._entity_syn_set_map[training_entity.entity] = list(entity_syn_set)

                # Update ignore_word_boundaries if provided in sample.
                if training_entity.ignore_word_boundaries is not None:
                    self._entity_ignore_word_boundaries_map[training_entity.entity] = training_entity.ignore_word_boundaries

                # Update ignore_case if provided in sample.
                if training_entity.ignore_case is not None:
                    self._entity_ignore_case_map[training_entity.entity] = training_entity.ignore_case

        return training_successful

    def get_labels(self) -> Optional[List[str]]:
        labels = []  # type: List[str]

        for entity in self._entity_syn_set_map:
            labels.append(entity)

        return labels

    def predict(self, input_text: str, lang_code_hint: Optional[str]) -> Tuple[List[SynonymEntity], Optional[str]]:
        """
        Predict which entities are present in the text.

        :param input_text: The text to extract entities from.
        :param lang_code_hint: The language of the input_text.
        :return: List of extracted entities i.e. List[SynonymEntity]
        """
        result_list = []  # type: List[SynonymEntity]

        for entity, syn_value_set in self._entity_syn_set_map.items():
            ignore_word_boundaries = self._entity_ignore_word_boundaries_map.get(entity, False)
            ignore_case = self._entity_ignore_case_map.get(entity, True)

            for syn_value in syn_value_set:
                try:
                    if ignore_word_boundaries:
                        pattern = r'({0})'.format(syn_value)
                    else:
                        pattern = r'\b({0})\b'.format(syn_value)

                    if ignore_case:
                        pattern_obj = self._pattern_obj_cache_ignore_case.get(pattern)
                        if pattern_obj is None:
                            pattern_obj = re.compile(pattern, flags=re.IGNORECASE)
                            self._pattern_obj_cache_ignore_case[pattern] = pattern_obj
                    else:
                        pattern_obj = self._pattern_obj_cache_honour_case.get(pattern)
                        if pattern_obj is None:
                            pattern_obj = re.compile(pattern)
                            self._pattern_obj_cache_honour_case[pattern] = pattern_obj

                    match = pattern_obj.search(input_text)
                    # ToDo: what about multiple matches?

                    if match:
                        match_span = match.span()

                        match_index = match_span[0]
                        match_len = len(syn_value)
                        match_already_recorded = False

                        # Only keep the first match of each entity for EXACTLY matching spans.
                        for result in result_list:
                            if (result.entity == entity) and (result.index == match_index) and (result.len == match_len):
                                match_already_recorded = True

                        if not match_already_recorded:
                            result_list.append(SynonymEntity(_entity=entity,
                                                             _value=syn_value,
                                                             _index=match_index, _len=match_len,
                                                             _ignore_word_boundaries=None,
                                                             _ignore_case=None,
                                                             _syn_set=None))
                except re.error as e:
                    # Ignore all syn values that are not valid regular expressions.
                    # These should all be caught during training.
                    logging.error(f"models.synonym_extractor.predict: re.error: {e}!")
                    pass

        return result_list, lang_code_hint
