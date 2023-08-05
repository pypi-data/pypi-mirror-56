# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_request, check_response_test
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestCRFEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_crf_entity_extractor(self):
        print("Rest HTTP test_crf_entity_extractor:", flush=True)
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance crf1 not loaded!'}))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors', 'post',
                                       {"name": "crf1",
                                        "desc": "CRF extractor for the Feersum NLU SDK.",
                                        "load_from_store": False},
                                       200,
                                       {"name": "crf1"}))

        training_samples = [
            {
                "text": "Can I have a burger with chips please?",
                "entity_list": [{"index": 13, "len": 17, "entity": "food"}]
            },
            {
                "text": "Can I have a slice of pizza?",
                "entity_list": [{"index": 13, "len": 14, "entity": "food"}]
            },
            {
                "text": "Can I have a hot dog with mustard?",
                "entity_list": [{"index": 13, "len": 20, "entity": "food"}]
            }
        ]
        testing_samples = [
            {
                "text": "Can I have a burger with chips please?",
                "entity_list": [{"index": 13, "len": 17, "entity": "food"}]
            },
            {
                "text": "Can I have a slice of pizza?",
                "entity_list": [{"index": 13, "len": 14, "entity": "food"}]
            },
            {
                "text": "Can I have a hot dog with mustard?",
                "entity_list": [{"index": 13, "len": 20, "entity": "food"}]
            }
        ]

        # Add some training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/training_samples',
                                       'post',
                                       training_samples,
                                       200,
                                       training_samples))

        # Add some testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/testing_samples', 'post',
                                       testing_samples,
                                       200,
                                       testing_samples))
        #####
        # Test retrieve when not yet trained.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {"text": "Was the SDK programmed in C++?"},
                                       200,
                                       []))

        # Test train and save of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/train',
                                       'post',
                                       {
                                           "threshold": 0.98,
                                       },
                                       200,
                                       {"name": "crf1"}))

        # Test delete of training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/training_samples_all', 'delete',
                                       {},
                                       200,
                                       training_samples,
                                       ))

        print("Test delete of single testing sample...", flush=True)

        # Test delete of single testing sample.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/testing_samples',
                                       'delete',
                                       [
                                           testing_samples[1]
                                       ],
                                       200,
                                       [
                                           testing_samples[1]
                                       ],
                                       ))

        # Test delete of testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/testing_samples_all', 'delete',
                                       {},
                                       200,
                                       [
                                           testing_samples[0],
                                           testing_samples[2]
                                       ],
                                       treat_list_as_set=True))

        # Add training samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/training_samples',
                                       'post',
                                       training_samples,
                                       200,
                                       training_samples))

        # Test get training data.
        response = check_response_request(self.client,
                                          f'/nlu/v2/crf_entity_extractors/crf1/training_samples', 'get',
                                          {})
        self.assertTrue(check_response_test(response,
                                            200,
                                            training_samples,
                                            treat_list_as_set=True))

        uuid_to_delete = response.json[2]['uuid']

        # Test delete of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/crf_entity_extractors/crf1/training_samples', 'delete',
                                       [{"uuid": uuid_to_delete}],
                                       200,
                                       [
                                           training_samples[2]
                                       ],
                                       treat_list_as_set=True))

        # Add training samples back (ignoring duplicates).
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/training_samples',
                                       'post',
                                       training_samples,
                                       200,
                                       [
                                           training_samples[2]
                                       ]
                                       ))

        # Add testing samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/testing_samples', 'post',
                                       testing_samples,
                                       200,
                                       testing_samples))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1', 'delete',
                                       {},
                                       200,
                                       {"name": "crf1"}))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors', 'post',
                                       {"name": "crf1",
                                        "load_from_store": True},
                                       200,
                                       {"name": "crf1"}))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1', 'get',
                                       {},
                                       200,
                                       {
                                           "desc": "CRF extractor for the Feersum NLU SDK.",
                                           "name": "crf1"
                                       }))

        # Test get training data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/training_samples',
                                       'get',
                                       {},
                                       200,
                                       training_samples,
                                       ))

        # Test get testing data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/testing_samples',
                                       'get',
                                       {},
                                       200,
                                       testing_samples,
                                       ))

        ######
        # Test retrieve.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {"text": "I would like to buy a beef sandwich with mustard."},
                                       200,
                                       [
                                           {'entity': 'food', 'index': 22, 'len': 26}
                                       ]))

        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {"text": "wh"},
                                       200,
                                       [
                                           {'entity': 'food', 'index': 0, 'len': 2}
                                       ]))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        crf_meta_info = wrapper_util.crf_extr_dict.get('crf1_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(crf_meta_info is not None)
        if crf_meta_info is not None:
            crf_meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # entity_wrapper_crf.crf_extr_trash_helper('crf1_FEERSUM-NLU-591-4ba0-8905-996076e94d')

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {"text": "I would like to buy a beef sandwich with mustard."},
                                       200,
                                       [
                                           {'entity': 'food', 'index': 22, 'len': 26}
                                       ]))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1', 'delete',
                                       {},
                                       200,
                                       {"name": "crf1"}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/crf_entity_extractors/crf1/retrieve',
                                       'post',
                                       {"text": "I would like to buy a beef sandwich with mustard."},
                                       400,
                                       {'error_detail': 'Named instance crf1 not loaded!'}))

        print('time = ' + str(time.time() - start_time))
        print()
