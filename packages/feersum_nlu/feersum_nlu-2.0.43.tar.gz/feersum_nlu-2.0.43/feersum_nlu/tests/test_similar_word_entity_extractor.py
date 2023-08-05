import unittest
import time
from typing import List  # noqa # pylint: disable=unused-import

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSimilarWordEntityExtractor(BaseTestCase):
    def test_accuracy(self):
        print("Testing TestSimilarWordEntityExtractor.test_accuracy.", flush=True)

        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']')
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']')
        print()

        print("Creating the word manifold...", flush=True)
        # nlpe.create_word_manifold_encoder("glove6B50D_trimmed", nlp_engine_data.get_path() + "/glove.6B.50d.trimmed.txt",
        #                                   stop_words=set(),
        #                                   spacies=["&", "#", "@", "？", "~", "”", "“", ".", ",",
        #                                            "?", ";", ":", "!", "(", ")",
        #                                            "{", "}",
        #                                            "[", "]", '"', "'", "`", "’", "-", "–", "/", "\\", "…"])
        nlpe.create_feers_language_model("glove6B50D_trimmed")

        print("Adding some words...", flush=True)
        manifold = nlpe.get_language_model("glove6B50D_trimmed")
        if manifold is not None:
            manifold.add_word_similar_to("avo", "avocado")

        print("Save the manifold...", flush=True, end='')
        success = nlpe.save_language_model("glove6B50D_trimmed")
        print(success, 'done.', flush=True)

        print("Load the manifold...", flush=True, end='')
        success = nlpe.load_language_model("glove6B50D_trimmed")
        print(success, 'done.', flush=True)

        colours = {"red", "green", "blue", "purple", "orange", "white", "black", "khaki", "beige", "silver", "brown"}
        toppings = {"cheese", "tomato", "salami", "pineapple", "chicken", "ham"}

        start_time = time.time()

        # ====
        print("retrieve_similar_entities...", flush=True)
        entity_list = nlpe.retrieve_similar_entities("My car has 120000 km on the clock ."
                                                     "It is a green Honda Jazz from 2009."
                                                     "My license plate number is AB34CDGP.",
                                                     colours,
                                                     0.8, "glove6B50D_trimmed", True, "")

        token_list = []

        for entity in entity_list:
            token_list.append(entity.get('entity'))

        self.assertTrue(token_list == ['green'])

        # ====
        entity_list = nlpe.retrieve_similar_entities("Can I please have cheddar, mushrooms, onions and avo.",
                                                     toppings,
                                                     0.75, "glove6B50D_trimmed", True, "")

        token_list.clear()

        for entity in entity_list:
            token_list.append(entity.get('entity'))

        self.assertTrue(token_list == ['cheddar', 'mushrooms', 'onions', 'avo'])

        end_time = time.time()
        print('TestIntentClsfr.test_accuracy time = ' + str(end_time - start_time))


if __name__ == '__main__':
    unittest.main()
