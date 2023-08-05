# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestPersonNameEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_person_name_extractor(self):
        print("Rest HTTP test_person_name_extractor:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance person_name_extr not loaded!'
                                       }))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors', 'post',
                                       {
                                           "name": "person_name_extr",
                                           "long_name": "An example person name info extractor.",
                                           "desc": "Example person name extractor model.",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example person name extractor model.',
                                           'long_name': 'An example person name info extractor.',
                                           'name': 'person_name_extr'
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example person name extractor model.',
                                           'name': 'person_name_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr/retrieve', 'post',
                                       {
                                           "text": "My name is Clark Kent.",
                                       },
                                       200,
                                       ['Clark Kent']
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr', 'delete',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example person name extractor model.',
                                           'long_name': 'An example person name info extractor.',
                                           'name': 'person_name_extr'
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors', 'post',
                                       {
                                           "name": "person_name_extr",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "person_name_extr"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example person name extractor model.',
                                           'name': 'person_name_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr/retrieve', 'post',
                                       {
                                           "text": "My name is Clark Kent.",
                                       },
                                       200,
                                       ['Clark Kent']
                                       ))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.person_name_extr_dict.get(
            'person_name_extr_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr/retrieve', 'post',
                                       {
                                           "text": "My name is Clark Kent.",
                                       },
                                       200,
                                       ['Clark Kent']
                                       ))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr/retrieve', 'post',
                                       {},
                                       400,
                                       {
                                           'detail': "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr', 'delete',
                                       {},
                                       200,
                                       {}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors/person_name_extr/retrieve', 'post',
                                       {
                                           "text": "My name is Clark Kent.",
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance person_name_extr not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
