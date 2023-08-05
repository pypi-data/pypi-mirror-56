import unittest
import time

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestEmotion(BaseTestCase):
    def test_sample(self):
        print("Testing TestEmotion.test_sample.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        result_fear = nlpe.retrieve_emotion("I am so disgusted right now! I didn't like it at all.", None)
        print(result_fear)
        result_happiness = nlpe.retrieve_emotion("I liked it. It made me feel happy :-). "
                                                 "I'll definitely give it a good score.", None)
        print(result_happiness)

        end_time = time.time()

        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()


if __name__ == '__main__':
    unittest.main()
