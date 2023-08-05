# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestDataObject(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_data_object(self):
        print("Rest HTTP test_data_object:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail if object doesn't exist yet.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance app_data not found!'}))

        # Test create/update - POST creates the data object if it doesn't yet exist.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'post',
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       },
                                       200,
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'get',
                                       {},
                                       200,
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       }))

        # Test get detail ALL.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects', 'get',
                                       {},
                                       200,
                                       ['app_data']))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'delete',
                                       {},
                                       200,
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       }))

        # Test restore/un-trash i.e. create from store.

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance app_data not found!'}))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'delete',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance app_data not found!'}))

        # Test get when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance app_data not found!'}))

        # Test create/update - POST creates the data object if it doesn't yet exist.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data', 'post',
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       },
                                       200,
                                       {
                                           "data":
                                               {
                                                   "app_attr1_key": "app_attr1_value",
                                                   "app_attr2_key": "app_attr1_value"
                                               }
                                       }))

        # Test create/update - POST creates the data object if it doesn't yet exist.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/comp_data', 'post',
                                       {
                                           "data":
                                               {
                                                   "comp_attr1_key": "comp_attr1_value",
                                                   "comp_attr2_key": "comp_attr1_value"
                                               }
                                       },
                                       200,
                                       {
                                           "data":
                                               {
                                                   "comp_attr1_key": "comp_attr1_value",
                                                   "comp_attr2_key": "comp_attr1_value"
                                               }
                                       }))

        # Test trashing of ALL models.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects', 'delete',
                                       {},
                                       200,
                                       ['comp_data', 'app_data'],
                                       treat_list_as_set=True))

        # Test vaporise
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/app_data/vaporise', 'post',
                                       {},
                                       200,
                                       {
                                           'data': {'app_attr1_key': 'app_attr1_value',
                                                    'app_attr2_key': 'app_attr1_value'}
                                        }))

        # Test vaporise
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/data_objects/comp_data/vaporise', 'post',
                                       {},
                                       200,
                                       {
                                           'data': {'comp_attr1_key': 'comp_attr1_value',
                                                    'comp_attr2_key': 'comp_attr1_value'}
                                        }))

        print('time = ' + str(time.time() - start_time))
        print()
