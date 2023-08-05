import time
import unittest

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestFAQs(BaseTestCase):
    def test_accuracy(self):
        print("Testing TestFAQs.test_accuracy.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)
        end_time = time.time()
        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        # ============================
        # === Create Word Manifold ===
        print("Creating the word manifold...", flush=True)
        start_time = time.time()
        # nlpe.create_word_manifold_encoder("glove6B50D_trimmed",
        #                                   nlp_engine_data.get_path() + "/glove.6B.50d.trimmed.txt",
        #                                   stop_words=set(),
        #                                   spacies=["&", "#", "@", "？", "~", "”", "“", ".", ",",
        #                                            "?", ";", ":", "!", "(", ")",
        #                                            "{", "}",
        #                                            "[", "]", '"', "'", "`", "’", "-", "–", "/", "\\", "…"])
        nlpe.create_feers_language_model("glove6B50D_trimmed")

        print("Adding some words...", flush=True)
        manifold = nlpe.get_language_model("glove6B50D_trimmed")

        if manifold is not None:
            manifold.add_word_similar_to("bot", "robot")
            manifold.add_word_similar_to("chatbot", "robot")
            manifold.add_word_similar_to("feersum", "robot")
            manifold.add_word_similar_to("botcon", "conference")
            manifold.add_word_similar_to("praekelt", "amazon")

        #     print("Saving, purging and loading again...", flush=True)
        #         nlpe.save_word_manifold("glove6B50D_trimmed")
        #         nlpe.purge_word_manifold("glove6B50D_trimmed")
        #         nlpe.load_word_manifold("glove6B50D_trimmed")

        end_time = time.time()

        print('create word manifold time = ' + str(end_time - start_time) + 's.', flush=True)
        print()

        manifold = nlpe.get_language_model("glove6B50D_trimmed")

        self.assertTrue(manifold is not None)
        # === ===

        # ==========================
        # === Create FAQ Matcher ===
        print("==========================")
        print("Creating FAQ matcher...", flush=True)
        start_time = time.time()
        training_list_all, testing_list_all = nlpe.load_faq_matcher_data(
            nlp_engine_data.get_path() + "/quora_duplicate_questions.tsv", "", "",
            4, 2,
            10, "\t")

        training_list_offline = training_list_all[:int(len(training_list_all) / 2)]
        training_list_online = training_list_all[int(len(training_list_all) / 2):]

        print("len(training_list_offline) =", len(training_list_offline), flush=True)
        print("len(training_list_online) =", len(training_list_online), flush=True)

        # Provide some training data up front.
        nlpe.train_faq_matcher("exampleFAQ",
                               training_list_offline,
                               [],
                               word_manifold_name_dict={"eng": "glove6B50D_trimmed"})

        # Online train with the rest of the training data.
        nlpe.train_faq_matcher_online("exampleFAQ",
                                      training_list_online,
                                      [])

        end_time = time.time()

        print('  Create time = ' + str(end_time - start_time) + 's.', flush=True)
        print()

        print("  Testing accuracy...", flush=True)
        start_time = time.time()
        accuracy, f1, confusion_dict, confusion_dict_labels = nlpe.test_faq_matcher("exampleFAQ",
                                                                                    testing_list_all,
                                                                                    1.0,
                                                                                    1)
        end_time = time.time()
        print("  accuracy = " + str(accuracy), flush=True)
        print()
        print('  testing time = ' + str(end_time - start_time) + 's.', flush=True)
        print()

        self.assertTrue(accuracy >= 0.75)

        #         print(nlpe.save_faq_matcher("exampleFAQ"), flush=True)
        #         print(nlpe.purge_faq_matcher("exampleFAQ"), flush=True)
        #         print(nlpe.load_faq_matcher("exampleFAQ", {"eng": "glove6B50D_trimmed"}), flush=True)

        print(nlpe.retrieve_faqs('exampleFAQ', "Why is the sky blue?", None, 0.95, 3), flush=True)
        # === ===

        # === Do some tests to make sure the below code doesn't throw exceptions ===
        faq_matcher = nlpe.get_faq_matcher("exampleFAQ")

        if faq_matcher is not None:
            # nlp_engine.FAQMatcher.show_stats(faq_matcher.get_model_questions())

            ts = faq_matcher.run_tsne(n_components=2, perplexity=30, learning_rate=200)
            # print(ts, flush=True)
            # [
            # ]
            self.assertTrue(ts[0][4] == 0.0)
            self.assertTrue(len(ts) == 2044)
        # === ===

        labels = nlpe.get_faq_matcher_labels("exampleFAQ")

        self.assertTrue(labels is not None)

        if labels is not None:
            print('labels =', labels)
            self.assertTrue('3620' in labels)
            self.assertTrue('1384' in labels)
            self.assertTrue('3620' in labels)
            self.assertTrue('79548' in labels)


#         self.assertTrue(nlpe.purge_faq_matcher("exampleFAQ"))
#         self.assertTrue(nlpe.purge_word_manifold("glove6B50D_trimmed"))


if __name__ == '__main__':
    unittest.main()
