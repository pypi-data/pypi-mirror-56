# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestLangIdent(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_LR4(self):
        print("Rest HTTP test_LR4:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance lid_example not loaded!'
                                       }))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers', 'post',
                                       {
                                           "name": "lid_example",
                                           "desc": "Example LID model.",
                                           "lid_model_file": "lid_za",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example LID model.',
                                           'lid_model_file': 'lid_za',
                                           'long_name': None,
                                           'name': 'lid_example'
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example LID model.',
                                           'name': 'lid_example'
                                       }))

        # Test get labels.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/labels', 'get',
                                       {},
                                       200,
                                       ['xho', 'nso', 'zul', 'eng', 'ssw', 'afr', 'nbl', 'tso', 'ven', 'sot', 'tsn'],
                                       treat_list_as_set=True))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/retrieve', 'post',
                                       {
                                           "text": "The cat is in the house."
                                       },
                                       200,
                                       [{'label': 'eng', 'probability': 1.0},
                                        {'label': 'afr', 'probability': 1.7041383540301057e-60},
                                        {'label': 'tsn', 'probability': 3.9031868308561294e-73},
                                        {'label': 'ven', 'probability': 2.2479441574259235e-85},
                                        {'label': 'nso', 'probability': 5.861466515239353e-90},
                                        {'label': 'sot', 'probability': 9.740106378827311e-91},
                                        {'label': 'xho', 'probability': 1.8510154583541782e-93},
                                        {'label': 'tso', 'probability': 6.442227032779462e-94},
                                        {'label': 'nbl', 'probability': 2.5587322553377174e-98},
                                        {'label': 'ssw', 'probability': 3.249043293762235e-100},
                                        {'label': 'zul', 'probability': 1.4197098809450186e-106}]
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example', 'delete',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example LID model.',
                                           'lid_model_file': 'lid_za',
                                           'long_name': None,
                                           'name': 'lid_example'
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers', 'post',
                                       {
                                           "name": "lid_example",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "lid_example"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example', 'get',
                                       {},
                                       200,
                                       {
                                           'desc': 'Example LID model.',
                                           'name': 'lid_example'
                                       }))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/retrieve', 'post',
                                       {
                                           "text": "The cat is in the house."
                                       },
                                       200,
                                       [{'label': 'eng', 'probability': 1.0},
                                        {'label': 'afr', 'probability': 1.7041383540301057e-60},
                                        {'label': 'tsn', 'probability': 3.9031868308561294e-73},
                                        {'label': 'ven', 'probability': 2.2479441574259235e-85},
                                        {'label': 'nso', 'probability': 5.861466515239353e-90},
                                        {'label': 'sot', 'probability': 9.740106378827311e-91},
                                        {'label': 'xho', 'probability': 1.8510154583541782e-93},
                                        {'label': 'tso', 'probability': 6.442227032779462e-94},
                                        {'label': 'nbl', 'probability': 2.5587322553377174e-98},
                                        {'label': 'ssw', 'probability': 3.249043293762235e-100},
                                        {'label': 'zul', 'probability': 1.4197098809450186e-106}]
                                       ))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.lr4_language_recogniser_dict.get(
            'lid_example_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/retrieve', 'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       200,
                                       [{'label': 'eng', 'probability': 1.0},
                                        {'label': 'afr', 'probability': 3.1551502149880003e-26},
                                        {'label': 'tsn', 'probability': 3.900934015807359e-82},
                                        {'label': 'ven', 'probability': 6.7879449938599815e-84},
                                        {'label': 'sot', 'probability': 5.3907049034673925e-89},
                                        {'label': 'tso', 'probability': 1.1681169708416598e-97},
                                        {'label': 'zul', 'probability': 2.236261432942528e-99},
                                        {'label': 'xho', 'probability': 3.4869059434662704e-101},
                                        {'label': 'nso', 'probability': 2.708466310611158e-102},
                                        {'label': 'ssw', 'probability': 4.679964055020788e-103},
                                        {'label': 'nbl', 'probability': 1.807421468585205e-125}]
                                       ))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/retrieve', 'post',
                                       {},
                                       400,
                                       {
                                           'detail': "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example', 'delete',
                                       {},
                                       200,
                                       {}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers/lid_example/retrieve', 'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance lid_example not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
