# data handling
import pandas as pd
# utilities
from typing import List, Tuple
import unittest
# feersum functionality
from feersum_nlu.models import emotion_analyser
from feersum_nlu import nlp_engine_data
# NLP libraries
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

from feersum_nlu.models.tests import BaseTestCase


class TestEmotionAnalysis(BaseTestCase):

    def test_emotion_classifier_anger(self):
        print("Testing TestEmotionAnalysis.test_emotion_classifier_anger ...", flush=True)

        blob_folder_name = "emotion_analysis_experiment/pretrained"
        blob_file_name = "export_emo_clas.pkl"
        local_file_cache_path, blob_file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name, blob_file_name)

        classifier = emotion_analyser.EmotionAnalyser(local_file_cache_path, blob_file_name)

        anger_text = " I am indignant and outraged!,I cannot believe what just happened"
        pred = classifier.classify(anger_text)

        self.assertEqual(pred[0][0], 'anger')

    def test_emotion_classifier_fear(self):
        print("Testing TestEmotionAnalysis.test_emotion_classifier_fear ...", flush=True)

        blob_folder_name = "emotion_analysis_experiment/pretrained"
        blob_file_name = "export_emo_clas.pkl"
        local_file_cache_path, blob_file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name, blob_file_name)

        classifier = emotion_analyser.EmotionAnalyser(local_file_cache_path, blob_file_name)

        fear_text = "A sight, sound & smell to behold in person, still gives me the creeps to think about. #shudder"
        pred = classifier.classify(fear_text)
        self.assertEqual(pred[0][0], 'fear')

    def test_emotion_classifier_joy(self):
        print("Testing TestEmotionAnalysis.test_emotion_classifier_joy ...", flush=True)

        blob_folder_name = "emotion_analysis_experiment/pretrained"
        blob_file_name = "export_emo_clas.pkl"
        local_file_cache_path, blob_file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name, blob_file_name)

        classifier = emotion_analyser.EmotionAnalyser(local_file_cache_path, blob_file_name)

        joy_text = "I'm so happy about all the love and good vibes I got today"
        pred = classifier.classify(joy_text)
        self.assertEqual(pred[0][0], 'joy')

    def test_emotion_classifier_sadness(self):
        print("Testing TestEmotionAnalysis.test_emotion_classifier_sadness ...", flush=True)

        blob_folder_name = "emotion_analysis_experiment/pretrained"
        blob_file_name = "export_emo_clas.pkl"
        local_file_cache_path, blob_file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name, blob_file_name)

        classifier = emotion_analyser.EmotionAnalyser(local_file_cache_path, blob_file_name)

        sad_text = "Should've stayed at school cause ain't nobody here,sadness"
        pred = classifier.classify(sad_text)
        self.assertEqual(pred[0][0], 'sadness')

    def test_classifier_performance(self):
        print("Testing TestEmotionAnalysis.test_classifier_accuracy ...", flush=True)

        blob_folder_name = "emotion_analysis_experiment/pretrained"
        blob_file_name = "export_emo_clas.pkl"
        local_file_cache_path, blob_file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name, blob_file_name)

        classifier = emotion_analyser.EmotionAnalyser(local_file_cache_path, blob_file_name)

        df = pd.read_csv(nlp_engine_data.get_path() + '/emotion_analysis_sample_data.csv')

        # Type cast as str from type Category
        pred_list = classifier.classify_list(df['content'])  # type: List[List[Tuple[str, float]]]
        pred_label_list = [pred[0][0] for pred in pred_list]  # type: List[str]

        df['pred_label'] = pred_label_list

        accuracy = accuracy_score(y_true=df['label'], y_pred=pred_label_list)
        macro_f1 = f1_score(y_true=df['label'], y_pred=pred_label_list, average='macro')
        micro_f1 = f1_score(y_true=df['label'], y_pred=pred_label_list, average='micro')

        labels = ['anger', 'fear', 'joy', 'sadness']  # Matches the label order in the model!

        f1_per_label = f1_score(y_true=df['label'],
                                y_pred=pred_label_list,
                                average=None,
                                labels=labels)

        print(f"accuracy = {accuracy}")
        print(f"macro_f1 = {macro_f1}")
        print(f"micro_f1 = {micro_f1}")
        print()
        self.assertGreaterEqual(accuracy, 0.95)
        self.assertGreaterEqual(macro_f1, 0.95)
        self.assertGreaterEqual(micro_f1, 0.95)

        anger_f1 = f1_per_label[0]
        fear_f1 = f1_per_label[1]
        joy_f1 = f1_per_label[2]
        sadness_f1 = f1_per_label[3]

        print(f"anger_f1 = {anger_f1}")
        print(f"fear_f1 = {fear_f1}")
        print(f"joy_f1 = {joy_f1}")
        print(f"sadness_f1 = {sadness_f1}")
        print()
        self.assertGreaterEqual(anger_f1, 0.96)
        self.assertGreaterEqual(fear_f1, 0.95)
        self.assertGreaterEqual(joy_f1, 0.98)
        self.assertGreaterEqual(sadness_f1, 0.91)


if __name__ == '__main__':
    unittest.main()
