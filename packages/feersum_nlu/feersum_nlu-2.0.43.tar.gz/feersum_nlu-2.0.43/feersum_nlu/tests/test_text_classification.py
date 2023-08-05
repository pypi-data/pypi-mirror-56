import time
import unittest

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestTextClassification(BaseTestCase):
    def test_accuracy(self):
        print("Testing TestTextClassification.test_accuracy.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)
        end_time = time.time()

        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        local_file_cache_path, blob_file_name = \
            nlp_engine_data.get_blob_from_gcp_bucket('glove_and_fasttext_ref', "glove.6B.50d.trimmed.txt")
        manifold_model_path = f"{local_file_cache_path}/{blob_file_name}"

        print("Creating the word manifold...", flush=True)
        nlpe.create_word_manifold_encoder("glove6B50D_trimmed",
                                          manifold_model_path,
                                          stop_words=set(),
                                          spacies=["&", "#", "@", "？", "~", "”", "“", ".", ",", "?", ";", ":", "!", "(", ")",
                                                   "{", "}",
                                                   "[", "]", '"', "'", "`", "’", "-", "–", "/", "\\", "…"])
        print("done.", flush=True)

        print("Training & testing...", flush=True)
        phrase_topic_list = [("hallo", "greeting", ""),
                             ("hello", "greeting", ""),
                             ("hi", "greeting", ""),
                             ("good day", "greeting", ""),
                             ("morning", "greeting", ""),
                             ("afternoon", "greeting", ""),
                             ("decoder error", "fault_report", ""),
                             ("dstv error", "fault_report", ""),
                             ("tv error", "fault_report", ""),
                             ("sound error", "fault_report", "")]

        nlpe.train_text_clsfr('test_text_classification',
                              phrase_topic_list,
                              phrase_topic_list,
                              "nearest_neighbour_l1",
                              {"eng": "glove6B50D_trimmed"})

        # nlpe.save_text_clsfr("test_text_classification")
        # nlpe.purge_text_clsfr("test_text_classification")
        # nlpe.load_text_clsfr("test_text_classification")

        accuracy, f1, cm, cm_labels = nlpe.test_text_clsfr('test_text_classification',
                                                           phrase_topic_list,
                                                           1.0,
                                                           1)
        print("done.", flush=True)

        ret1 = nlpe.retrieve_text_class('test_text_classification', "Hi, how are you?", None, 1.0, 2)
        ret2 = nlpe.retrieve_text_class('test_text_classification', "I get an error code.", None, 1.0, 2)

        end_time = time.time()
        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        print("accuracy = ", accuracy)
        print("ret1[0][0][0] = ", ret1[0][0][0])
        print("ret2[0][0][0] = ", ret2[0][0][0])

        # Test small training set accuracy and some samples.
        self.assertTrue(accuracy > 0.9)
        self.assertTrue(ret1[0][0][0] == "greeting")
        self.assertTrue(ret2[0][0][0] == "fault_report")

        # === Do some tests to make sure the below code doesn't throw exceptions ===
        text_clsfr = nlpe.get_text_classifier("test_text_classification")

        if text_clsfr is not None:
            ts = text_clsfr.run_tsne(n_components=2, perplexity=30, learning_rate=200)
            # print(ts)
            # [
            # ]
            self.assertTrue(ts[0][4] == 0.0)
            self.assertTrue(len(ts) == 10)
        # === ===


#         self.assertTrue(nlpe.purge_text_clsfr("test_text_classification"))


if __name__ == '__main__':
    unittest.main()
