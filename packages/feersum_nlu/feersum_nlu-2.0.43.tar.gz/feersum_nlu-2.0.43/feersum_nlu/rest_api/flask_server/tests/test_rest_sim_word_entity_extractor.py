# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestSimWordEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_sim_word_extractor(self):
        print("Rest HTTP test_sim_word_extractor:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance sim_word_extr not loaded!'
                                       }))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors', 'post',
                                       {
                                           "name": "sim_word_extr",
                                           "long_name": "An example sim word info extractor.",
                                           "desc": "Example sim word extractor model.",
                                           "similar_words": ['cat'],
                                           "threshold": 0.6,
                                           "word_manifold": "glove6B50D_trimmed",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example sim word extractor model.',
                                           "long_name": "An example sim word info extractor.",
                                           'name': 'sim_word_extr'
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example sim word extractor model.',
                                           'name': 'sim_word_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr/retrieve', 'post',
                                       {
                                           "text": "I have a cat and a dog and some other pets."
                                       },
                                       200,
                                       [{'entity': 'cat', 'similarity': 1.0},
                                        {'entity': 'dog', 'similarity': 0.9218005273769249},
                                        {'entity': 'pets', 'similarity': 0.6448809531912634}]
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr', 'delete',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example sim word extractor model.',
                                           "long_name": "An example sim word info extractor.",
                                           'name': 'sim_word_extr'
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors', 'post',
                                       {
                                           "name": "sim_word_extr",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "sim_word_extr"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example sim word extractor model.',
                                           'name': 'sim_word_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr/retrieve', 'post',
                                       {
                                           "text": "I have a cat and a dog and some other pets."
                                       },
                                       200,
                                       [{'entity': 'cat', 'similarity': 1.0},
                                        {'entity': 'dog', 'similarity': 0.9218005273769249},
                                        {'entity': 'pets', 'similarity': 0.6448809531912634}]
                                       ))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.sim_word_extr_dict.get(
            'sim_word_extr_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr/retrieve', 'post',
                                       {
                                           "text": "I have a cat and a dog and some other pets."
                                       },
                                       200,
                                       [{'entity': 'cat', 'similarity': 1.0},
                                        {'entity': 'dog', 'similarity': 0.9218005273769249},
                                        {'entity': 'pets', 'similarity': 0.6448809531912634}]
                                       ))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr/retrieve', 'post',
                                       {},
                                       400,
                                       {
                                           'detail': "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr', 'delete',
                                       {},
                                       200,
                                       {}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors/sim_word_extr/retrieve', 'post',
                                       {
                                           "text": "I have a cat and a dog and some other pets."
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance sim_word_extr not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
