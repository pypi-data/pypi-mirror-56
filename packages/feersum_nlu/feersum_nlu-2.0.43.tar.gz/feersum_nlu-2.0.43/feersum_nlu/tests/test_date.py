import unittest
import time
import os  # noqa # pylint: disable=unused-import

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestDate(BaseTestCase):
    def test_duckling(self):
        print("Testing TestDate.test_duckling.", flush=True)

        nlpe = nlp_engine.NLPEngine(use_duckling=True)

        # Switch to env var / QA instance of duckling. Default is prod instance.
        # duckling_url = os.environ.get("FEERSUM_NLU_DUCKLING_URL", "https://qonda.qa.feersum.io")
        # nlpe.set_duckling_url(duckling_url)

        start_time = time.time()

        num_iterations = 10
        for i in range(num_iterations):
            ent_list_1 = nlpe.retrieve_date("21 October 1981 at 8:00", "")
            ent_list_2 = nlpe.retrieve_date("The day after 5 Sept 1982", "past")

            self.assertEqual(ent_list_1, [('1981-10-21 08:00:00', 'minute')])
            self.assertEqual(ent_list_2, [('1982-09-06 00:00:00', 'day')])
            print('.', end='', flush=True)

        end_time = time.time()
        print()

        print('retrieve time = ' + str((end_time - start_time) / (num_iterations * 2.0)), flush=True)

        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

    def test_dateparse(self):
        print("Testing TestDate.test_dateparse.", flush=True)

        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        start_time = time.time()

        date_list_1 = nlpe.retrieve_date("21 October 1981 at 8:00", "")
        date_list_2 = nlpe.retrieve_date("5 Sept 1982", "")

        print(date_list_1, flush=True)
        print(date_list_2, flush=True)

        end_time = time.time()
        print('retrieve time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        self.assertEqual(date_list_1, [('1981-10-21 08:00:00', 'hour')])
        self.assertEqual(date_list_2, [('1982-09-05 00:00:00', 'day')])


if __name__ == '__main__':
    unittest.main()
