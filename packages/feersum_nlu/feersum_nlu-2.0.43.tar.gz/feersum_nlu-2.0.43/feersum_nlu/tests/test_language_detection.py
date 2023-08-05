import unittest

# from feersum_nlu import nlp_engine
# from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


@unittest.skip("skipping during dev")
class TestLanguageDetection(BaseTestCase):
    def test_lid(self):
        print("Testing TestLanguageDetection.test_lid.", flush=True)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
