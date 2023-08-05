"""
Feersum_nlu CRF Extractor.
"""

from typing import Tuple, List, Set, Optional, Dict, Any  # noqa # pylint: disable=unused-import
import logging
import nltk

import sklearn_crfsuite
# from sklearn_crfsuite import scorers
# from sklearn_crfsuite import metrics


class CRFEntity(object):
    def __init__(self,
                 _entity: str,
                 _value: Optional[str],
                 _index: int,
                 _len: int):
        self.entity = _entity
        self.value = _value
        self.index = _index
        self.len = _len

    def __repr__(self) -> str:
        return f"{self.entity} {self.value} {self.index} {self.len}"

    def __str__(self) -> str:
        return f"{self.entity} {self.value} {self.index} {self.len}"


class CRFSample(object):
    def __init__(self,
                 _text: str,
                 _entity_list: List[CRFEntity]) -> None:
        self.text = _text
        self.entity_list = _entity_list


class CRFExtractor(object):
    """
    Feersum_nlu CRFExtractor class.
    """

    def __init__(self) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.

        self._tagger = None

    @staticmethod
    def cnvrt_json_to_crf_entity_list(json_entity_list: List[Dict]) -> List[CRFEntity]:
        """
        Convert json entity list to CRF entity list.

        :param json_entity_list: [{'index': 0, 'len': 1, 'entity': 'object'}, ...]
        :return: List of CRF entities.
        """
        valid_entity_list = []  # type: List[CRFEntity]

        for json_entity in json_entity_list:
            if isinstance(json_entity, dict):
                index = json_entity.get('index')
                entity_len = json_entity.get('len')
                entity = json_entity.get('entity')

                if isinstance(index, int) and isinstance(entity_len, int) and \
                        isinstance(entity, str):
                    valid_entity_list.append(CRFEntity(_entity=entity, _value=None, _index=index, _len=entity_len))

        return valid_entity_list

    @staticmethod
    def cnvrt_json_to_crf_samples(json_samples: List[Dict]) -> List[CRFSample]:
        """
        Convert json samples to CRF samples.

        :param json_samples: [{'text': '...', 'entity_list': [{'index': 0, 'len': 1, 'entity': 'object'}, ...]
        :return: List of CRF samples.
        """
        crf_samples = []  # type: List[CRFSample]

        for json_sample in json_samples:
            json_text = json_sample.get('text')
            json_entity_list = json_sample.get('entity_list')

            if isinstance(json_text, str) and isinstance(json_entity_list, list):
                valid_entity_list = CRFExtractor.cnvrt_json_to_crf_entity_list(json_entity_list)

                if len(valid_entity_list) > 0:
                    crf_samples.append(CRFSample(_text=json_text, _entity_list=valid_entity_list))

        return crf_samples

    @staticmethod
    def score_prediction(pred_entity_list: List[CRFEntity],
                         true_entity_list: List[CRFEntity],
                         text) -> float:
        """
        Score a single CRF prediction sample.

        :param pred_entity_list: The list of predicted entities with values
        :param true_entity_list: The actual/true list entities.
        :param text: The true sample's text to get the true entity values from.
        :return: The accuracy of the CRF prediction; acc = entity_found_count / entity_total_count.
        """
        entity_found_count = 0
        entity_total_count = 0

        for entity in true_entity_list:
            entity_value = text[entity.index: entity.index+entity.len]

            # Find the entity amongst the predicted entities.
            for pred_entity in pred_entity_list:
                if (entity.entity == pred_entity.entity) and (entity_value == pred_entity.value):
                    # Found!
                    entity_found_count += 1
                    break

            entity_total_count += 1

        return entity_found_count / entity_total_count

    @staticmethod
    def clean_text(input_text: str) -> str:
        """ Clean text by replacing unwanted characters with spaces. Don't change string indices of words! """
        # ToDo: replace punctuation with spaces?
        return input_text

    @staticmethod
    def _calc_word_features(pos_tagged_tokens: List[Tuple[str, str]], i) -> Dict[str, Any]:
        word = pos_tagged_tokens[i][0]
        pos_tag = pos_tagged_tokens[i][1]

        features = {
            'bias': 1.0,
            'word.lower': word.lower(),
            'word[-3:]': word[-3:],  # 3-suffix
            'word[-2:]': word[-2:],  # 2-suffix
            'word.isupper': word.isupper(),
            'word.istitle': word.istitle(),
            'word.isdigit': word.isdigit(),
            'postag': pos_tag,
            'postag[:2]': pos_tag[:2]  # major part of tag (UPenn)
        }

        if i > 0:
            word = pos_tagged_tokens[i - 1][0]
            postag = pos_tagged_tokens[i - 1][1]
            features.update({
                '-1:word.lower': word.lower(),
                '-1:word.istitle': word.istitle(),
                '-1:word.isupper': word.isupper(),
                '-1:postag': postag,
                '-1:postag[:2]': postag[:2]  # major part of tag (UPenn)
            })
        else:
            features['BOS'] = True

        if i < len(pos_tagged_tokens) - 1:
            word = pos_tagged_tokens[i + 1][0]
            postag = pos_tagged_tokens[i + 1][1]
            features.update({
                '+1:word.lower': word.lower(),
                '+1:word.istitle': word.istitle(),
                '+1:word.isupper': word.isupper(),
                '+1:postag': postag,
                '+1:postag[:2]': postag[:2]  # major part of tag (UPenn)
            })
        else:
            features['EOS'] = True

        return features

    @staticmethod
    def prepare_data(samples: List[CRFSample]) -> Tuple[List, List]:
        # Prepare training data.
        x = []
        y = []

        for sample in samples:
            text = CRFExtractor.clean_text(sample.text)
            tokens = nltk.word_tokenize(text)

            tokens_start_end = []  # type: List[Tuple[int, int]]
            labels = []  # type: List[str]

            find_base = 0

            for token in tokens:
                # 1) Find the start and end indices of the token.
                token_start = text.find(token, find_base)
                token_end = token_start + len(token)
                find_base = token_end

                tokens_start_end.append((token_start, token_end))

                # 2) Find the first entity that includes the token.
                for entity in sample.entity_list:
                    entity_start = entity.index
                    entity_end = entity_start + entity.len

                    if (token_end > entity_start) and (token_start < entity_end):
                        labels.append(entity.entity)
                        break  # from for loop.
                else:
                    labels.append('_')

            features = []
            tagged_tokens = nltk.pos_tag(tokens)

            for idx, (token, tag) in enumerate(tagged_tokens):
                if token != tokens[idx]:
                    logging.error("models.crf_extractor.predict: token tags misaligned with tokens!")
                features.append(CRFExtractor._calc_word_features(tagged_tokens, idx))

            x.append(features)
            y.append(labels)

        return x, y

    def train(self,
              training_samples: List[CRFSample],
              testing_samples: List[CRFSample]) -> bool:
        """ Reset and train the CRF extractor with word labelled docs.

        :param training_samples: List of training samples.
        :param testing_samples: List of testing samples to test accuracy & overfit during training.
        :return: Boolean indicating whether or not the training was successful.
        """
        if len(training_samples) > 0:
            x_train, y_train = CRFExtractor.prepare_data(training_samples)
            x_test, y_test = CRFExtractor.prepare_data(testing_samples)

            # Train the CRF model - https://github.com/TeamHG-Memex/sklearn-crfsuite/blob/master/docs/CoNLL2002.ipynb
            crf = sklearn_crfsuite.CRF(
                algorithm='lbfgs',
                c1=0.1,
                c2=0.1,
                max_iterations=100,
                all_possible_transitions=True
            )

            crf.fit(x_train, y_train)

            # y_pred = crf.predict(x_test)
            # labels = list(crf.classes_)
            # labels.remove('_')
            # print(metrics.flat_classification_report(y_test, y_pred, labels=labels, digits=3))

            self._tagger = crf

            return True
        else:
            return False

    def get_labels(self) -> Optional[List[str]]:
        if self._tagger is not None:
            labels = list(self._tagger.classes_)
            labels.remove('_')
            return labels
        else:
            return None

    def predict(self, input_text: str, lang_code_hint: Optional[str]) -> Tuple[List[CRFEntity], Optional[str]]:
        """
        Predict which entities are present in the text.

        :param input_text: The text to extract entities from.
        :param lang_code_hint: The language of the input_text.
        :return: List of extracted entities i.e. List[CRFEntity]
        """

        input_text = self.clean_text(input_text)
        tokens = nltk.word_tokenize(input_text)  # type: List[str]

        # == Find the token start indices and lengths for use later ==
        token_indices = []
        token_lengths = []
        search_index = 0

        for token in tokens:
            token_index = input_text.find(token, search_index)
            token_len = len(token)
            search_index = token_index + token_len
            token_indices.append(token_index)
            token_lengths.append(token_len)
        # == ==

        tagged_tokens = nltk.pos_tag(tokens)
        features = []

        for idx, (token, tag) in enumerate(tagged_tokens):
            if token != tokens[idx]:
                logging.error("models.crf_extractor.predict: token tags misaligned with tokens!")
            features.append(CRFExtractor._calc_word_features(tagged_tokens, idx))

        x_test = [features]

        if self._tagger is not None:
            y_test = self._tagger.predict(x_test)
            extracted_entities = []  # type: List[CRFEntity]

            for idx, label in enumerate(y_test[0]):  # y_test[0] is prediction for input at x_test[0]
                if label != "_":
                    if (len(extracted_entities) > 0) and (label == extracted_entities[-1].entity):
                        # Update/fuse the last extracted entity to include more tokens.
                        existing_entity = extracted_entities[-1]

                        index = existing_entity.index
                        length = (token_indices[idx] - existing_entity.index) + token_lengths[idx]

                        extracted_entities[-1] = \
                            CRFEntity(_entity=existing_entity.entity,
                                      _value=input_text[index:(index+length)],
                                      _index=index,
                                      _len=length)
                    else:
                        # Add the entity to the list of extracted entities.
                        index = token_indices[idx]
                        length = token_lengths[idx]

                        extracted_entities.append(CRFEntity(_entity=label,
                                                            _value=input_text[index:(index+length)],
                                                            _index=index,
                                                            _len=length))

                    # entity 'value' = tokens[idx]

            return extracted_entities, lang_code_hint
        else:
            return [], None
