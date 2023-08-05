# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestRegexEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_regex_extractor(self):
        print("Rest HTTP test_regex_extractor:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance regex_extr not loaded!'
                                       }))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors', 'post',
                                       {
                                           "name": "regex_extr",
                                           "long_name": "An example regular expression info extractor.",
                                           "desc": "Example regex extractor model.",
                                           "regex": r"(?P<license>"
                                                    r"([A-Z]{3}[ ]?[0-9]{3}[ ]?(GP|NW|MP|EC|L|NC|NW))|"
                                                    r"([A-Z]{2}[ ]?[0-9]{2}[ ]?[A-Z]{2}[ ]?(GP|NW|MP|EC|L|NC|NW)))",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example regex extractor model.',
                                           'long_name': 'An example regular expression info extractor.',
                                           'name': 'regex_extr'
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example regex extractor model.',
                                           'name': 'regex_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr/retrieve', 'post',
                                       {
                                           "text": "My car's registration is ABC 123 GP."
                                       },
                                       200,
                                       [{'license': 'ABC 123 GP'}]
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr', 'delete',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example regex extractor model.',
                                           'long_name': 'An example regular expression info extractor.',
                                           'name': 'regex_extr'
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors', 'post',
                                       {
                                           "name": "regex_extr",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "regex_extr"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example regex extractor model.',
                                           'name': 'regex_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr/retrieve', 'post',
                                       {
                                           "text": "My car's registration is ABC 123 GP."
                                       },
                                       200,
                                       [{'license': 'ABC 123 GP'}]
                                       ))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.regex_extr_dict.get(
            'regex_extr_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr/retrieve', 'post',
                                       {
                                           "text": "My car's registration is ABC 123 GP."
                                       },
                                       200,
                                       [{'license': 'ABC 123 GP'}]
                                       ))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr/retrieve', 'post',
                                       {},
                                       400,
                                       {
                                           'detail': "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr', 'delete',
                                       {},
                                       200,
                                       {}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors/regex_extr/retrieve', 'post',
                                       {
                                           "text": "My car's registration is ABC 123 GP."
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance regex_extr not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
