import unittest
import time
import json

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestIntentClsfr(BaseTestCase):
    def test_accuracy(self):
        print("Testing TestIntentClsfr.test_accuracy.", flush=True)

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

        #      print("Saving, purging and loading again...", flush=True)
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
        # === Create Intent Classifier ===
        print("==========================")
        print("Creating Intent Classifier...", flush=True)
        start_time = time.time()

        # (expression, label, lang_code) tuples
        training_tuples = [
            ('help me.', 'help', ''),
            ('Can I get some help.', 'help', ''),
            ('Help would be good', 'help', ''),

            ('Can I get a quote please?', 'quote', ''),
            ("Give me a quote please.", 'quote', ''),
            ('I need a quote.', 'quote', ''),

            ('Can I go to the menu?', 'menu', ''),
            ("Take me to the menu.", 'menu', ''),
            ("I would like to go to the menu.", 'menu', ''),
        ]
        testing_tuples = [
            ('I need help.', 'help', ''),
            ("How can I get a quote?", 'quote', ''),
            ('Menu please.', 'menu', ''),
        ]

        intent_tuples = training_tuples + testing_tuples
        intent_expressions = nlpe.cnvrt_intent_tuples_to_expressions(intent_tuples)

        training_expressions = intent_expressions[:len(training_tuples)]
        testing_expressions = intent_expressions[len(training_tuples):]

        # training_expressions_offline = training_expressions[:int(len(training_expressions) / 2)]
        # training_expressions_online = training_expressions[int(len(training_expressions) / 2):]

        print("  len(training_expressions) =", len(training_expressions), flush=True)
        print("  len(testing_expressions) =", len(testing_expressions), flush=True)

        weak_match_threshold = 2.0

        # Provide some training data up front.
        # nlpe.train_intent_clsfr("exampleIntentClsfr",
        #                         # training_expressions_offline,
        #                         training_expressions,
        #                         [],
        #                         word_manifold_name_dict={"eng": "glove6B50D_trimmed"})

        validation_accuracy, validation_f1, validation_confusion_dict, validation_confusion_dict_labels = \
            nlpe.train_and_cross_validate_intent_clsfr("exampleIntentClsfr",
                                                       # training_expressions_offline,
                                                       training_expressions,
                                                       [],
                                                       word_manifold_name_dict={"eng": "glove6B50D_trimmed"},
                                                       weak_match_threshold=weak_match_threshold,
                                                       k=5, n_experiments=30)

        # Online train with the rest of the training data.
        # nlpe.train_intent_clsfr_online("exampleIntentClsfr",
        #                                training_expressions_online,
        #                                [])

        end_time = time.time()

        print('  Create time = ' + str(end_time - start_time) + 's.', flush=True)
        print()

        print("  validation_accuracy = " + str(validation_accuracy), flush=True)
        print()
        print(json.dumps(validation_confusion_dict, indent=4))
        print()

        self.assertTrue(validation_accuracy == 1.0)

        print("  Retrieve - ", flush=True)
        print(nlpe.retrieve_intents("exampleIntentClsfr",
                                    "Hi", None,
                                    weak_match_threshold,
                                    3))
        print()

        print("================")
        print("Testing accuracy...", flush=True)
        start_time = time.time()
        test_accuracy, test_f1, test_confusion_dict, test_confusion_dict_labels = \
            nlpe.test_intent_clsfr("exampleIntentClsfr",
                                   testing_expressions,
                                   0.99,
                                   1)
        end_time = time.time()

        print("  test_accuracy = " + str(test_accuracy), flush=True)
        print()
        # print(json.dumps(test_confusion_dict, indent=4))
        # print()
        print('  testing time = ' + str(end_time - start_time) + 's.', flush=True)
        print()

        self.assertTrue(test_accuracy == 1.0)

        #         print(nlpe.save_intent_clsfr("exampleIntentClsfr"), flush=True)
        #         print(nlpe.purge_intent_clsfr("exampleIntentClsfr"), flush=True)
        #         print(nlpe.load_intent_clsfr("exampleIntentClsfr", {"eng": "glove6B50D_trimmed"}), flush=True)

        print("  Retrieve - ", flush=True)
        print(nlpe.retrieve_intents('exampleIntentClsfr', "Help!", None, 0.95, 3), flush=True)
        # === ===

        # === Do some tests to make sure the below code doesn't throw exceptions ===
        intent_clsfr = nlpe.get_intent_classifier("exampleIntentClsfr")

        if intent_clsfr is not None:
            nlp_engine.IntentClassifier.show_stats(intent_clsfr.get_model_expressions())

            ts = intent_clsfr.run_tsne(n_components=2, perplexity=30, learning_rate=200)
            # print(ts)
            # [
            #     ('Can I get a quote please?', 'quote', 68.63184356689453, -49.94352340698242, 0.0),
            #     ('I would like to go to the menu.', 'menu', 18.918176651000977, 133.92724609375, 0.0),
            #     ('I need a quote.', 'quote', -80.57017517089844, 115.71224212646484, 0.0),
            #     ('Help would be good', 'help', 8.520785331726074, 32.45862579345703, 0.0),
            #     ('Can I go to the menu?', 'menu', 102.02958679199219, 57.748714447021484, 0.0),
            #     ('help me.', 'help', -73.67484283447266, 10.271224975585938, 0.0),
            #     ('Give me a quote please.', 'quote', -132.1832275390625, -67.88475799560547, 0.0),
            #     ('Can I get some help.', 'help', -163.59573364257812, 48.28276824951172, 0.0),
            #     ('Take me to the menu.', 'menu', -26.50295639038086, -84.29590606689453, 0.0)
            # ]
            self.assertTrue(ts[0][4] == 0.0)
            self.assertTrue(len(ts) == 9)
        # === ===


#         self.assertTrue(nlpe.purge_intent_clsfr("exampleIntentClsfr"))
#         self.assertTrue(nlpe.purge_word_manifold("glove6B50D_trimmed"))


if __name__ == '__main__':
    unittest.main()
