# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestDucklingEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, True,  # use_duckling = True
                              *args, **kwargs)

    def test_duckling_extractor(self):
        print("Rest HTTP test_duckling_extractor:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance duckling_extr not loaded!'
                                       }))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors', 'post',
                                       {
                                           "name": "duckling_extr",
                                           "long_name": "An example duckling info extractor.",
                                           "desc": "Example duckling extractor model.",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example duckling extractor model.',
                                           'long_name': 'An example duckling info extractor.',
                                           'name': 'duckling_extr'
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example duckling extractor model.',
                                           'name': 'duckling_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr/retrieve', 'post',
                                       {
                                           "text": "The day after tomorrow at 15:00.",
                                           "reference_time": "2017-01-20"
                                       },
                                       200,
                                       [
                                           {
                                               'body': 'The day after tomorrow at 15:00',
                                               'dim': 'time',
                                               'grain': 'minute',
                                               'type': 'value',
                                           }
                                       ]
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr', 'delete',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example duckling extractor model.',
                                           'long_name': 'An example duckling info extractor.',
                                           'name': 'duckling_extr'
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors', 'post',
                                       {
                                           "name": "duckling_extr",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "duckling_extr"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example duckling extractor model.',
                                           'name': 'duckling_extr'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr/retrieve', 'post',
                                       {
                                           "text": "The day after tomorrow at 15:00.",
                                           "reference_time": "2017-01-20"
                                       },
                                       200,
                                       [
                                           {
                                               'body': 'The day after tomorrow at 15:00',
                                               'dim': 'time',
                                               'grain': 'minute',
                                               'type': 'value',
                                           }
                                       ]
                                       ))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.duckling_extr_dict.get(
            'duckling_extr_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr/retrieve', 'post',
                                       {
                                           "text": "The day after tomorrow at 15:00.",
                                           "reference_time": "2017-01-20"
                                       },
                                       200,
                                       [
                                           {
                                               'body': 'The day after tomorrow at 15:00',
                                               'dim': 'time',
                                               'grain': 'minute',
                                               'type': 'value',
                                           }
                                       ]
                                       ))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr/retrieve', 'post',
                                       {},
                                       400,
                                       {
                                           'detail': "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr', 'delete',
                                       {},
                                       200,
                                       {}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors/duckling_extr/retrieve', 'post',
                                       {
                                           "text": "The day after tomorrow at 15:00.",
                                           "reference_time": "2017-01-20"
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance duckling_extr not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
