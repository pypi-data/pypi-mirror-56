# import unittest
from typing import Optional  # noqa # pylint: disable=unused-import

import time
import uuid
import json

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_request, check_response_test
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestAPIKeyManagement(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_api_key_management(self):
        print("Rest HTTP test_api_key_management:")
        start_time = time.time()

        # Add the ADMIN auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Admin & Testing.")
        wrapper_util.add_admin_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Admin & Testing.")

        # random api key to test response for unknown key.
        user_key = str(uuid.uuid4())  # type: Optional[str]

        # Test get detail when user key does not exist.
        self.assertTrue(check_response(self.client,
                                       f"/nlu/v2/api_keys/{user_key}", 'get',
                                       {},
                                       400,
                                       {'error_detail': f"API key {user_key} not found!"}))

        # === Test create ===
        response = check_response_request(self.client,
                                          '/nlu/v2/api_keys', 'post',
                                          {
                                              "desc": "API key for testing.",
                                              "call_count_limit": 10,
                                              "load_from_store": False
                                          })

        self.assertTrue(check_response_test(response, 200, {"desc": "API key for testing."}))
        # === ===

        try:
            response_data = json.loads(response.data.decode("utf-8"))
            user_key = response_data['api_key']
        except (ValueError, KeyError):
            user_key = None

        print("user_key =", user_key)

        self.assertTrue(user_key is not None)

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       f"/nlu/v2/api_keys/{user_key}", 'get',
                                       {},
                                       200,
                                       {
                                           'api_key': f"{user_key}",
                                           'call_count': 0,
                                           'call_count_limit': 10,
                                           'desc': 'API key for testing.'
                                       }))

        # Test update detail (call_count_limit only)
        self.assertTrue(check_response(self.client,
                                       f"/nlu/v2/api_keys/{user_key}", 'post',
                                       {
                                           "call_count_limit": 20,
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'api_key': f"{user_key}",
                                           'call_count': 0,
                                           'call_count_limit': 20,
                                           "desc": "API key for testing.",
                                       }))

        # Test update detail.
        response = check_response_request(self.client,
                                          f"/nlu/v2/api_keys/{user_key}", 'post',
                                          {
                                              "desc": "API key for testing (updated).",
                                              "call_count_limit": 100,
                                              "load_from_store": False
                                          })
        self.assertTrue(check_response_test(response, 200,
                                            {
                                                'api_key': f"{user_key}",
                                                'call_count': 0,
                                                'call_count_limit': 100,
                                                "desc": "API key for testing (updated).",
                                            }))

        # Test get detail of the internal key used for testing.
        response = check_response_request(self.client,
                                          "/nlu/v2/api_keys/FEERSUM-NLU-591-4ba0-8905-996076e94d", 'get',
                                          {})
        self.assertTrue(check_response_test(response, 200,
                                            {
                                                'api_key': "FEERSUM-NLU-591-4ba0-8905-996076e94d",
                                                'call_count': 4,
                                                'call_count_limit': None,
                                                'desc': 'Admin & Testing.',
                                                'call_count_breakdown': {'api_key_create': 1,
                                                                         'api_key_get_details': 1,
                                                                         'api_key_update_details': 2}
                                            }))

        # Test delete
        response = check_response_request(self.client,
                                          f"/nlu/v2/api_keys/{user_key}", 'delete',
                                          {})
        self.assertTrue(check_response_test(response, 200,
                                            {
                                                'api_key': f"{user_key}",
                                                'call_count': 0,
                                                'call_count_limit': 100,
                                                "desc": "API key for testing (updated).",
                                            }))

        # random api key to test update to add key entry with existing key.
        user_key_new = str(uuid.uuid4())  # type: Optional[str]

        # Test update to add key entry with existing key.
        self.assertTrue(check_response(self.client,
                                       f"/nlu/v2/api_keys/{user_key_new}", 'post',
                                       {
                                           "desc": "API key for testing (new).",
                                           "call_count_limit": 200,
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'api_key': f"{user_key_new}",
                                           'call_count': 0,
                                           'call_count_limit': 200,
                                           "desc": "API key for testing (new).",
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       f"/nlu/v2/api_keys/{user_key_new}", 'delete',
                                       {},
                                       200,
                                       {
                                           'api_key': f"{user_key_new}",
                                           'call_count': 0,
                                           'call_count_limit': 200,
                                           "desc": "API key for testing (new).",
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
