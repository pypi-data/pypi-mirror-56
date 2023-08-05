"""
Feersum_nlu Emotion Analysis class.
"""

from typing import List, Tuple

from fastai.text import load_learner
import logging


class EmotionAnalyser(object):
    """ Perform emotion analysis on text, categorise into one of four classes"""

    def __init__(self, blob_folder_name, blob_file_name) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        self._classifier = load_learner(blob_folder_name, blob_file_name)

    def classify(self, input_text: str) -> List[Tuple[str, float]]:
        """ classify text as one of four labels

        :param input_text: Input text string to process.
        :return: prediction; list of score labels.
        """

        if self._classifier is None:
            logging.error("emotion_analyser.classify - classifier not loaded!")
            return []

        preds = []  # type: List[Tuple[str, float]]

        clssfr_pred = self._classifier.predict(input_text)
        label = clssfr_pred[0]
        label_idx = clssfr_pred[1]
        label_score = clssfr_pred[2].numpy()[label_idx].item()
        # print('++', input_text, label, label_score)

        preds.append((str(label), label_score))

        return preds

    def classify_list(self, input_samples: List[str]) -> List[List[Tuple[str, float]]]:
        """
        Classify a list of text strings.

        Classify a list of text strings. It doesn't seem as if the model as a bulk process method so call 'classify'.

        :param input_samples: The list of text strings to process.
        :return: The list of predictions. Each prediction is a list of scored labels.
        """
        pred_list = []  # type: List[List[Tuple[str, float]]]

        for sample_text in input_samples:
            pred = self.classify(sample_text)
            pred_list.append(pred)

        return pred_list
